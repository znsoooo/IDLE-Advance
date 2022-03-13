# IDLE-Advance

## About
- __Platform:__ >= Windows or Linux/macOS (untested)
- __Python:__ >= Python 3.4
- __Author:__ Lishixian (znsoooo)
- __Github:__ https://github.com/znsoooo/IDLE-Advance
- __License:__ MIT License. Copyright (c) 2022 Lishixian (znsoooo). All Rights Reserved.


## What is it?
- `IDLE-Advance`  add some useful extensions base on `idlelib`. It can be work on any platform where `IDLE` can be work.
- See `~/idlealib/readme.md` to get spec of each extension. It is same as open each script and watch \_\_doc__.
- Stop extension(s) by moveing script(s) to `nouse` folder.
- It will generate `.pybak` file in script folder, and `recent-saved.lst` in `userdir`. So make sure no important files will be overwritten.


## How to use?

### Run directly
It is same as run such file by `python` or `pythonw`:
```bash
~/run.py  
~/idlealib/__main__.py  
~/idlealib/scripts/run.py
```

### Install by pip
```bash
pip install idlea --upgrade
```

install `windnd` and `qrcode` for `drag-open` and `code-share` feature:
```bash
pip install windnd
pip install qrcode
```

### Install by source
```bash
python setup.py install
```

### Run script in shell
Script in Python folder `~/Scripts`:
```bash
idlea
```

### Run module as script
```bash
python -m idlealib
```

### Run module in python
```python
import idlealib
idlealib.run()
```

### Run unit test of one extension
Open any `~/idlealib/*.py` file directly.

### Stop extension(s)
Move stopped script file to `~/nouse` folder and restart `idlea`.


## How to Set?

### Quick set
Make shortcut to Desktop and Startup Menu.  
Open the GUI config helper and setting:

```bash
~/idlealib/scripts/context_helper.pyw
```

### Make shortcut
Make shortcut of `~/idlealib/__main__.py` to Desktop or Startup Menu folder or anywhere.

### Add to right-click menu (only windows)
Create `path` in `regedit`:
```
HKEY_CURRENT_USER\Software\Classes\Python.File\Shell\Edit with IDLE-Adv\command
```

and set `value` as:
```
"~\pythonw.exe" "~\idlealib\__main__.py" "%L" %*
```


# IDLE增强计划（Advance）
- __Author:__ Lishixian
- __QQ:__ 11313213
- __Email:__ lsx7@sina.com
- __Website:__ https://github.com/znsoooo/IDLE-Advance


## 运行方法
- __平台：__ Windows/Python3.4 （Python3.4.4是Windows XP支持的最后一个版本，所以低于此版本的不再测试。Linux/macOS平台未做测试）
- __依赖：__ 可选择地安装windnd库，增加拖拽脚本文件到窗口即可打开的快捷操作，不安装此依赖也不影响整体运行
- __使用：__ 用python启动run.py文件，随后在此界面上操作打开其他的脚本文件即可
- __功能：__ 见后文todolist，实现的功能已经标记，剩余部分争取在1年之内完成

## 关于项目

### 笔者的话

