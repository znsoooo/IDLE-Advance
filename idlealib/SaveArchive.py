'''记录备份'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os
import time


def StampFile(path):
    root, file = os.path.split(path)
    name, ext = os.path.splitext(file)
    root2 = os.path.join(root, '.pybak')
    os.makedirs(root2, exist_ok=True)

    tag = time.strftime('@%Y%m%d_%H%M%S')
    file2 = os.path.join(root2, name + tag + ext)
    return file2


class SaveArchive:
    def __init__(self, parent):
        self.io = parent.io
        parent.after_save.append(self.Saving)

    def Saving(self):
        self.io.writefile(StampFile(self.io.filename)) # todo 只有未保存的状态下保存才会保存副本
