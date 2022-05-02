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


sp = lambda c: eval(c.replace('.',',')) # Good!
jn = lambda x,y: '%i.%i'%(x,y) # Good!

cmd = '''if 1:
    obj = %r
    try:
        help(eval(obj))
    except (NameError, SyntaxError):
        help(obj)'''


class HelpViewer:
    def __init__(self, parent):
        self.text = parent.text
        self.flist = parent.flist

        parent.rmenu.add_separator()
        parent.rmenu.add_command(label='Help Viewer', command=self.view)
        parent.add_adv_menu('Help Viewer', self.view)

    def view(self):
        sel = self.text.get('sel.first', 'sel.last')
        if sel:
            s = self.help(cmd % sel)
            view_text(self.text, 'Help on %r:' % sel, s, modal=False)

    def help(self, cmd):
        # open shell
        shell = self.flist.pyshell or self.flist.open_shell()
        interp = shell.interp

        # fake printer
        f = io.StringIO()
        _write = shell.write
        shell.write = lambda s, tags=(): f.write(s)

        # run command
        interp.runcommand(cmd)

        # restore
        shell.write = _write

        # get result
        f.seek(0)
        return f.read()
