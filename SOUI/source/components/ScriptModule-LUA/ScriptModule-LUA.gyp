
{  
  'includes': [
    '../../../build/win_precompile.gypi',
    'ScriptModule-LUA.gypi',
  ],
  'targets': [
    {
      'target_name': 'ScriptModule-LUA',
      'type': '<(component)',
      'includes': [ '../../build/common.gypi', ],  
      'dependencies': [ 
      	'../../utilities/utilities.gyp:*',
      	'../../third-part/lua-52/lua-52.gyp:*',
      	'../../SOUI/SOUI.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
