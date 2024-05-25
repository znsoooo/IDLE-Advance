@echo off

set py=python

%py% setup.py sdist
echo.

for /f %%i in (VERSION.txt) do (set ver=%%i)
echo Version:
echo   %ver%
echo.

%py% -m pip install dist/idlea-%ver%.tar.gz
echo.

:: switch directory to avoid import package in current path
cd idlealib
%py% -c "__import__('idlealib.ContextManager').ContextManager.AddWindowsMenu()"
%py% -m idlealib
echo.

pause
