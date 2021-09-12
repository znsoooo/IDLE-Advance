'''提取说明文件到readme.md'''

import os
import glob
import imp

os.chdir('..')
for file in glob.iglob('*.py'):
    pkg = imp.load_package(file, file) # every package's `name` should not repeat.
    print('- __%s__  '%file.replace('_', '\\_'))
    print(str(pkg.__doc__).strip().replace('\n', '  \n'))
    print()
