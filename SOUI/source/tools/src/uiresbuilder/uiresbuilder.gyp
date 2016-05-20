
{  
  'includes': [
    '../../../../build/win_precompile.gypi',
    'uiresbuilder.gypi',
  ],
  'targets': [
    {
      'target_name': 'uiresbuilder',
      'type': 'executable',
      'includes': [ '../../../build/common.gypi', ],   
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
