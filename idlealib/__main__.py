"""主程序入口"""

# Usage: python -m idlealib


def FixPath():
    # To fix `python -m idlealib` cant find `__init__`.
    import os
    import sys
    path = os.path.dirname(__file__)
    if path not in sys.path:
        sys.path.insert(0, path)


if __name__ == '__main__':
    FixPath()
    import __init__
    __init__.run()
