
{
  'target_defaults': {
    'conditions': 
    [
        ['component=="shared_library"', 
	      {
	          'sources': [ 'translator.rc',],
	      }, 
	      {
	          'defines': [],
	      }],
    ],
    'sources': [
      #include files	
      'translator.h',
      'targetver.h',
			
			#source files 
			'dllmain.cpp',
			'translator.cpp',
    ],
    'include_dirs': [ 
      '.',
      '../../config',
			'../../utilities/include',
			'../../SOUI/include',
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
