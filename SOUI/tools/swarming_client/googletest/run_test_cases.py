#!/usr/bin/env python
# Copyright 2013 The Swarming Authors. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0 that
# can be found in the LICENSE file.

"""Runs each test cases as a single shard, single process execution.

Similar to sharding_supervisor.py but finer grained. It runs each test case
individually instead of running per shard. Runs multiple instances in parallel.
"""

import datetime
import fnmatch
import json
import logging
import optparse
import os
import random
import re
import sys
import threading
import time
from xml.dom import minidom
import xml.parsers.expat

# Directory with this file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Root of a repository.
ROOT_DIR = os.path.dirname(BASE_DIR)
# Name of the optional package with all dependencies.
DEPENDENCIES_ZIP = os.path.join(BASE_DIR, 'run_isolated.zip')

# When running in isolated environment, dependencies is in zipped package.
if os.path.exists(DEPENDENCIES_ZIP):
  sys.path.insert(0, DEPENDENCIES_ZIP)
else:
  # Otherwise it is in the root of the repository.
  if not ROOT_DIR in sys.path:
    sys.path.insert(0, ROOT_DIR)


from utils import subprocess42
from utils import threading_utils
from utils import tools


# These are known to influence the way the output is generated.
KNOWN_GTEST_ENV_VARS = [
  'GTEST_ALSO_RUN_DISABLED_TESTS',
  'GTEST_BREAK_ON_FAILURE',
  'GTEST_CATCH_EXCEPTIONS',
  'GTEST_COLOR',
  'GTEST_FILTER',
  'GTEST_OUTPUT',
  'GTEST_PRINT_TIME',
  'GTEST_RANDOM_SEED',
  'GTEST_REPEAT',
  'GTEST_SHARD_INDEX',
  'GTEST_SHARD_STATUS_FILE',
  'GTEST_SHUFFLE',
  'GTEST_THROW_ON_FAILURE',
  'GTEST_TOTAL_SHARDS',
]

# These needs to be poped out before running a test.
GTEST_ENV_VARS_TO_REMOVE = [
  'GTEST_ALSO_RUN_DISABLED_TESTS',
  'GTEST_FILTER',
  'GTEST_OUTPUT',
  'GTEST_RANDOM_SEED',
  # TODO(maruel): Handle.
  'GTEST_REPEAT',
  'GTEST_SHARD_INDEX',
  # TODO(maruel): Handle.
  'GTEST_SHUFFLE',
  'GTEST_TOTAL_SHARDS',
]


RUN_PREFIX = '[ RUN      ] '
OK_PREFIX = '[       OK ] '
FAILED_PREFIX = '[  FAILED  ] '


class Failure(Exception):
  pass


def setup_gtest_env():
  """Copy the enviroment variables and setup for running a gtest."""
  env = os.environ.copy()
  for name in GTEST_ENV_VARS_TO_REMOVE:
    env.pop(name, None)

  # Forcibly enable color by default, if not already disabled.
  env.setdefault('GTEST_COLOR', 'on')

  return env


def gtest_list_tests(cmd, cwd):
  """List all the test cases for a google test.

  See more info at http://code.google.com/p/googletest/.
  """
  cmd = cmd[:]
  cmd.append('--gtest_list_tests')
  env = setup_gtest_env()
  timeout = 0.
  try:
    out, err, returncode, _ = subprocess42.call_with_timeout(
        cmd,
        timeout,
        stderr=subprocess42.PIPE,
        env=env,
        cwd=cwd)
  except OSError, e:
    raise Failure('Failed to run %s\ncwd=%s\n%s' % (' '.join(cmd), cwd, str(e)))
  if returncode:
    raise Failure(
        'Failed to run %s\nstdout:\n%s\nstderr:\n%s' %
          (' '.join(cmd), out, err), returncode)
  # pylint: disable=E1103
  if err and not err.startswith('Xlib:  extension "RANDR" missing on display '):
    logging.error('Unexpected spew in gtest_list_tests:\n%s\n%s', err, cmd)
  return out


def filter_shards(tests, index, shards):
  """Filters the shards.

  Watch out about integer based arithmetics.
  """
  # The following code could be made more terse but I liked the extra clarity.
  assert 0 <= index < shards
  total = len(tests)
  quotient, remainder = divmod(total, shards)
  # 1 item of each remainder is distributed over the first 0:remainder shards.
  # For example, with total == 5, index == 1, shards == 3
  # min_bound == 2, max_bound == 4.
  min_bound = quotient * index + min(index, remainder)
  max_bound = quotient * (index + 1) + min(index + 1, remainder)
  return tests[min_bound:max_bound]


def _starts_with(a, b, prefix):
  return a.startswith(prefix) or b.startswith(prefix)


def is_valid_test_case(test, disabled):
  """Returns False on malformed or DISABLED_ test cases."""
  if not '.' in test:
    logging.error('Ignoring unknown test %s', test)
    return False
  fixture, case = test.split('.', 1)
  if not disabled and _starts_with(fixture, case, 'DISABLED_'):
    return False
  return True


def filter_bad_tests(tests, disabled):
  """Filters out malformed or DISABLED_ test cases."""
  return [test for test in tests if is_valid_test_case(test, disabled)]


