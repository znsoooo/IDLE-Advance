import os
import re
import sys
from .util import Cur2Lc, Pos2Cur, Cur2Pos, Select, SelectSpan

# print(bytes(range(128)))
# print(re.sub(rb'\w', b'', bytes(range(128))))

def FindKey(key, path='lib/idlelib'):
    print('\nFindkey:\n"%s" in "%s":'%(key, path))
    for root, folders, files in os.walk(os.path.join(sys.base_prefix, path)):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), encoding='u8') as f:
                    s = f.read()
                for m in re.finditer(key, s):
                    print(file, Pos2Cur(s, m.start()), m.group().strip())
    print()

# FindKey(r'.*\bCopy\b.*')
# FindKey(r'.*\b\.tcl\b.*', path='lib/tkinter')


def PrintTags(text):
    print(text.tag_names())
    for name in text.tag_names():
        print(name, text.tag_ranges(name))


# class MyPyShellFileList(PyShellFileList):
#     def unregister_maybe_terminate(self, edit): # TODO 关闭最后一个窗口时的策略(暂时没用)
#         key = self.inversedict[edit]
#         if key:
#             del self.dict[key]
#         del self.inversedict[edit]
#         if not self.inversedict:
#             self.open_shell()
#             self.open('run.py')
