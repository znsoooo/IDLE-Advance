from idlexx import test


test.FindKey(r'.*\'=\'.*')
# test.FindKey(r'.*<<.*>>.*')
# test.FindKey(r'.*\.(open|_close|save).*')

# test.FindKey(r'.*recent_file.*')


# test.FindKey(r'FocusIn')
# test.FindKey(r'FOCUSIN')
# test.FindKey(r".*'window'.*")

# test.FindKey(r".*\bListedToplevel\b.*")
# test.FindKey(r".*\bunregister_callback\b.*")
# test.FindKey(r".*\bdict\.\b.*")



import tkinter as tk
# help(tk.Tk.bind)

from idlexx import run

run()

# TODO 检查run(None)只运行shell时运行错误的原因