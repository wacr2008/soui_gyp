
{
  'target_defaults': {
    'defines': [
       
    ],
    'sources': [
      
      'MainDlg.h',
			'FormatMsgDlg.h',
			'resource.h',
			'wtlhelper/whwindow.h',
			'../../controls.extend/SWkeWebkit.h',
			'../../controls.extend/gif/SAniImgFrame.h',
			'../../controls.extend/gif/SGifPlayer.h',
			'../../controls.extend/gif/SSkinGif.h',
			'../../controls.extend/gif/SSkinAPNG.h',
			'../../controls.extend/SSkinImgFrame2.h',
			'../../controls.extend/FileHelper.h',
			'../../controls.extend/sipaddressctrl.h',
			'../../controls.extend/propgrid/SPropertyGrid.h',
			'../../controls.extend/sflywnd.h',
			'../../controls.extend/sfadeframe.h',
			'../../controls.extend/sradiobox2.h',
			'../../controls.extend/SChromeTabCtrl.h',
			'../../controls.extend/siectrl.h',
			'../../controls.extend/schatedit.h',
			'../../controls.extend/reole/richeditole.h',
			'../../controls.extend/reole/dataobject.h',
			'../../controls.extend/sscrolltext.h',
			'../../controls.extend/scalendar2.h',
			'../../controls.extend/slistctrlex.h',
			'../../controls.extend/simagemaskwnd.h',
			'../../controls.extend/SRatingBar.h',
			'../../controls.extend/SFreeMoveWindow.h',
			'../../controls.extend/smiley/SSmileyCtrl.h',
			'httpsvr/filereader-i.h',
			'httpsvr/genericserver.h',
			'httpsvr/httpserver.h',
			'magnet/magnetframe.h',
			'smatrixwindow.h',
			'memflash.h',
			'setskinwnd.h',
			'SmileyCreateHook.h',
			'uianimation/uianimation.h',
			'uianimation/uianimationwnd.h',
			'appledock/sdesktopdock.h',
			'clock/sclock.h',
			'demo.cpp',
			'MainDlg.cpp',
			'FormatMsgDlg.cpp',
			'../../controls.extend/SWkeWebkit.cpp',
			'../../controls.extend/gif/SGifPlayer.cpp',
			'../../controls.extend/gif/SSkinGif.cpp',
			'../../controls.extend/gif/SSkinAPNG.cpp',
			'../../controls.extend/SSkinImgFrame2.cpp',
			'../../controls.extend/sipaddressctrl.cpp',
			'../../controls.extend/propgrid/spropertygrid.cpp',
			'../../controls.extend/propgrid/spropertyitembase.cpp',
			'../../controls.extend/propgrid/propitem/spropertyitem-text.cpp',
			'../../controls.extend/propgrid/propitem/spropertyitem-option.cpp',
			'../../controls.extend/propgrid/propitem/spropertyitem-color.cpp',
			'../../controls.extend/propgrid/propitem/spropertyitem-size.cpp',
			'../../controls.extend/sflywnd.cpp',
			'../../controls.extend/sfadeframe.cpp',
			'../../controls.extend/sradiobox2.cpp',
			'../../controls.extend/SChromeTabCtrl.cpp',
			'../../controls.extend/siectrl.cpp',
			'../../controls.extend/schatedit.cpp',
			'../../controls.extend/reole/richeditole.cpp',
			'../../controls.extend/reole/dataobject.cpp',
			'../../controls.extend/sscrolltext.cpp',
			'../../controls.extend/scalendar2.cpp',
			'../../controls.extend/slistctrlex.cpp',
			'../../controls.extend/simagemaskwnd.cpp',
			'../../controls.extend/SRatingBar.cpp',
			'../../controls.extend/SFreeMoveWindow.cpp',
			'httpsvr/genericserver.cpp',
			'httpsvr/httpserver.cpp',
			'magnet/magnetframe.cpp',
			'memflash.cpp',
			'smatrixwindow.cpp',
			'setskinwnd.cpp',
			'SmileyCreateHook.cpp',
			'uianimation/uianimationwnd.cpp',
			'appledock/sdesktopdock.cpp',
			'clock/sclock.cpp',
			
			'demo.rc',

    ],
    'include_dirs': [ 
      '.',
      '../../config',
			'../../utilities/include',
			'../../soui/include',
			'../../third-part/wke/include',
			'../../third-part/mhook/mhook-lib',
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
