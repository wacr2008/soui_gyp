
{  
  'includes': [
    '../../../build/win_precompile.gypi',
    'render-skia.gypi',
  ],
  'targets': [
    {
      'target_name': 'render-skia',
      'type': '<(component)',
      'includes': [ '../../build/common.gypi', ],  
      'dependencies': [ 
      	'<(app_root)/utilities/utilities.gyp:*',
      	'<(app_root)/third-part/skia/skia.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
