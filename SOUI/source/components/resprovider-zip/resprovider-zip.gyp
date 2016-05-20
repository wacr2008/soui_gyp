
{  
  'includes': [
    '../../../build/win_precompile.gypi',
    'resprovider-zip.gypi',
  ],
  'targets': [
    {
      'target_name': 'resprovider-zip',
      'type': '<(component)',
      'includes': [ '../../build/common.gypi', ],  
      'dependencies': [ 
      	'<(DEPTH)/source/utilities/utilities.gyp:*',
      	'<(DEPTH)/source/third-part/zlib/zlib.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
