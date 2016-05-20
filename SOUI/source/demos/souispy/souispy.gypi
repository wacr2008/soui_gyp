
{
  'target_defaults': {
   
    'sources': [
      #include files			
			'MainDlg.h',
			'resource.h',
			'SCaptureButton.h',
			'SwndFrame.h',
			
			#source files 
			'MainDlg.cpp',
      'SCaptureButton.cpp',
      'souispy.cpp',
      'SwndFrame.cpp',
      
      'souispy.rc',

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
