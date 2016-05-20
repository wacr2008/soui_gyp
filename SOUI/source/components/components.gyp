
{  
  'targets': [
    {
      'target_name': 'components',
      'type': 'none',  
      'dependencies': [ 
	      'imgdecoder-gdip/imgdecoder-gdip.gyp:*',
	      'imgdecoder-png/imgdecoder-png.gyp:*',
	      'imgdecoder-stb/imgdecoder-stb.gyp:*',
	      'imgdecoder-wic/imgdecoder-wic.gyp:*',
	      'log4z/log4z.gyp:*',
	      'render-gdi/render-gdi.gyp:*',
	      'render-skia/render-skia.gyp:*',
	      'resprovider-zip/resprovider-zip.gyp:*',
	      'ScriptModule-LUA/ScriptModule-LUA.gyp:*',
	      'translator/translator.gyp:*',
       ],
    },
  ],
}

# Local Variables:
# tab-width:2
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=2 shiftwidth=2:
