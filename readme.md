# IDLE增强计划（Advance）
- __Author:__ Lishixian
- __QQ:__ 11313213
- __Email:__ lsx7@sina.com
- __Website:__ github.com/znsoooo/IDLE-Advance


## 运行方法
- __平台：__ Windows/Python3.6 （其他平台未测试，但是计划支持Linux/Windows和py3.4以上的版本）
- __依赖：__ 可选择地安装windnd库，增加拖拽脚本文件到窗口即可打开的快捷操作，不安装此依赖也不影响整体运行
- __使用：__ 用python启动idlexx.py文件，随后在此界面上操作打开其他的脚本文件即可
- __功能：__ 见后文todolist，实现的功能已经标记，剩余部分争取在1年之内完成


## Todolist

★★★★★（Very Useful）
- [x] 选中同名变量高亮（全字匹配、右键上一条和下一条、右键搜索）
- [x] Alt+左/右导航上一次鼠标点击位置/回到上次编辑的位置/前进后退上次光标位置
- [x] 查找替换工具条（搜索记录、大小写匹配、全字匹配、正则、匹配数量、修改动态显示、所有匹配结果高亮、只替换选中的区域、上下条、多文件搜索）

★★★★（Useful）
- [x] 历史剪切版
- [x] 快速加括号、引号、方括号/快速拆括号
- [ ] 显示最近打开的修改过的文件
- [x] 双击选中（FIX遇到中文的问题、选中括号内的内容、引号中的内容、注释内容、连续空格）
- [x] 双击左侧空白选中代码块
- [x] 打开时回到上次编辑的位置

★★（Good）
- [ ] 按照剪切板文本搜索
- [x] 打开脚本所在目录/终端打开脚本所在目录/拷贝脚本所在路径、完整路径、文件名/插入脚本路径
- [x] 运行选中的代码（自动缩进调整）
- [x] 检测文本变化和重新加载
- [x] 横向滚动条
- [x] 拖拽打开文件
- [x] 快捷键窗口切换/恢复页面/关闭窗口/关闭全部
- [ ] 取消关闭窗口后清空剪切板
- [ ] 自动补全作用域内的参数名
- [ ] File manager: 修改文件名，重新加载，复制和打开和插入

★（Better）
- [ ] 捕获异常模板（Exception和pdb调试）
- [ ] 反方向查找（shift+F3）
- [ ] 放置鼠标气泡显示数值/引用参数查看定义位置/定义参数查找使用位置
- [ ] 自动换行
- [ ] 带参数运行脚本
- [x] 调试运行到光标位置
- [ ] 快速查看被引用内容（比如预览图片、文本、二进制）
- [x] 版本比较（基于difflib）
- [x] 自动备份（.py.2020-08-05.bak）
- [ ] 注释后移动到下一行


## 关于项目

### 笔者的话
- 本项目（IDLE-Advance）和另一个IDLEX的开发项目（ http://idlex.sourceforge.net ）没有关联！
- 由于该项目停止维护已久（2012年），并且该项目使用者的主要功能提升是增加了可以显示代码行号。
- 但是我认为IDLE本来在窗口的右下角就有显示行号，甚至在新版的python中，可选的显示行号功能直接增加为了新的feature（py3.9）。
- 所以笔者不在前人的轮子基础上继续修改，而是选择重新造一个轮子。


### 项目目标
- 众所周知，Python安装自带IDLE，是一个轻量级的编辑器，比命令行的python和记事本打开修改py文件的调试效率高了无数倍，甚至还有断点和单步调试的功能。
- 但是那么多人使用Pycharm等第三方编译环境也不是没有道理的，Pycharm中的很多便捷操作确实很实用，但是毕竟pycharm实在是太大了（300MB+）。
- 抱着IDLE发展了十几年，也一直有人用的想法，这个轮子应该不会马上被抛弃。增强IDLE的功能，通过一些简单但实用的功能，增加IDLE的生命力，让坚守者可以坚持得更久一点（？）。
- 本工程代码中有大量的“TODO”标记，如果希望贡献意见，可以在GitHub上提交修改。不过GitHub我不太会用，修改代码前最好留言说明，或者发送给我邮件：11313213@qq.com ，非常感谢您的贡献！


### 使用方法
- 本代码运行需保证已经安装Python和IDLE，新增方法采用hack进原idlelib库的方法，所以除了增加部分功能完全没有影响IDLE的原始功能，不需要改变任何idlelib的原始代码即可运行。
- 原始IDLE实现右键即可通过IDLE打开的方法，实际是是通过添加右键菜单转义为将idlelib库通过带参数运行的方式启动。本作并不想采用创新的方法重新造轮子，所以为了修改只需要将原来的idle换成idlexx即可改变右键编辑的功能。
- 或者可以直接使用python运行本代码，会启动shell，然后打开后续的.py脚本文件可以实现相同的效果。
- 所有的方法都展示在菜单栏最后一个增加的Advance项目下，以供快速使用。


## 他山之石

### Pycharm
- [ ] 选择python解释器
- [x] 带参数运行脚本
- [x] 调试运行到光标位置
- [x] 自动换行
- [ ] 快速换行（Shift+Enter）
- [ ] 快速大小写转化（Ctrl+Shift+U）
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
- [ ] 文本纵向选中
- [ ] 代码重构：变量重命名、函数重命名（使用替换、全字匹配、区域替换等）
- [x] 打开脚本所在目录
- [x] 终端打开脚本所在目录
- [x] 拷贝脚本所在路径/完整路径/文件名
- Ref: http://pycharm.iswbm.com/

### IELDX
- [ ] 在shell中粘贴并运行多行
- [ ] 无需重新启动即可清除Shell窗口
- [ ] 按F8使用代码浏览器改进代码导航（和class browser功能雷同）
- [ ] 查找和替换作为具有增量搜索的工具栏
- [ ] shell智能粘贴（删除 >>> 提示）
- [ ] 在编辑器中突出显示(\t)
- [ ] 使用 F9 从编辑器中执行突出显示的代码或单行
- [ ] 文档查看器在单独的窗口中查看help()和文档字符串
- [ ] 查看网站和检查更新状态
- [ ] 扩展管理器
- [ ] 关于框
- [ ] 快捷启动器
- [ ] 快捷部署器（增加右键菜单）
- Ref: http://idlex.sourceforge.net