def chromium_is_valid_test_case(test, disabled, fails, flaky, pre, manual):
  """Return False on chromium specific bad tests in addition to
  is_valid_test_case().

  FAILS_, FLAKY_, PRE_, MANUAL_ and other weird Chromium-specific test cases.
  """
  if not is_valid_test_case(test, disabled):
    return False
  fixture, case = test.split('.', 1)
  if not fails and _starts_with(fixture, case, 'FAILS_'):
    return False
  if not flaky and _starts_with(fixture, case, 'FLAKY_'):
    return False
  if not pre and _starts_with(fixture, case, 'PRE_'):
    return False
  if not manual and _starts_with(fixture, case, 'MANUAL_'):
    return False
  if test == 'InProcessBrowserTest.Empty':
    return False
  return True


def chromium_filter_bad_tests(tests, disabled, fails, flaky, pre, manual):
  """Filters out chromium specific bad tests in addition to filter_bad_tests().

  Filters out FAILS_, FLAKY_, PRE_, MANUAL_ and other weird Chromium-specific
  test cases.
  """
  return [
    test for test in tests if chromium_is_valid_test_case(
        test, disabled, fails, flaky, pre, manual)
  ]


def chromium_filter_pre_tests(test_case_results):
  """Filters out PRE_ test case results."""
  return (
      i for i in test_case_results if chromium_is_valid_test_case(
          i['test_case'],
          disabled=True,
          fails=True,
          flaky=True,
          pre=False,
          manual=True))


def parse_gtest_cases(out, seed):
  """Returns the flattened list of test cases in the executable.

  The returned list is sorted so it is not dependent on the order of the linked
  objects. Then |seed| is applied to deterministically shuffle the list if
  |seed| is a positive value. The rationale is that the probability of two test
  cases stomping on each other when run simultaneously is high for test cases in
  the same fixture. By shuffling the tests, the probability of these badly
  written tests running simultaneously, let alone being in the same shard, is
  lower.

  Expected format is a concatenation of this:
  TestFixture1
     TestCase1
     TestCase2
  """
  tests = []
  fixture = None
  lines = out.splitlines()
  while lines:
    line = lines.pop(0)
    if not line:
      break
    if not line.startswith('  '):
      fixture = line
    else:
      case = line[2:]
      if case.startswith('YOU HAVE'):
        # It's a 'YOU HAVE foo bar' line. We're done.
        break
      assert ' ' not in case
      tests.append(fixture + case)
  tests = sorted(tests)
  if seed:
    # Sadly, python's random module doesn't permit local seeds.
    state = random.getstate()
    try:
      # This is totally deterministic.
      random.seed(seed)
      random.shuffle(tests)
    finally:
      random.setstate(state)
  return tests


def list_test_cases(cmd, cwd, index, shards, seed, disabled):
  """Returns the list of test cases according to the specified criterias."""
  tests = parse_gtest_cases(gtest_list_tests(cmd, cwd), seed)

  # TODO(maruel): Splitting shards before filtering bad test cases could result
  # in inbalanced shards.
  if shards:
    tests = filter_shards(tests, index, shards)
  return filter_bad_tests(tests, disabled)


def chromium_list_test_cases(
    cmd, cwd, index, shards, seed, disabled, fails, flaky, pre, manual):
  """Returns the list of test cases according to the specified criterias."""
  tests = list_test_cases(cmd, cwd, index, shards, seed, disabled)
  return chromium_filter_bad_tests(tests, disabled, fails, flaky, pre, manual)


class RunSome(object):
  """Thread-safe object deciding if testing should continue."""
  def __init__(
      self, expected_count, retries, min_failures, max_failure_ratio,
      max_failures):
    """Determines if it is better to give up testing after an amount of failures
    and successes.

    Arguments:
    - expected_count is the expected number of elements to run.
    - retries is how many time a failing element can be retried. retries should
      be set to the maximum number of retries per failure. This permits
      dampening the curve to determine threshold where to stop.
    - min_failures is the minimal number of failures to tolerate, to put a lower
      limit when expected_count is small. This value is multiplied by the number
      of retries.
    - max_failure_ratio is the ratio of permitted failures, e.g. 0.1 to stop
      after 10% of failed test cases.
    - max_failures is the absolute maximum number of tolerated failures or None.

    For large values of expected_count, the number of tolerated failures will be
    at maximum "(expected_count * retries) * max_failure_ratio".

    For small values of expected_count, the number of tolerated failures will be
    at least "min_failures * retries".
    """
    assert 0 < expected_count
    assert 0 <= retries < 100
    assert 0 <= min_failures
    assert 0. < max_failure_ratio < 1.
    # Constants.
    self._expected_count = expected_count
    self._retries = retries
    self._min_failures = min_failures
    self._max_failure_ratio = max_failure_ratio

    self._min_failures_tolerated = self._min_failures * (self._retries + 1)
    # Pre-calculate the maximum number of allowable failures. Note that
    # _max_failures can be lower than _min_failures.
    self._max_failures_tolerated = round(
        (expected_count * (retries + 1)) * max_failure_ratio)
    if max_failures is not None:
      # Override the ratio if necessary.
      self._max_failures_tolerated = min(
          self._max_failures_tolerated, max_failures)
      self._min_failures_tolerated = min(
          self._min_failures_tolerated, max_failures)

    # Variables.
    self._lock = threading.Lock()
    self._passed = 0
    self._failures = 0
    self.stopped = False

  def should_stop(self):
    """Stops once a threshold was reached. This includes retries."""
    with self._lock:
      if self.stopped:
        return True
      # Accept at least the minimum number of failures.
      if self._failures <= self._min_failures_tolerated:
        return False
      if self._failures >= self._max_failures_tolerated:
        self.stopped = True
      return self.stopped

  def got_result(self, passed):
    with self._lock:
      if passed:
        self._passed += 1
      else:
        self._failures += 1

  def __str__(self):
    return '%s(%d, %d, %d, %.3f)' % (
        self.__class__.__name__,
        self._expected_count,
        self._retries,
        self._min_failures,
        self._max_failure_ratio)


