@echo off

echo Python versions:
py -0
echo.

pause
echo.

py -c "__import__('idlealib.ContextManager').ContextManager.DeleteWindowsMenuAll()"
for /f %%i in ('py -0') do (
    echo Initial IDLE-Adv Menu on python %%i ...
    pyw %%i -c "__import__('idlealib.ContextManager').ContextManager.AddWindowsMenu()"
)
echo.

pause
