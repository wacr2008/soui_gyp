
{
  'target_defaults': {
    'conditions': 
    [
        ['component=="shared_library"', 
	      {
	          'sources': [ 'imgdecoder-gdip.rc',],
	      }, 
	      {
	          'defines': [],
	      }],
    ],  
    'sources': [
      #include files			
			'imgdecoder-gdip.h',
			
			#source files 
			'imgdecoder-gdip.cpp',

    ],
    'include_dirs': [ 
      '.',
      '../../config',
			'../../third-part/zlib',
			'../../third-part/png',
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