class RunAll(object):
  """Never fails."""
  stopped = False

  @staticmethod
  def should_stop():
    return False

  @staticmethod
  def got_result(_):
    pass


def process_output(lines, test_cases):
  """Yield the data of each test cases.

  Expects the test cases to be run in the order of the list.

  Handles the following google-test behavior:
    - Test case crash causing a partial number of test cases to be run.
    - Invalid test case name so the test case wasn't run at all.

  This function automatically distribute the startup cost across each test case.
  """
  test_cases = test_cases[:]
  test_case = None
  test_case_data = None
  # Accumulates the junk between test cases.
  accumulation = ''
  eat_last_lines = False

  for line in lines:
    if eat_last_lines:
      test_case_data['output'] += line
      continue

    i = line.find(RUN_PREFIX)
    if i > 0 and test_case_data:
      # This may occur specifically in browser_tests, because the test case is
      # run in a child process. If the child process doesn't terminate its
      # output with a LF, it may cause the "[ RUN    ]" line to be improperly
      # printed out in the middle of a line.
      test_case_data['output'] += line[:i]
      line = line[i:]
      i = 0
    if i >= 0:
      if test_case:
        # The previous test case had crashed. No idea about its duration
        test_case_data['returncode'] = 1
        test_case_data['duration'] = 0
        test_case_data['crashed'] = True
        yield test_case_data

      test_case = line[len(RUN_PREFIX):].strip().split(' ', 1)[0]
      # Accept the test case even if it was unexpected.
      if test_case in test_cases:
        test_cases.remove(test_case)
      else:
        logging.warning('Unexpected test case: %s', test_case)
      test_case_data = {
        'test_case': test_case,
        'returncode': None,
        'duration': None,
        'output': accumulation + line,
      }
      accumulation = ''

    elif test_case:
      test_case_data['output'] += line
      i = line.find(OK_PREFIX)
      if i >= 0:
        result = 0
        line = line[i + len(OK_PREFIX):]
      else:
        i = line.find(FAILED_PREFIX)
        if i >= 0:
          line = line[i + len(FAILED_PREFIX):]
          result = 1
      if i >= 0:
        # The test completed. It's important to make sure the test case name
        # match too, since it could be a fake output.
        if line.startswith(test_case):
          line = line[len(test_case):]
          match = re.search(r' \((\d+) ms\)', line)
          if match:
            test_case_data['duration'] = float(match.group(1)) / 1000.
          else:
            # Make sure duration is at least not None since the test case ran.
            test_case_data['duration'] = 0
          test_case_data['returncode'] = result
          if not test_cases:
            # Its the last test case. Eat all the remaining lines.
            eat_last_lines = True
            continue
          yield test_case_data
          test_case = None
          test_case_data = None
    else:
      accumulation += line

  # It's guaranteed here that the lines generator is exhausted.
  if eat_last_lines:
    yield test_case_data
    test_case = None
    test_case_data = None

  if test_case_data:
    # This means the last one likely crashed.
    test_case_data['crashed'] = True
    test_case_data['duration'] = 0
    test_case_data['returncode'] = 1
    test_case_data['output'] += accumulation
    yield test_case_data

  # If test_cases is not empty, these test cases were not run.
  for t in test_cases:
    yield {
      'test_case': t,
      'returncode': None,
      'duration': None,
      'output': None,
    }


def convert_to_lines(generator):
  """Turn input coming from a generator into lines.

  It is Windows-friendly.
  """
  accumulator = ''
  for data in generator:
    items = (accumulator + data).splitlines(True)
    for item in items[:-1]:
      yield item
    if items[-1].endswith(('\r', '\n')):
      yield items[-1]
      accumulator = ''
    else:
      accumulator = items[-1]
  if accumulator:
    yield accumulator


class ResetableTimeout(object):
  """A resetable timeout that acts as a float.

  At each reset, the timeout is increased so that it still has the equivalent
  of the original timeout value, but according to 'now' at the time of the
  reset.
  """
  def __init__(self, timeout):
    assert timeout >= 0.
    self.timeout = float(timeout)
    self.last_reset = time.time()

  def reset(self):
    """Respendish the timeout."""
    now = time.time()
    self.timeout += max(0., now - self.last_reset)
    self.last_reset = now
    return now

  @staticmethod
  def __bool__():
    return True

  def __float__(self):
    """To be used as a timeout value for a function call."""
    return self.timeout


