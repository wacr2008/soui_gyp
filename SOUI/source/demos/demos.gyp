
{  
  'targets': [
    {
      'target_name': 'demos',
      'type': 'none',  
      'dependencies': [ 
	      '360demo/360demo.gyp:*',
	      '360Preview/360Preview.gyp:*',
	      'demo/demo.gyp:*',
	      'mclistview_demo/mclistview_demo.gyp:*',
	      'PCManager/PCManager.gyp:*',
	      'QQLogin/QQLogin.gyp:*',
	      'SoTool/SoTool.gyp:*',
	      'souispy/souispy.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
