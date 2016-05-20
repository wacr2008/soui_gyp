
{
  'target_defaults': {
    'defines': [
      '_CRT_SECURE_NO_WARNINGS',
    ],
    'sources': [
        #include files	
        'crc32.h',
				'deflate.h',
				'inffast.h',
				'inffixed.h',
				'inflate.h',
				'inftrees.h',
				'trees.h',
				'zconf.h',
				'zconf.in.h',
				'zlib.h',
				'zutil.h',
				
				#source files
				'adler32.c',
				'compress.c',
				'crc32.c',
				'deflate.c',
				'gzio.c',
				'infback.c',
				'inffast.c',
				'inflate.c',
				'inftrees.c',
				'trees.c',
				'uncompr.c',
				'zutil.c',

    ],
    'include_dirs': [ 
      '.',
			'../zlib',
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