class GoogleTestRunner(object):
  """Immutable settings to run many test cases in a loop."""
  def __init__(
      self,
      cmd,
      cwd_dir,
      timeout,
      progress,
      retries,
      decider,
      verbose,
      add_task,
      add_serial_task,
      filter_results):
    """Defines how to run a googletest executable.

    Arguments:
    - cmd: command line to start with.
    - cwd_dir: directory to start the app in.
    - timeout: timeout while waiting for output.
    - progress: object to present the user with status updates.
    - retries: number of allowed retries. For example if 2, the test case will
      be tried 3 times in total.
    - decider: object to decide if the run should be stopped early.
    - verbose: inconditionally prints output.
    - add_task: function to add the task back when failing, for retry.
    - add_serial_task: function to add the task back when failing too often so
                       it should be run serially.
    - filter_results: optional function to filter undesired extraneous test case
                      run without our consent.
    """
    self.cmd = cmd[:]
    self.cwd_dir = cwd_dir
    self.timeout = timeout
    self.progress = progress
    self.retries = retries
    self.decider = decider
    self.verbose = verbose
    self.add_task = add_task
    self.add_serial_task = add_serial_task
    self.filter_results = filter_results or (lambda x: x)
    # It is important to remove the shard environment variables since it could
    # conflict with --gtest_filter.
    self.env = setup_gtest_env()

  def map(self, priority, test_cases, try_count):
    """Traces a single test case and returns its output.

    try_count is 0 based, the original try is 0.
    """
    if self.decider.should_stop():
      raise StopIteration()
    cmd = self.cmd + ['--gtest_filter=%s' % ':'.join(test_cases)]
    if '--gtest_print_time' not in cmd:
      cmd.append('--gtest_print_time')
    proc = subprocess42.Popen(
        cmd,
        cwd=self.cwd_dir,
        stdout=subprocess42.PIPE,
        stderr=subprocess42.STDOUT,
        env=self.env)

    # Use an intelligent timeout that can be reset. The idea is simple, the
    # timeout is set to the value of the timeout for a single test case.
    # Everytime a test case is parsed, the timeout is reset to its full value.
    # proc.yield_any() uses float() to extract the instantaneous value of
    # 'timeout'.
    timeout = ResetableTimeout(self.timeout)

    # Create a pipeline of generators.
    gen_lines = convert_to_lines(data for _, data in proc.yield_any(timeout))
    # It needs to be valid utf-8 otherwise it can't be stored.
    # TODO(maruel): Be more intelligent than decoding to ascii.
    gen_lines_utf8 = (
      line.decode('ascii', 'ignore').encode('utf-8') for line in gen_lines)
    gen_test_cases = process_output(gen_lines_utf8, test_cases)
    last_timestamp = proc.start
    got_failure_at_least_once = False
    results = []
    for i in self.filter_results(gen_test_cases):
      results.append(i)
      now = timeout.reset()
      test_case_has_passed = (i['returncode'] == 0)
      if i['duration'] is None:
        assert not test_case_has_passed
        # Do not notify self.decider, because an early crash in a large cluster
        # could cause the test to quit early.
      else:
        i['duration'] = max(i['duration'], now - last_timestamp)
        # A new test_case completed.
        self.decider.got_result(test_case_has_passed)

      need_to_retry = not test_case_has_passed and try_count < self.retries
      got_failure_at_least_once |= not test_case_has_passed
      last_timestamp = now

      # Create the line to print out.
      if i['duration'] is not None:
        duration = '(%.2fs)' % i['duration']
      else:
        duration = '<unknown>'
      if try_count:
        line = '%s %s - retry #%d' % (i['test_case'], duration, try_count)
      else:
        line = '%s %s' % (i['test_case'], duration)
      if self.verbose or not test_case_has_passed or try_count > 0:
        # Print output in one of three cases:
        # - --verbose was specified.
        # - The test failed.
        # - The wasn't the first attempt (this is needed so the test parser can
        #   detect that a test has been successfully retried).
        if i['output']:
          line += '\n' + i['output']
      self.progress.update_item(line, index=1, size=int(need_to_retry))

      if need_to_retry:
        priority = self._retry(priority, i['test_case'], try_count)

      # Delay yielding when only one test case is running, in case of a
      # crash-after-succeed.
      if len(test_cases) > 1:
        yield i

    if proc.returncode and not got_failure_at_least_once:
      if results and len(test_cases) == 1:
        # Crash after pass.
        results[-1]['returncode'] = proc.returncode

      if try_count < self.retries:
        # This is tricky, one of the test case failed but each did print that
        # they succeeded! Retry them *all* individually.
        if not self.verbose and not try_count:
          # Print all the output as one shot when not verbose to be sure the
          # potential stack trace is printed.
          output = ''.join(i['output'] for i in results)
          self.progress.update_item(output, raw=True)
        for i in results:
          priority = self._retry(priority, i['test_case'], try_count)
          self.progress.update_item('', size=1)

    # Only yield once the process completed when there is only one test case as
    # a safety precaution.
    if results and len(test_cases) == 1:
      yield results[-1]

  def _retry(self, priority, test_case, try_count):
    """Adds back the same task again only if relevant.

    It may add it either at lower (e.g. higher value) priority or at the end of
    the serially executed list.
    """
    if try_count + 1 < self.retries:
      # The test failed and needs to be retried normally.
      # Leave a buffer of ~40 test cases before retrying.
      priority += 40
      self.add_task(priority, self.map, priority, [test_case], try_count + 1)
    else:
      # This test only has one retry left, so the final retry should be
      # done serially.
      self.add_serial_task(
          priority, self.map, priority, [test_case], try_count + 1)
    return priority


class ChromiumGoogleTestRunner(GoogleTestRunner):
  def __init__(self, *args, **kwargs):
    super(ChromiumGoogleTestRunner, self).__init__(
        *args, filter_results=chromium_filter_pre_tests, **kwargs)


