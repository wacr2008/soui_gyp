
{
  'target_defaults': { 
    'sources': [
      #include files			
			'resource.h',
			'MainDlg.h',
			'Switch/SSwitch.h',
			'Toolbox/SToolbox.h',
			
			#source files 
			'PCManager.cpp',
      'MainDlg.cpp',
      'Switch/SSwitch.cpp',
      'Toolbox/SToolbox.cpp',
      'PCManager.rc',

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
