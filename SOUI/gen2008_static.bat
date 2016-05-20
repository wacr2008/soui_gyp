call setenv2008.bat

set GYP_DEFINES=component=static_library buildtype=Official

call python %~dp0source\config\com_gen.py static_library 
call python %~dp0source\config\core_gen.py static_library 

python source/build/gyp_app  -Dextra_gyp_flag=0