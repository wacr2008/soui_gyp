
{
  'target_defaults': {
    'conditions': 
    [
        ['component=="shared_library"', 
	      {
	          'sources': [ 'ResProvider-Zip.rc',],
	      }, 
	      {
	          'defines': [],
	      }],
    ], 
    'defines': [
      'RESPROVIDERZIP_EXPORTS',
    ],
    'sources': [
      #include files	
      'SResProviderZip.h',
      'ZipArchive.h',
			
			#source files 
			'cursoricon.cpp',
			'SResProviderZip.cpp',
			'zipArchive.cpp',

    ],
    'include_dirs': [ 
      '.',
      '../../config',
			'../../third-part/zlib',
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
			             'Usp10.lib',
			             'opengl32.lib',
			        ],
              'SubSystem': '2', #/SUBSYSTEM:WINDOWS
            },
          },
	      }
    }, # configurations
  },
}
