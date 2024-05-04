@echo off

for /f %%i in (VERSION.txt) do (set ver=%%i)
echo Version:
echo   %ver%
echo.

python -m twine upload dist/idlea-%ver%.tar.gz
echo.

pause
