'''记录备份'''


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import os


def UniqueFile(file):
    root = os.path.splitext(file)[0]
    n = 1
    while os.path.exists(file):
        n += 1
        file = '%s.%d.pybak'%(root, n)
    return file


class SaveArchive:
    def __init__(self, parent):
        return  # TODO too much backup files.

        self.io = parent.io
        parent.after_save.append(self.Saving)

    def Saving(self):
        self.io.writefile(UniqueFile(self.io.filename))