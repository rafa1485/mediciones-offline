call "%~dp0%\Env\Scripts\activate.bat"

set actual_dir=%~dp0%

set interpreter_python="%actual_dir%\Env\Scripts\python.exe"

::cd "%actual_dir%\resultados"

%windir%\system32\cmd.exe /K %interpreter_python% gui-mediciones.py

pause

