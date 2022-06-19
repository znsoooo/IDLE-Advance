"""打印回车符换成换行符"""
# 解决进度条库在IDLE中全部显示在一行中的问题


if __name__ == '__main__':
    import __init__
    __init__.test_shell(__file__)


import re


CLEAR_LINE = 1


class PrintCr:
    def __init__(self, parent):
        if hasattr(parent, 'write'): # is shell?
            self.text = parent.per.bottom
            self._write, parent.write = parent.write, self.write

    def write(self, s, tags=()):
        s = s.replace('\r\n', '\n')
        if '\r' in s and CLEAR_LINE: # 清除行和替换为换行两种模式选择
            self.text.delete('iomark linestart', 'iomark lineend')
            s = re.sub(r'.*\r', '', s)
        self._write(s.replace('\r', '\n'), tags)


""" TEST CODE:
print('12345\rabc')
for i in range(1, 10):
    __import__('time').sleep(0.2)
    print(f'\rprocess: {i/10:.0%}', end='', file=__import__('sys').stderr)

"""
