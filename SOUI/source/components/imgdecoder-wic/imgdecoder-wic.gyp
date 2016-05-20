
{  
  'includes': [
    '../../../build/win_precompile.gypi',
    'imgdecoder-wic.gypi',
  ],
  'targets': [
    {
      'target_name': 'imgdecoder-wic',
      'type': '<(component)',
      'includes': [ '../../build/common.gypi', ],  
      'dependencies': [ 
      	'<(DEPTH)/source/third-part/zlib/zlib.gyp:*',
      	'<(DEPTH)/source/third-part/png/png.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
