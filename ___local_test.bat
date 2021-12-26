:: auto get current version

python setup.py sdist

for /f %%a in (VERSION.txt) do (set ver=%%a)
echo %ver%

pip install dist/idlea-%ver%.tar.gz
pause
