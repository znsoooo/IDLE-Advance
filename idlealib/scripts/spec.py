'''提取说明文件到readme.md'''

import os
import imp

for file in os.listdir('..'):
    if file.endswith('.py'):
        pkg = imp.load_package('pkg', '../' + file)
        print('- ' + file)
        print(str(pkg.__doc__).strip())
        print()
