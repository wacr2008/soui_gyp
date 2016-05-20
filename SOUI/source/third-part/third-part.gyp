
{   
  'targets': [
    {
      'target_name': 'third-part',
      'type': 'none',
      'dependencies': [ 
      	'png/png.gyp:*',
      	'skia/skia.gyp:*',
      	'zlib/zlib.gyp:*',
      	'lua-52/lua-52.gyp:*',
      	'smiley/smiley.gyp:*',
      	'mhook/mhook.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