- 本项目（IDLE-Advance）和另一个[IDLEX](http://idlex.sourceforge.net)的开发项目没有关联！
- 由于该项目停止维护已久（2012年），并且该项目使用者的主要功能提升是增加了可以显示代码行号。
- 但是我认为IDLE本来在窗口的右下角就有显示行号，甚至在新版的python中，可选的显示行号功能直接增加为了新的feature（py3.9）。
- 所以笔者不在前人的轮子基础上继续修改，而是选择重新造一个轮子。


### 项目目标

- 众所周知，Python安装自带IDLE，是一个轻量级的编辑器，比命令行的python和记事本打开修改py文件的调试效率高了无数倍，甚至还有断点和单步调试的功能。
- 但是那么多人使用PyCharm等第三方编译环境也不是没有道理的，PyCharm中的很多便捷操作确实很实用，但是毕竟PyCharm实在是太大了（300MB+）。
- 抱着IDLE发展了20+年，也一直有人在用的打算，这个轮子应该不会马上被抛弃。增强IDLE的功能，通过一些简单但实用的功能，增加IDLE的生命力，让坚守者可以坚持得更久一点（？）。
- 本工程代码中有大量的`TODO`标记，如果希望贡献意见，可以在GitHub上提交修改。不过GitHub我不太会用，修改代码前最好留言说明，或者发送给我邮件：11313213@qq.com ，非常感谢您的贡献！


### 使用方法

- 本代码运行需保证已经安装Python和IDLE，新增方法采用hack进原idlelib库的方法，所以除了增加部分功能完全没有影响IDLE的原始功能，不需要改变任何idlelib的原始代码即可运行。
- 原始IDLE实现右键即可通过IDLE打开的方法，实际是是通过添加右键菜单转义为将idlelib库通过带参数运行的方式启动。本作并不想采用创新的方法重新造轮子，所以为了修改只需要将原来的idlelib换成idlealib即可改变右键编辑的功能。
- 或者可以直接使用python运行本代码，会启动shell，然后打开后续的.py脚本文件可以实现相同的效果。
- 所有的方法都展示在菜单栏最后一个增加的Advance项目下，以供快速使用。


## Todolist

★★★★★（Very Useful）
- [x] 选中同名变量高亮（全字匹配、右键上一条和下一条、右键搜索）
- [x] Alt+左/右导航上一次鼠标点击位置/回到上次编辑的位置/前进后退上次光标位置
- [x] 查找替换工具条（搜索记录、大小写匹配、全字匹配、正则、匹配数量、修改动态显示、所有匹配结果高亮、只替换选中的区域、上下条、多文件搜索）

★★★★（Useful）
- [x] 横向滚动条
- [x] 历史剪切版
- [x] 快速添加/删除括号
- [x] 双击选中（选中括号内的内容、引号中的内容、注释内容、连续空格）
- [x] 双击左侧空白选中代码块
- [x] 检测文件变化重新加载
- [x] 打开时回到上次编辑的位置
- [x] 不保存运行当前脚本（Shift+F5）
- [x] 自动恢复未保存NewFile的内容
- [x] 未选中文本时，复制/剪切选中当前行
- [x] 文本纵向选择

★★（Good）
- [x] 打开脚本所在目录/终端打开脚本所在目录/拷贝脚本所在路径、完整路径、文件名/插入脚本路径
- [x] 运行选中的代码（自动缩进调整）/运行到光标位置/从光标位置开始运行
- [x] 复制文件名/打开路径/插入文件名、重新加载、修改文件名
- [x] 快捷反向查找（F3/Shift+F3）
- [ ] 内建搜索窗口置顶但不捕捉
- [x] 自动备份/定时备份/打开时恢复未保存记录
- [x] 拖拽打开文件
- [x] 二维码分享代码
- [x] 交换位置复制（Ctrl+Shift+X）
- [x] 自动补全保留关键词
- [ ] 快速大小写转换
- [x] 可选中Calltips中的文本
- [x] 选中变量帮助查看器

★（Better）
- [x] 快捷键窗口循环切换/恢复页面/关闭窗口(并激活下一个窗口)/关闭全部
- [x] 显示最近打开的修改过的文件
- [x] 带参数运行脚本
- [x] 快速打开资源文件
- [x] 模拟打印\r效果
- [x] 版本比较（基于difflib）
- [x] 快速输入当前时间戳注释文本
- [ ] 按照剪切板文本搜索
- [ ] 取消关闭窗口后清空剪切板

☆（Shell）
- [x] 多行运行
- [x] 魔法复制
- [x] 执行记录新建为脚本
- [x] 清空Shell或Shell选中的内容
- [x] 自动换行切换
- [ ] 本地记录历史操作

☆（Other）
- [x] 模块单元测试
- [x] 提交PyPI
- [x] 兼容py34
- [ ] 扩展管理器（开关和配置热键）
- [ ] 检查更新
- [x] 关于框
- [x] 快捷启动器
- [x] 快捷部署器（右键菜单/右键新建/桌面和开始菜单快捷方式）
- [ ] 一键打开Github网页项目
- [x] 汇总打印扩展简要说明
- [x] 添加Scripts脚本
- [x] 支持包模式运行

×（Future）
- [ ] Filelist/Shell/Editor连在一个窗口
- [ ] 自动补全作用域内的参数名
- [ ] 放置鼠标气泡显示数值/引用参数查看定义位置/定义参数查找使用位置
- [x] 快速查看被引用内容（比如打开图片、文本、快速执行命令）
- [ ] 代码模板（Exception和pdb调试）

×（Forget）
- [ ] 注释后移动到下一行
- [ ] Shell自由编辑模式（F12）


## 他山之石

### Pycharm
- [ ] 选择python解释器
- [x] 带参数运行脚本
- [x] 调试运行到光标位置
- [x] 自动换行
- [ ] 快速换行（Shift+Enter）
- [x] 快速大小写转化（Ctrl+Shift+U）
- [ ] 代码折叠
- [x] 历史剪切版
- [ ] 书签
- [x] 捕获异常模板（Exception和pdb调试）
- [ ] 代码模板
- [x] 双击左侧空白选中代码块
- [ ] 多规则搜索筛选文件排除测试文件
- [x] 回到上次编辑的位置
- [ ] 进入函数方法（进入定义、进入父类定义方法）
- [x] 前进后退上次光标位置
- [x] 显示最近打开的修改过的文件
- [ ] 搜索TODO和FIXME
- [x] 最近搜索记录
- [ ] 正则表达式测试
- [ ] 代码滚动预览
- [ ] 储存操作记录（历史编辑文件）
- [ ] 输入时自动匹配（下拉菜单、忽略大小写）
- [x] 文本纵向选中
- [ ] 代码重构：变量重命名、函数重命名（使用替换、全字匹配、区域替换等）
- [x] 打开脚本所在目录
- [x] 终端打开脚本所在目录
- [x] 拷贝脚本所在路径/完整路径/文件名
- Ref: http://pycharm.iswbm.com/

### IELDX
- [x] 在shell中粘贴并运行多行
- [x] 无需重新启动即可清除Shell窗口
- [ ] 按F8使用代码浏览器改进代码导航（和class browser功能雷同）
- [ ] 查找和替换作为具有增量搜索的工具栏
- [x] shell智能粘贴（删除 >>> 提示）
- [ ] 在编辑器中突出显示(\t)
- [x] 使用F9从编辑器中执行突出显示的代码或单行
- [ ] 文档查看器在单独的窗口中查看help()和文档字符串
- [x] 查看网站和检查更新状态
- [x] 扩展管理器
- [x] 关于框
- [x] 快捷启动器
- [x] 快捷部署器（增加右键菜单）
- Ref: http://idlex.sourceforge.net
