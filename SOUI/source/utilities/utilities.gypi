
{
  'target_defaults': {
    'conditions': 
    [
        ['component=="shared_library"', 
	      {
	          'defines': ['UTILITIES_EXPORTS',],
	          'sources': [ 'utilities.rc',],
	      }, 
	      {
	          'defines': [],
	      }],
    ], 
    'sources': [
      #include files
      'include/gdialpha.h',
			'include/souicoll.h',
			'include/trace.h',
			'include/snew.h',
			'include/utilities-def.h',
			'include/utilities.h',
			'include/soui_mem_wrapper.h',
			'include/atl.mini/atldef.h',
			'include/atl.mini/SComCli.h',
			'include/atl.mini/SComHelper.h',
			'include/pugixml/pugiconfig.hpp',
			'include/pugixml/pugixml.hpp',
			'include/string/strcpcvt.h',
			'include/string/tstring.h',
			'include/unknown/obj-ref-i.h',
			'include/unknown/obj-ref-impl.hpp',
			'include/com-loader.hpp',
			'include/wtl.mini/msgcrack.h',
			'include/wtl.mini/souimisc.h',
			
			#source files 
			'src/gdialpha.cpp',
			'src/trace.cpp',
			'src/utilities.cpp',
			'src/soui_mem_wrapper.cpp',
			'src/pugixml/pugixml.cpp',
			'src/string/strcpcvt.cpp',
			'src/string/tstring.cpp',

    ],
    'include_dirs': [
      'include/',
      '../config/',
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
              'SubSystem': '2', #/SUBSYSTEM:WINDOWS
            },
          },
	      }
    }, # configurations
  },
}
