
{
  'target_defaults': {
    'defines': [
       '_CONSOLE',
    ],
    'defines!':
    [
    	'_WINDOWS',
    ],
    'sources': [
      #include files
      'pugixml/pugiconfig.hpp',
			'XGetopt.h',
			
			#source files  
			'pugixml/pugixml.cpp',
			'pugixml/pugixml.cpp',
			'uiresImporter.cpp',
			'XGetopt.cpp',

    ],
    'include_dirs': [
      'pugixml/',
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
			              #'utilities.lib'
			        ],
              'SubSystem': '1', #/SUBSYSTEM:WINDOWS
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
			             #'utilities.lib'
			        ],
              'SubSystem': '1', #/SUBSYSTEM:WINDOWS
            },
          },
	      }
    }, # configurations
  },
}
