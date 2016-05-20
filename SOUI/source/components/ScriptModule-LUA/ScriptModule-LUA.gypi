
{
  'target_defaults': {
    'conditions': 
    [
        ['component=="shared_library"', 
	      {
	          'sources': [ 'src/ScriptModule-Lua.rc',],
	      }, 
	      {
	          'defines': [],
	      }],
    ], 
    'defines': [
      'exports',
    ],
    'sources': [
      #include files	
      #'src/require.h',
			'src/ScriptModule-Lua.h',
			'src/exports/exp_app.h',
			'src/exports/exp_Basic.h',
			'src/exports/exp_eventArgs.h',
			'src/exports/exp_hostwnd.h',
			'src/exports/exp_msgbox.h',
			'src/exports/exp_pugixml.h',
			'src/exports/exp_ResProvider.h',
			'src/exports/exp_ScriptModule.h',
			'src/exports/exp_strcpcvt.h',
			'src/exports/exp_string.h',
			'src/exports/exp_Window.h',
			'src/exports/exp_Object.h',
			'src/exports/exp_ctrls.h',
			'lua_tinker/lua_tinker.h',
			
			#source files 
			'src/ScriptModule-Lua.cpp',
      'src/exports/exp_soui.cpp',
      'lua_tinker/lua_tinker.cpp',

    ],
    'include_dirs': [ 
      '.',
      '../../config',
			'./src',
			'../../third-part/lua-52/src',
			'../../soui/include',
			'../../utilities/include',
    ],
    'direct_dependent_settings': {
        'include_dirs': [
          '.',
        ],
    },
    'configurations': {
	      'Debug': {
	        # Specify third party library directory
          'msvs_settings': {
            'VCLinkerTool': {
              "AdditionalLibraryDirectories": [
			          #'../3rd/detours/lib', 
              ],
              'AdditionalDependencies': [
			             'Usp10.lib',
			             'opengl32.lib',
			        ],
              'SubSystem': '2', #/SUBSYSTEM:WINDOWS
            },
          },
	      },
	      'Release': {
	        # Specify third party library directory
          'msvs_settings': {
            'VCLinkerTool': {
              "AdditionalLibraryDirectories": [
			          #'../3rd/detours/lib', 
              ],
              'AdditionalDependencies': [
			             #'Usp10.lib',
			             #'opengl32.lib',
			        ],
              'SubSystem': '2', #/SUBSYSTEM:WINDOWS
            },
          },
	      }
    }, # configurations
  },
}
