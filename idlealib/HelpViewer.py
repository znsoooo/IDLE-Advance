"""帮助查看器"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import io
import re

import sys
if sys.version_info > (3, 6):
    from idlelib.textview import view_text
    from idlelib.calltip import get_entity
else:
    from idlelib.textView import view_text
    from idlelib.CallTips import get_entity


sp = lambda c: eval(c.replace('.',',')) # Good!
jn = lambda x,y: '%i.%i'%(x,y) # Good!


def HelpText(object):
    # 在pydoc.ttypager和pydoc.plainpager中使用了一些`sys.stdout.write`的方法，所以hack重定向此方法后读取help文本
    f = io.StringIO()
    stdout, sys.stdout = sys.stdout, f
    help(object)
    sys.stdout = stdout
    f.tell()
    f.seek(0)
    return f.read()


class HelpViewer:
    def __init__(self, parent):
        self.text = parent.text
        parent.rmenu.add_separator()
        parent.rmenu.add_command(label='Help Viewer', command=self.view)
        parent.add_adv_menu('Help Viewer', self.view)

    def view(self):
        text = self.text
        if not text.tag_ranges('sel'):
            if re.match('\W', text.get('insert')):
                text.tag_add('sel', 'insert', 'insert+1c')
            else:
                ln, col = sp(text.index('insert'))
                line = text.get('%d.0' % ln, '%d.end' % ln)
                end = col + re.match('\w+', line[col:]).end()
                start = re.search('[\w.]+$', line[:end]).start()
                text.tag_add('sel', jn(ln, start), jn(ln, end))

        sel = text.get('sel.first', 'sel.last')
        obj = get_entity(sel)
        if obj is None:
            obj = sel

        view_text(text, 'Help on %r:' % sel, HelpText(obj), modal=False)
