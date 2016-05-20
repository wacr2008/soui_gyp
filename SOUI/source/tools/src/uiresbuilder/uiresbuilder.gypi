
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
      'tinyxml/tinystr.h',
			'tinyxml/tinyxml.h',
			'XGetopt.h',
			
			#source files  
			'tinyxml/tinystr.cpp',
			'tinyxml/tinyxml.cpp',
			'tinyxml/tinyxmlerror.cpp',
			'tinyxml/tinyxmlparser.cpp',
			'residbuilder.cpp',
			'XGetopt.cpp',

    ],
    'include_dirs': [
      'tinyxml/',
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
          'msvs_configuration_attributes': {
	          'CharacterSet': '0',
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
          'msvs_configuration_attributes': {
	          'CharacterSet': '0',
	        },
	      }
    }, # configurations
  },
}
