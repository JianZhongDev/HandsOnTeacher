@echo off
rem Course lab launcher for Windows. Run it from the course folder:
rem   .\lab list  |  .\lab 03/L01  |  .\lab 03/L01 help  |  .\lab 03/L01 size=5000
rem   .\lab run <script> [args]  |  .\lab check
setlocal
set "HERE=%~dp0"
set "COURSE_DIR=%~dp0."

rem ---- set by setup-environment (see course.json) ----------------------------
rem MODE=native runs labs with RUN below. MODE=wsl forwards every command to lab.sh in WSL.
set "MODE=native"
set "WSL_DISTRO="
set RUN="%HERE%.env\Scripts\python.exe" -B
set "LAB_FILE=lab.py"
set CHECK=%RUN% -c "import handson; print('runtime OK')"
set "PYTHONPATH=%HERE%_shared;%PYTHONPATH%"
rem ----------------------------------------------------------------------------

if /i "%MODE%"=="wsl" goto wsl
set "CMD=%~1"
if "%CMD%"=="" set "CMD=list"
rem Keep the remaining arguments as typed: cmd would split key=value at the "=".
set "REST="
for /f "tokens=1,*" %%a in ("%*") do set "REST=%%b"
if /i "%CMD%"=="list" goto list
if /i "%CMD%"=="check" goto check
if /i "%CMD%"=="run" goto run
if /i "%CMD%"=="py" goto run
if /i "%CMD%"=="help" goto usage
echo %CMD%| find "/" >nul || (echo Unknown command "%CMD%". Try: lab help & exit /b 1)

for /f "tokens=1,2 delims=/" %%a in ("%CMD%") do (set "MOD=%%a" & set "LES=%%b")
set "DIR="
for /d %%m in ("%HERE%%MOD%-*") do for /d %%l in ("%%~m\lessons\%LES%*") do if not defined DIR set "DIR=%%~l"
if not defined DIR (echo No lab found for %CMD%. Try: lab list & exit /b 1)
pushd "%DIR%"
%RUN% %LAB_FILE% %REST%
set "RC=%ERRORLEVEL%"
popd
exit /b %RC%

:list
echo Labs (run with: lab ^<module^>/^<lesson^> [key=value ...]):
set "FOUND="
for /d %%m in ("%HERE%??-*") do for /d %%l in ("%%~m\lessons\L*") do if exist "%%~l\%LAB_FILE%" (
  for /f "delims=-" %%n in ("%%~nxm") do for /f "delims=-" %%o in ("%%~nxl") do echo   %%n/%%o   %%~nxm / %%~nxl
  set "FOUND=1"
)
if not defined FOUND echo   (none yet: the teaching agent creates labs as lessons are prepared)
exit /b 0

:check
%CHECK%
exit /b %ERRORLEVEL%

:run
set "SCRIPT="
for /f "tokens=1,*" %%a in ("%REST%") do (set "SCRIPT=%%~fa" & set "SARGS=%%b")
if not defined SCRIPT (echo usage: lab run ^<script^> [args] & exit /b 1)
if not exist "%SCRIPT%" (echo No such script: %SCRIPT% & exit /b 1)
for %%f in ("%SCRIPT%") do pushd "%%~dpf"
%RUN% "%SCRIPT%" %SARGS%
set "RC=%ERRORLEVEL%"
popd
exit /b %RC%

:usage
echo   lab list                   your labs
echo   lab 03/L01                 run module 03, lesson L01 with default settings
echo   lab 03/L01 help            the settings this lab lets you change
echo   lab 03/L01 size=5000       change one setting (results are kept per setting)
echo   lab run ^<script^> [args]    run any script with the course runtime
echo   lab check                  check that the runtime works
exit /b 0

:wsl
if defined WSL_DISTRO (
  wsl.exe -d %WSL_DISTRO% --cd "%~dp0." --exec bash ./lab.sh %*
) else (
  wsl.exe --cd "%~dp0." --exec bash ./lab.sh %*
)
exit /b %ERRORLEVEL%
