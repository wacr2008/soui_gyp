
{  
  'targets': [
    {
      'target_name': 'tools',
      'type': 'none',  
      'dependencies': [ 
	      'src/uiresbuilder/uiresbuilder.gyp:*',
	      'src/uiresImporter/uiresImporter.gyp:*',	       
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
