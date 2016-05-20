
{  
  'includes': [
    '../../../build/win_precompile.gypi',
    'render-gdi.gypi',
  ],
  'targets': [
    {
      'target_name': 'render-gdi',
      'type': '<(component)',
      'includes': [ '../../build/common.gypi', ],  
      'dependencies': [ 
      	'<(app_root)/utilities/utilities.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
