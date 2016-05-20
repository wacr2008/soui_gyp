call setenv.bat

call python %~dp0source\config\com_gen.py shared_library 
call python %~dp0source\config\core_gen.py shared_library 

python source/build/gyp_app  -Dextra_gyp_flag=0