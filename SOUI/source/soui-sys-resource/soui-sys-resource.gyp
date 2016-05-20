
{  
  'includes': [
    '../../build/win_precompile.gypi',
    'soui-sys-resource.gypi',
  ],
  'targets': [
    {
      'target_name': 'soui-sys-resource',
      'type': 'shared_library',
      'includes': [ '../build/common.gypi', ],  
      'dependencies': [ 
      	'<(app_root)/utilities/utilities.gyp:*',
      	#'<(app_root)/third-part/png/png.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