def get_test_cases(
    cmd, cwd, whitelist, blacklist, index, shards, seed, disabled, fails, flaky,
    manual):
  """Returns the filtered list of test cases.

  This is done synchronously.
  """
  try:
    # List all the test cases if a whitelist is used.
    tests = chromium_list_test_cases(
        cmd,
        cwd,
        index=index,
        shards=shards,
        seed=seed,
        disabled=disabled,
        fails=fails,
        flaky=flaky,
        pre=False,
        manual=manual)
  except Failure, e:
    print('Failed to list test cases. This means the test executable is so '
        'broken that it failed to start and enumerate its test cases.\n\n'
        'An example of a potential problem causing this is a Windows API '
        'function not available on this version of Windows.')
    print(e.args[0])
    return None

  if shards:
    # This is necessary for Swarm log parsing.
    print('Note: This is test shard %d of %d.' % (index+1, shards))

  # Filters the test cases with the two lists.
  if blacklist:
    tests = [
      t for t in tests if not any(fnmatch.fnmatch(t, s) for s in blacklist)
    ]
  if whitelist:
    tests = [
      t for t in tests if any(fnmatch.fnmatch(t, s) for s in whitelist)
    ]
  logging.info('Found %d test cases in %s' % (len(tests), ' '.join(cmd)))
  return tests


def dump_results_as_json(result_file, results):
  """Write the results out to a json file."""
  base_path = os.path.dirname(result_file)
  if base_path and not os.path.isdir(base_path):
    os.makedirs(base_path)
  with open(result_file, 'wb') as f:
    json.dump(results, f, sort_keys=True, indent=2)


def dump_results_as_xml(gtest_output, results, now):
  """Write the results out to a xml file in google-test compatible format."""
  # TODO(maruel): Print all the test cases, including the ones that weren't run
  # and the retries.
  test_suites = {}
  for test_case, result in results['test_cases'].iteritems():
    suite, case = test_case.split('.', 1)
    test_suites.setdefault(suite, {})[case] = result[0]

  with open(gtest_output, 'wb') as f:
    # Sanity warning: hand-rolling XML. What could possibly go wrong?
    f.write('<?xml version="1.0" ?>\n')
    # TODO(maruel): File the fields nobody reads anyway.
    # disabled="%d" errors="%d" failures="%d"
    f.write(
        ('<testsuites name="AllTests" tests="%d" time="%f" timestamp="%s">\n')
        % (results['expected'], results['duration'], now))
    for suite_name, suite in test_suites.iteritems():
      # TODO(maruel): disabled="0" errors="0" failures="0" time="0"
      f.write('<testsuite name="%s" tests="%d">\n' % (suite_name, len(suite)))
      for case_name, case in suite.iteritems():
        if case['returncode'] == 0:
          f.write(
            '  <testcase classname="%s" name="%s" status="run" time="%f"/>\n' %
            (suite_name, case_name, case['duration']))
        else:
          f.write(
            '  <testcase classname="%s" name="%s" status="run" time="%f">\n' %
            (suite_name, case_name, (case['duration'] or 0)))
          # While at it, hand-roll CDATA escaping too.
          output = ']]><![CDATA['.join((case['output'] or '').split(']]>'))
          # TODO(maruel): message="" type=""
          f.write('<failure><![CDATA[%s]]></failure></testcase>\n' % output)
      f.write('</testsuite>\n')
    f.write('</testsuites>')


def append_gtest_output_to_xml(final_xml, filepath):
  """Combines the shard xml file with the final xml file."""
  try:
    with open(filepath) as shard_xml_file:
      shard_xml = minidom.parse(shard_xml_file)
  except xml.parsers.expat.ExpatError as e:
    logging.error('Failed to parse %s: %s', filepath, e)
    return final_xml
  except IOError as e:
    logging.error('Failed to load %s: %s', filepath, e)
    # If the shard crashed, gtest will not have generated an xml file.
    return final_xml

  if not final_xml:
    # Out final xml is empty, let's prepopulate it with the first one we see.
    return shard_xml

  final_testsuites_by_name = dict(
      (suite.getAttribute('name'), suite)
      for suite in final_xml.documentElement.getElementsByTagName('testsuite'))

  for testcase in shard_xml.documentElement.getElementsByTagName('testcase'):
    # Don't bother updating the final xml if there is no data.
    status = testcase.getAttribute('status')
    if status == 'notrun':
      continue

    name = testcase.getAttribute('name')
    # Look in our final xml to see if it's there.
    to_remove = []
    final_testsuite = final_testsuites_by_name[
        testcase.getAttribute('classname')]
    for final_testcase in final_testsuite.getElementsByTagName('testcase'):
      # Trim all the notrun testcase instances to add the new instance there.
      # This is to make sure it works properly in case of a testcase being run
      # multiple times.
      if (final_testcase.getAttribute('name') == name and
          final_testcase.getAttribute('status') == 'notrun'):
        to_remove.append(final_testcase)

    for item in to_remove:
      final_testsuite.removeChild(item)
    # Reparent the XML node.
    final_testsuite.appendChild(testcase)

  return final_xml


def running_serial_warning():
  return ['*****************************************************',
          '*****************************************************',
          '*****************************************************',
          'WARNING: The remaining tests are going to be retried',
          'serially. All tests should be isolated and be able to pass',
          'regardless of what else is running.',
          'If you see a test that can only pass serially, that test is',
          'probably broken and should be fixed.',
          '*****************************************************',
          '*****************************************************',
          '*****************************************************']


