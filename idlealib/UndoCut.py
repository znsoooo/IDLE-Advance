"""将剪切合并为一步撤销动作"""


if __name__ == '__main__':
    import __init__
    __init__.test_editor(__file__)


class UndoCut:
    def __init__(self, parent):
        parent.before_paste.insert(0, parent.undo.undo_block_start)
        parent.after_paste.insert(0, parent.undo.undo_block_stop)
