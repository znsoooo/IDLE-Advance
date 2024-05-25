@echo off

for /f %%i in (VERSION.txt) do (set ver=%%i)
echo Version:
echo   %ver%
echo.

echo Python versions:
py -0
echo.

pause
echo.

:: switch directory to avoid import package in current path
cd idlealib

for /f %%i in ('py -0') do (
    echo ====================
    echo.
    echo pip install on python %%i ...
    echo.
    py %%i -m pip install ..\dist\idlea-%ver%.tar.gz -U
    echo.
    pyw %%i -c "__import__('idlealib.ContextManager').ContextManager.AddWindowsMenu()"
    start py %%i -m idlealib
    echo.
)
echo ====================
echo.

pause
