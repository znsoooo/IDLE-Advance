import os
import time
import zipfile

def mark(target):
    tt = time.strftime('.%Y%m%d_%H%M%S')
    base, ext = os.path.splitext(target)
    os.rename(target, base + tt + ext)

def walk(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
        elif os.path.isdir(path):
            for root, folders, files in os.walk(path):
                for file in files:
                    yield os.path.join(root, file)

def compress(pkg, paths=(), ignore=()):
    save_name = pkg + time.strftime('.%Y%m%d_%H%M%S.zip')
    zip = zipfile.ZipFile(save_name, 'w', zipfile.ZIP_DEFLATED)
    ex = list(walk(ignore))
    for file in walk(paths):
        if all(not os.path.samefile(f1, file) for f1 in ex):
            zip.write(file, file)
    zip.close()


# mark('idlexx.zip')

compress(pkg = 'idlexx',
         paths = (
             'idlexx',
             ),
         ignore = (
             'idlexx/.idea',
             'idlexx/__pycache__',
             'idlexx/test/__pycache__',
             )
         )