def gen_gtest_output_dir(cwd, gtest_output):
  """Converts gtest_output to an actual path that can be used in parallel.

  Returns a 'corrected' gtest_output value.
  """
  if not gtest_output.startswith('xml'):
    raise Failure('Can\'t parse --gtest_output=%s' % gtest_output)
  # Figure out the result filepath in case we can't parse it, it'd be
  # annoying to error out *after* running the tests.
  if gtest_output == 'xml':
    gtest_output = os.path.join(cwd, 'test_detail.xml')
  else:
    match = re.match(r'xml\:(.+)', gtest_output)
    if not match:
      raise Failure('Can\'t parse --gtest_output=%s' % gtest_output)
    # If match.group(1) is an absolute path, os.path.join() will do the right
    # thing.
    if match.group(1).endswith((os.path.sep, '/')):
      gtest_output = os.path.join(cwd, match.group(1), 'test_detail.xml')
    else:
      gtest_output = os.path.join(cwd, match.group(1))

  base_path = os.path.dirname(gtest_output)
  if base_path and not os.path.isdir(base_path):
    os.makedirs(base_path)

  # Emulate google-test' automatic increasing index number.
  while True:
    try:
      # Creates a file exclusively.
      os.close(os.open(gtest_output, os.O_CREAT|os.O_EXCL|os.O_RDWR, 0666))
      # It worked, we are done.
      return gtest_output
    except OSError:
      pass
    logging.debug('%s existed', gtest_output)
    base, ext = os.path.splitext(gtest_output)
    match = re.match(r'^(.+?_)(\d+)$', base)
    if match:
      base = match.group(1) + str(int(match.group(2)) + 1)
    else:
      base = base + '_0'
    gtest_output = base + ext


def calc_cluster_default(num_test_cases, jobs):
  """Calculates a desired number for clusters depending on the number of test
  cases and parallel jobs.
  """
  if not num_test_cases:
    return 0
  chunks = 6 * jobs
  if chunks >= num_test_cases:
    # Too many chunks, use 1~5 test case per thread. Not enough to start
    # chunking.
    value = num_test_cases / jobs
  else:
    # Use chunks that are spread across threads.
    value = (num_test_cases + chunks - 1) / chunks
  # Limit to 10 test cases per cluster.
  return min(10, max(1, value))


def run_test_cases(
    cmd, cwd, test_cases, jobs, timeout, clusters, retries, run_all,
    max_failures, no_cr, gtest_output, result_file, verbose):
  """Runs test cases in parallel.

  Arguments:
    - cmd: command to run.
    - cwd: working directory.
    - test_cases: list of preprocessed test cases to run.
    - jobs: number of parallel execution threads to do.
    - timeout: individual test case timeout. Modulated when used with
      clustering.
    - clusters: number of test cases to lump together in a single execution. 0
      means the default automatic value which depends on len(test_cases) and
      jobs. Capped to len(test_cases) / jobs.
    - retries: number of times a test case can be retried.
    - run_all: If true, do not early return even if all test cases fail.
    - max_failures is the absolute maximum number of tolerated failures or None.
    - no_cr: makes output friendly to piped logs.
    - gtest_output: saves results as xml.
    - result_file: saves results as json.
    - verbose: print more details.

  It may run a subset of the test cases if too many test cases failed, as
  determined with max_failures, retries and run_all.
  """
  assert 0 <= retries <= 100000
  if not test_cases:
    return 0
  if run_all:
    decider = RunAll()
  else:
    # If 10% of test cases fail, just too bad.
    decider = RunSome(len(test_cases), retries, 2, 0.1, max_failures)

  if not clusters:
    clusters = calc_cluster_default(len(test_cases), jobs)
  else:
    # Limit the value.
    clusters = max(min(clusters, len(test_cases) / jobs), 1)

  logging.debug('%d test cases with clusters of %d', len(test_cases), clusters)

  if gtest_output:
    gtest_output = gen_gtest_output_dir(cwd, gtest_output)
  columns = [('index', 0), ('size', len(test_cases))]
  progress = threading_utils.Progress(columns)
  progress.use_cr_only = not no_cr
  serial_tasks = threading_utils.QueueWithProgress(progress)

  def add_serial_task(priority, func, *args, **kwargs):
    """Adds a serial task, to be executed later."""
    assert isinstance(priority, int)
    assert callable(func)
    serial_tasks.put((priority, func, args, kwargs))

  with threading_utils.ThreadPoolWithProgress(
      progress, jobs, jobs, len(test_cases)) as pool:
    runner = ChromiumGoogleTestRunner(
        cmd,
        cwd,
        timeout,
        progress,
        retries,
        decider,
        verbose,
        pool.add_task,
        add_serial_task)
    function = runner.map
    # Cluster the test cases right away.
    for i in xrange((len(test_cases) + clusters - 1) / clusters):
      cluster = test_cases[i*clusters : (i+1)*clusters]
      pool.add_task(i, function, i, cluster, 0)
    results = pool.join()

    # Retry any failed tests serially.
    if not serial_tasks.empty():
      progress.update_item('\n'.join(running_serial_warning()), raw=True)
      progress.print_update()

      while not serial_tasks.empty():
        _priority, func, args, kwargs = serial_tasks.get()
        for out in func(*args, **kwargs):
          results.append(out)
        serial_tasks.task_done()
        progress.print_update()

      # Call join since that is a standard call once a queue has been emptied.
      serial_tasks.join()

    duration = time.time() - pool.tasks.progress.start

  cleaned = {}
  for i in results:
    cleaned.setdefault(i['test_case'], []).append(i)
  results = cleaned

  # Total time taken to run each test case.
  test_case_duration = dict(
      (test_case, sum((i.get('duration') or 0) for i in item))
      for test_case, item in results.iteritems())

  # Classify the results
  success = []
  flaky = []
  fail = []
  nb_runs = 0
  for test_case in sorted(results):
    items = results[test_case]
    nb_runs += len(items)
    if not any(i['returncode'] == 0 for i in items):
      fail.append(test_case)
    elif len(items) > 1 and any(i['returncode'] == 0 for i in items):
      flaky.append(test_case)
    elif len(items) == 1 and items[0]['returncode'] == 0:
      success.append(test_case)
    else:
      # The test never ran.
      assert False, items
  missing = sorted(set(test_cases) - set(success) - set(flaky) - set(fail))

  saved = {
    'test_cases': results,
    'expected': len(test_cases),
    'success': success,
    'flaky': flaky,
    'fail': fail,
    'missing': missing,
    'duration': duration,
  }
  if result_file:
    dump_results_as_json(result_file, saved)
  if gtest_output:
    dump_results_as_xml(gtest_output, saved, datetime.datetime.now())
  sys.stdout.write('\n')
  if not results:
    return 1

  if flaky:
    print('Flaky tests:')
    for test_case in sorted(flaky):
      items = results[test_case]
      print('  %s (tried %d times)' % (test_case, len(items)))

  if fail:
    print('Failed tests:')
    for test_case in sorted(fail):
      print('  %s' % test_case)

  if not decider.should_stop() and missing:
    print('Missing tests:')
    for test_case in sorted(missing):
      print('  %s' % test_case)

  print('Summary:')
  if decider.should_stop():
    print('  ** STOPPED EARLY due to high failure rate **')
  output = [
    ('Success', success),
    ('Flaky', flaky),
    ('Fail', fail),
  ]
  if missing:
    output.append(('Missing', missing))
  total_expected = len(test_cases)
  for name, items in output:
    number = len(items)
    print(
        '  %7s: %4d %6.2f%% %7.2fs' % (
          name,
          number,
          number * 100. / total_expected,
          sum(test_case_duration.get(item, 0) for item in items)))
  print('  %.2fs Done running %d tests with %d executions. %.2f test/s' % (
      duration,
      len(results),
      nb_runs,
      nb_runs / duration if duration else 0))
  return int(bool(fail) or decider.stopped or bool(missing))


