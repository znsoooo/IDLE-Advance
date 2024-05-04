@echo off

python setup.py sdist
echo.

for /f %%i in (VERSION.txt) do (set ver=%%i)
echo Version:
echo   %ver%
echo.

pip install dist/idlea-%ver%.tar.gz
echo.

pause
