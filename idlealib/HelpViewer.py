"""帮助查看器"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


import io

import sys
if sys.version_info > (3, 6):
    from idlelib.textview import view_text
else:
    from idlelib.textView import view_text


def HelpText(object): # TODO 读取真正的object而不是string
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
        sel = self.text.get('sel.first', 'sel.last')
        view_text(self.text, 'Help on %r:' % sel, HelpText(sel))