class OptionParserWithLogging(tools.OptionParserWithLogging):
  def __init__(self, **kwargs):
    tools.OptionParserWithLogging.__init__(
        self,
        log_file=os.environ.get('RUN_TEST_CASES_LOG_FILE', ''),
        **kwargs)


class OptionParserWithTestSharding(OptionParserWithLogging):
  """Adds automatic handling of test sharding"""
  def __init__(self, **kwargs):
    OptionParserWithLogging.__init__(self, **kwargs)

    def as_digit(variable, default):
      return int(variable) if variable.isdigit() else default

    group = optparse.OptionGroup(self, 'Which shard to select')
    group.add_option(
        '-I', '--index',
        type='int',
        default=as_digit(os.environ.get('GTEST_SHARD_INDEX', ''), None),
        help='Shard index to select')
    group.add_option(
        '-S', '--shards',
        type='int',
        default=as_digit(os.environ.get('GTEST_TOTAL_SHARDS', ''), None),
        help='Total number of shards to calculate from the --index to select')
    self.add_option_group(group)

  def parse_args(self, *args, **kwargs):
    options, args = OptionParserWithLogging.parse_args(self, *args, **kwargs)
    if bool(options.shards) != bool(options.index is not None):
      self.error('Use both --index X --shards Y or none of them')
    return options, args


class OptionParserWithTestShardingAndFiltering(OptionParserWithTestSharding):
  """Adds automatic handling of test sharding and filtering."""
  def __init__(self, *args, **kwargs):
    OptionParserWithTestSharding.__init__(self, *args, **kwargs)

    group = optparse.OptionGroup(self, 'Which test cases to select')
    group.add_option(
        '-w', '--whitelist',
        default=[],
        action='append',
        help='filter to apply to test cases to run, wildcard-style, defaults '
        'to all test')
    group.add_option(
        '-b', '--blacklist',
        default=[],
        action='append',
        help='filter to apply to test cases to skip, wildcard-style, defaults '
        'to no test')
    group.add_option(
        '-T', '--test-case-file',
        help='File containing the exact list of test cases to run')
    group.add_option(
        '--gtest_filter',
        default=os.environ.get('GTEST_FILTER', ''),
        help='Select test cases like google-test does, separated with ":"')
    group.add_option(
        '--seed',
        type='int',
        default=os.environ.get('GTEST_RANDOM_SEED', '1'),
        help='Deterministically shuffle the test list if non-0. default: '
             '%default')
    group.add_option(
        '-d', '--disabled',
        action='store_true',
        default=int(os.environ.get('GTEST_ALSO_RUN_DISABLED_TESTS', '0')),
        help='Include DISABLED_ tests')
    group.add_option(
        '--gtest_also_run_disabled_tests',
        action='store_true',
        dest='disabled',
        help='same as --disabled')
    self.add_option_group(group)

    group = optparse.OptionGroup(
        self, 'Which test cases to select; chromium-specific')
    group.add_option(
        '-f', '--fails',
        action='store_true',
        help='Include FAILS_ tests')
    group.add_option(
        '-F', '--flaky',
        action='store_true',
        help='Include FLAKY_ tests')
    group.add_option(
        '-m', '--manual',
        action='store_true',
        help='Include MANUAL_ tests')
    group.add_option(
        '--run-manual',
        action='store_true',
        dest='manual',
        help='same as --manual')
    self.add_option_group(group)

  def parse_args(self, *args, **kwargs):
    options, args = OptionParserWithTestSharding.parse_args(
        self, *args, **kwargs)

    if options.gtest_filter:
      # Override any other option.
      # Based on UnitTestOptions::FilterMatchesTest() in
      # http://code.google.com/p/googletest/source/browse/#svn%2Ftrunk%2Fsrc
      if '-' in options.gtest_filter:
        options.whitelist, options.blacklist = options.gtest_filter.split('-',
                                                                          1)
      else:
        options.whitelist = options.gtest_filter
        options.blacklist = ''
      options.whitelist = [i for i in options.whitelist.split(':') if i]
      options.blacklist = [i for i in options.blacklist.split(':') if i]

    return options, args

  @staticmethod
  def process_gtest_options(cmd, cwd, options):
    """Grabs the test cases."""
    if options.test_case_file:
      with open(options.test_case_file, 'r') as f:
        # Do not shuffle or alter the file in any way in that case except to
        # strip whitespaces.
        return [l for l in (l.strip() for l in f) if l]
    else:
      return get_test_cases(
          cmd,
          cwd,
          options.whitelist,
          options.blacklist,
          options.index,
          options.shards,
          options.seed,
          options.disabled,
          options.fails,
          options.flaky,
          options.manual)


