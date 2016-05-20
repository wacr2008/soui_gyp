
{  
  'includes': [
    '../../../build/win_precompile.gypi',
    'lua-52.gypi',
  ],
  'targets': [
    {
      'target_name': 'lua-52',
      'type': 'static_library',
      'includes': [ '../../build/common.gypi', ],  
      'dependencies': [ 
      	'../../utilities/utilities.gyp:*',
      	#'../../third-part/png/png.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
