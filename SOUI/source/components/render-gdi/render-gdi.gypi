
{
  'target_defaults': {
    'conditions': 
    [
        ['component=="shared_library"', 
	      {
	          'sources': [ 'render-gdi.rc',],
	      }, 
	      {
	          'defines': [],
	      }],
    ], 
    'sources': [
      #include files	
      'GradientFillHelper.h',
      'render-gdi.h',
			
			#source files 
			'GradientFillHelper.cpp',
			'render-gdi.cpp',

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
