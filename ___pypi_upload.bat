:: auto get current version and upload to pypi

for /f %%a in (VERSION.txt) do (set ver=%%a)
echo %ver%

python -m twine upload dist/idlea-%ver%.tar.gz
pause
