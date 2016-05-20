
{  
  'includes': [
    '../../build/win_precompile.gypi',
    'utilities.gypi',
  ],
  'targets': [
    {
      'target_name': 'utilities',
      'type': '<(component)',
      'includes': [ '../build/common.gypi', ],  
      'dependencies': [  ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
