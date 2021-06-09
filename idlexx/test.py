import os
import re
import sys
from .util import Cur2Lc, Pos2Cur, Cur2Pos, Select, SelectSpan

print(bytes(range(128)))
print(re.sub(rb'\w', b'', bytes(range(128))))

def FindKey(key, path='lib/idlelib'):
    print('\nFindkey:\n"%s" in "%s":'%(key, path))
    for root, folders, files in os.walk(os.path.join(sys.base_prefix, path)):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), encoding='u8') as f:
                    s = f.read()
                for m in re.finditer(key, s):
                    print(file, Pos2Cur(s, m.start()), m.group().strip())

# FindKey(r'.*\bCopy\b.*')
# FindKey(r'.*\b\.tcl\b.*', path='lib/tkinter')


def PrintTags(text):
    print(text.tag_names())
    for name in text.tag_names():
        print(name, text.tag_ranges(name))