class OptionParserTestCases(OptionParserWithTestShardingAndFiltering):
  def __init__(self, *args, **kwargs):
    OptionParserWithTestShardingAndFiltering.__init__(self, *args, **kwargs)
    self.add_option(
        '-j', '--jobs',
        type='int',
        default=threading_utils.num_processors(),
        help='Number of parallel jobs; default=%default')
    self.add_option(
        '--use-less-jobs',
        action='store_const',
        const=max(1, threading_utils.num_processors() / 2),
        dest='jobs',
        help='Starts less parallel jobs than the default, used to help reduce'
             'contention between threads if all the tests are very CPU heavy.')
    self.add_option(
        '-t', '--timeout',
        type='int',
        default=75,
        help='Timeout for a single test case, in seconds default:%default')
    self.add_option(
        '--clusters',
        type='int',
        help='Number of test cases to cluster together, clamped to '
             'len(test_cases) / jobs; the default is automatic')


def process_args(argv):
  parser = OptionParserTestCases(
      usage='%prog <options> [gtest]',
      verbose=int(os.environ.get('ISOLATE_DEBUG', 0)))
  parser.add_option(
      '--run-all',
      action='store_true',
      help='Do not fail early when a large number of test cases fail')
  parser.add_option(
      '--max-failures', type='int',
      help='Limit the number of failures before aborting')
  parser.add_option(
      '--retries', type='int', default=2,
      help='Number of times each test case should be retried in case of '
           'failure.')
  parser.add_option(
      '--no-dump',
      action='store_true',
      help='do not generate a .run_test_cases file')
  parser.add_option(
      '--no-cr',
      action='store_true',
      help='Use LF instead of CR for status progress')
  parser.add_option(
      '--result',
      help='Override the default name of the generated .run_test_cases file')

  group = optparse.OptionGroup(parser, 'google-test compability flags')
  group.add_option(
      '--gtest_list_tests',
      action='store_true',
      help='List all the test cases unformatted. Keeps compatibility with the '
           'executable itself.')
  group.add_option(
      '--gtest_output',
      default=os.environ.get('GTEST_OUTPUT', ''),
      help='XML output to generate')
  parser.add_option_group(group)

  options, args = parser.parse_args(argv)

  if not args:
    parser.error(
        'Please provide the executable line to run, if you need fancy things '
        'like xvfb, start this script from *inside* xvfb, it\'ll be much faster'
        '.')

  if options.run_all and options.max_failures is not None:
    parser.error('Use only one of --run-all or --max-failures')
  return parser, options, tools.fix_python_path(args)


def main(argv):
  """CLI frontend to validate arguments."""
  tools.disable_buffering()
  parser, options, cmd = process_args(argv)

  if options.gtest_list_tests:
    # Special case, return the output of the target unmodified.
    return subprocess42.call(cmd + ['--gtest_list_tests'])

  cwd = os.getcwd()
  test_cases = parser.process_gtest_options(cmd, cwd, options)

  if options.no_dump:
    result_file = None
  else:
    result_file = options.result
    if not result_file:
      if cmd[0] == sys.executable:
        result_file = '%s.run_test_cases' % cmd[1]
      else:
        result_file = '%s.run_test_cases' % cmd[0]

  if not test_cases:
    # The fact of not running any test is considered a failure. This is to
    # prevent silent failure with an invalid --gtest_filter argument or because
    # of a misconfigured unit test.
    if test_cases is not None:
      print('Found no test to run')
    if result_file:
      dump_results_as_json(result_file, {
        'test_cases': [],
        'expected': 0,
        'success': [],
        'flaky': [],
        'fail': [],
        'missing': [],
        'duration': 0,
      })
    return 1

  if options.disabled:
    cmd.append('--gtest_also_run_disabled_tests')
  if options.manual:
    cmd.append('--run-manual')

  try:
    return run_test_cases(
        cmd,
        cwd,
        test_cases,
        options.jobs,
        options.timeout,
        options.clusters,
        options.retries,
        options.run_all,
        options.max_failures,
        options.no_cr,
        options.gtest_output,
        result_file,
        options.verbose)
  except Failure as e:
    print >> sys.stderr, e.args[0]
    return 1


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
