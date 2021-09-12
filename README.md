# IDLE-Advance

## About

__Platform:__ >= Windows or Linux/macOS (untested)
__Python:__ >= Python 3.6
__Author:__ Lishixian (znsoooo)
__Github:__ https://github.com/znsoooo/IDLE-Advance
__License:__ MIT License. Copyright (c) 2021 Lishixian (znsoooo). All Rights Reserved.


## What is it?
- Add some useful extensions base on idlelib. Can be work on any place with IDLE.
- See "~/idlealib/readme.md" to get spec of each extension. It is same as open script and watch \__doc__.
- Stop extension(s) by move script(s) to "nouse" folder.
- It will generate ".pybak" file in script folder, and "recent-saved.lst" in userdir. Make sure no important files will be overwritten.


## How to use?

### Run directly
It is same as run such file by python/pythonw:
> ~/run.py
> ~/idlealib/\__main__.py
> ~/idlealib/scripts/run.py

### Install by pip
> pip install idlea

or update:
> pip install idlea --upgrade

for drag-open file feature:
> pip install windnd

### Install by source
> python setup.py install

### Run script in shell
Script in Python folder `~/Scripts`:
> idlea

### Run module as script
> python -m idlealib

### Run module in python
> import idlelib
> idlelib.run()

### Run unit test of one extension
Open any ".py" file in "~/idlealib" folder directly.

### stop extension(s)
Move stopped script file to "~/nouse" folder and restart IDLE-Advance.


## How to Set?

### Quick set
Make shortcut to Desktop and Startup Menu.
Open the GUI config helper and setting:
> ~/idlealib/scripts/context_helper.pyw

### Make shortcut
Make shortcut of "~/idlealib/\__main__.py" to Desktop or Startup Menu folder or anywhere.

### Add to right-click menu (only windows)
Create `path` and add `value` to Regedit.

Value:
> "~\pythonw.exe" "~\idlealib\__main__.py" "%L" %*

Path:
> "HKEY_CURRENT_USER\Software\Classes\Python.File\Shell\Edit with IDLE-Adv\command"
