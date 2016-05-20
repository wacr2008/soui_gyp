
{
  'target_defaults': {
    'defines': [
      '_CRT_SECURE_NO_WARNINGS',
    ],
    'sources': [
        #include files	
        'png.h',
				'pngconf.h',
				'pngdebug.h',
				'pnginfo.h',
				'pnglibconf.h',
				'pngpriv.h',
				'pngstruct.h',
			
			  #source files 
				'png.c',
				'pngerror.c',
				'pngget.c',
				'pngmem.c',
				'pngpread.c',
				'pngread.c',
				'pngrio.c',
				'pngrtran.c',
				'pngrutil.c',
				'pngset.c',
				'pngtrans.c',
				'pngwio.c',
				'pngwrite.c',
				'pngwtran.c',
				'pngwutil.c',

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
