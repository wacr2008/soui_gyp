
{
  'target_defaults': {
    'defines': [
      '_CRT_SECURE_NO_WARNINGS',
    ],
    'sources': [
       #include files	
       'disasm-lib/cpu.h',
			 'disasm-lib/disasm.h',
			 'disasm-lib/disasm_x86.h',
			 'disasm-lib/disasm_x86_tables.h',
			 'disasm-lib/misc.h',
			 'mhook-lib/mhook.h',
			
			 #source files 
			'disasm-lib/cpu.c',
			'disasm-lib/disasm.c',
			'disasm-lib/disasm_x86.c',
			'disasm-lib/misc.c',
			'mhook-lib/mhook.cpp',

    ],
    'include_dirs': [ 
      '.',
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
