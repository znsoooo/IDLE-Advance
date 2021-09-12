import os
import re
import sys


def lc(s):
    ss = s.split('\n')
    cur = '%d.%d' % (len(ss), len(ss[-1]))
    return cur


def FindKey(key, path='lib/idlelib'):
    print('\nFindkey:\n"%s" in "%s":'%(key, path))
    for root, folders, files in os.walk(os.path.join(sys.base_prefix, path)):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), encoding='u8') as f:
                    s = f.read()
                for m in re.finditer(key, s):
                    print(file, lc(s[:m.start()]), m.group().strip())
    print()


def PrintTags(text):
    print(text.tag_names())
    for name in text.tag_names():
        print(name, text.tag_ranges(name))


if __name__ == '__main__':
    FindKey('hello......')

    FindKey(r'.*\bCopy\b.*')
    FindKey(r'.*\b\.tcl\b.*', path='lib/tkinter')

    # FindKey(r'.*EditorWindow.*')

    # FindKey(r'.*<<.*>>.*')

    # FindKey(r'FocusIn')
    # FindKey(r'FOCUSIN')

    # FindKey(r".*\bListedToplevel\b.*")
    # FindKey(r".*\bunregister_callback\b.*")
    # FindKey(r".*\bdict\.\b.*")
