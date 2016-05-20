
{
  'target_defaults': {
    'defines': [
       
    ],
    'sources': [
      
      '2UnicodeHandler.h',
			'CalcMd5Handler.h',
			'CodeLineCounter.h',
			'CodeLineCounterHandler.h',
			'droptarget.h',
			'FolderHander.h',
			'FolderScanHandler.h',
			'ImageMergerHandler.h',
			'MainDlg.h',
			'MD5.h',
			'resource.h',
			'SEdit2.h',
			'SFolderList.h',
			'SImgCanvas.h',
			'STreeList.h',
			'2UnicodeHandler.cpp',
			'CalcMd5Handler.cpp',
			'CodeLineCounter.cpp',
			'CodeLineCounterHandler.cpp',
			'FolderHander.cpp',
			'FolderScanHandler.cpp',
			'ImageMergerHandler.cpp',
			'MainDlg.cpp',
			'MD5.cpp',
			'SEdit2.cpp',
			'SFolderList.cpp',
			'SImgCanvas.cpp',
			'SoTool.cpp',
			'STreeList.cpp',
			
			'SoTool.rc',

    ],
    'include_dirs': [ 
      '.',
      '../../config',
      '../../controls.extend',
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
