
{
  'target_defaults': {
    'defines': [
       
    ],
    'sources': [
      
      'MainDlg.h',
      'resource.h',
      'SToolbox.h',
      'SImageSwitcher.h',
      
      '360Preview.cpp',
      'MainDlg.cpp',
      'SToolbox.cpp',
      'SImageSwitcher.cpp',
      
      '360Preview.rc',

    ],
    'include_dirs': [ 
      '.',
      '../../config',
			'../../utilities/include',
			'../../soui/include',
			'../../components',
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
