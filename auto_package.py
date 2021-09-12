# TODO 增加右键菜单和拖拽启动打包

import os
import glob
import time
import zipfile


def mark(target):
    tt = time.strftime('.%Y%m%d_%H%M%S')
    base, ext = os.path.splitext(target)
    os.rename(target, base + tt + ext)


def compress(paths, except_key=()):
    save_name = os.path.splitext(paths[0])[0] + time.strftime('.%Y%m%d_%H%M%S.zip')
    zip = zipfile.ZipFile(save_name, 'w', zipfile.ZIP_DEFLATED)
    for path in paths:
        if os.path.isfile(path):
            zip.write(path, path)
        else:
            for file in glob.iglob('%s/**' % path, recursive=True):
                if all(key not in file for key in except_key):
                    zip.write(file, file)
    zip.close()


# mark('idlealib.zip')

lst = [file for file in os.listdir() if os.path.isfile(file) and not file.startswith('test') and not file.endswith('.zip')]
print(lst)

compress(('idlealib', *lst),
         except_key=('__pycache__',))
