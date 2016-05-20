
{
  'target_defaults': {
    'conditions': 
    [
        ['component=="shared_library"', 
	      {
	          'sources': [ 'render-skia.rc',],
	      }, 
	      {
	          'defines': [],
	      }],
    ], 
    'sources': [
      #include files	
      'drawtext-skia.h',
      'render-skia.h',
      'render-skia2-i.h',
      'render-skia2.h',
      'skia2rop2.h',
			
			#source files 
			'drawtext-skia.cpp',
			'render-skia.cpp',
			'render-skia2.cpp',
			'skia2rop2.cpp',

    ],
    'include_dirs': [ 
      '.',
      '../../config',
			'../../soui/include',
			'../../utilities/include',
			'../../third-part/skia',
			'../../third-part/skia/include',
			'../../third-part/skia/include/config',
			'../../third-part/skia/include/core',
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
