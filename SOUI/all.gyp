{
	  'variables': {
	    'app_root%': '<(DEPTH)',  
	  },
	   
    
    'targets':
    [ 
        {
            'target_name': 'gen_demo_resource',
            'type': 'none',
            'includes': [ 'source/build/common.gypi', ],
            'hard_dependency': 1,
            'actions':
            [ 
   							{
                    'action_name': 'APP pre-Build Script 360 resource',
                    'message': 'APP pre-Build Script 360 resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                    		'<(app_root)/source/demos/360demo/gen.out', 
                    ],
                    'action':
                    [
                       '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/360demo/uires/uires.idx -p uires -r ./res/soui_res.rc2 -h ./res/R.h idtable ',
                    ],
                },
                
                {
                    'action_name': 'APP pre-Build Script 360Preview resource',
                    'message': 'APP pre-Build Script 360Preview resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                        '<(app_root)/source/demos/360Preview/gen.out', 
                    ],
                    'action':
                    [
                        '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/360Preview/uires/uires.idx -p uires -r ./res/360Preview.rc2 -h ./res/R.h idtable ', 
                    ],
                }, 
                
                {
                    'action_name': 'APP pre-Build Script demo resource',
                    'message': 'APP pre-Build Script demo resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                        '<(app_root)/source/demos/demo/gen.out', 
                    ],
                    'action':
                    [
                        '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/demo/uires/uires.idx -p uires -r ./res/demo.rc2 -h ./res/R.h idtable ', 
                    ],
                }, 
                
                {
                    'action_name': 'APP pre-Build Script mclistview_demo resource',
                    'message': 'APP pre-Build Script mclistview_demo resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                        '<(app_root)/source/demos/mclistview_demo/gen.out', 
                    ],
                    'action':
                    [
                        '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/mclistview_demo/uires/uires.idx -p uires -r ./res/mclistview_demo.rc2 -h ./res/R.h idtable ', 
                    ],
                }, 
                
                {
                    'action_name': 'APP pre-Build Script PCManager resource',
                    'message': 'APP pre-Build Script PCManager resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                        '<(app_root)/source/demos/PCManager/gen.out', 
                    ],
                    'action':
                    [
                        '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/PCManager/uires/uires.idx -p uires -r ./res/PCManager.rc2 -h ./res/R.h idtable ', 
                    ],
                }, 
                
                {
                    'action_name': 'APP pre-Build Script QQLogin resource',
                    'message': 'APP pre-Build Script QQLogin resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                        '<(app_root)/source/demos/QQLogin/gen.out', 
                    ],
                    'action':
                    [
                        '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/QQLogin/uires/uires.idx -p uires -r ./res/QQLogin.rc2 -h ./res/R.h idtable ', 
                    ],
                }, 
                
                {
                    'action_name': 'APP pre-Build Script SoTool resource',
                    'message': 'APP pre-Build Script SoTool resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                        '<(app_root)/source/demos/SoTool/gen.out', 
                    ],
                    'action':
                    [
                        '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/SoTool/uires/uires.idx -p uires -r ./res/SoTool.rc2 -h ./res/R.h idtable ', 
                    ],
                }, 
                
                {
                    'action_name': 'APP pre-Build Script souispy resource',
                    'message': 'APP pre-Build Script souispy resource...',
                    'msvs_cygwin_shell': 0,
                    'inputs': [ 
                    		'<(app_root)/uiresbuilder.exe',
                    ],
                    'outputs': [
                        '<(app_root)/source/demos/souispy/gen.out', 
                    ],
                    'action':
                    [
                        '<(app_root)/uiresbuilder.exe  -i <(app_root)/source/demos/souispy/uires/uires.idx -p uires -r ./res/souispy.rc2 -h ./res/R.h idtable ', 
                    ],
                }, 
                 
                
            ], #actions
        }, 
       
        
       {
          'target_name': 'All',
          'type': 'none',
          'dependencies':
          [ 
          	  '<(app_root)/source/SOUI/SOUI.gyp:*',
          	  '<(app_root)/source/third-part/third-part.gyp:*',          	  
          	  '<(app_root)/source/components/components.gyp:*',        	  
          	  '<(app_root)/source/soui-sys-resource/soui-sys-resource.gyp:*',
          	  '<(app_root)/source/demos/demos.gyp:*', 
          	  '<(app_root)/source/tools/tools.gyp:*',  
          ],
      }, 
    ],
}
