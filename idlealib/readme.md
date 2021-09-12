# Specification of extensions

- __init__.py
运行__main__.py获得一个加载所有插件的IDLE-Advance的示例文件。
运行__init__.py获得一个打开自身脚本并加载所有插件的editor的例子。
分别运行idlealib目录下的扩展文件，可以得到一个打开自身的editor或shell的例子。
如果需要停用部分扩展，将对应的脚本移出目录后重启IDLE即可。

- __main__.py
主程序入口

- AutoReload.py
重载文件

- AutoSave.py
自动备份

- CalltipSelect.py
可选中函数提示

- ClearShell.py
清空Shell

- CompareFile.py
文本比较

- CopyNoSelect.py
当选区为空时复制/剪切复制当前行

- CursorHistory.py
光标记录

- DragOpen.py
拖拽打开

- FileManager.py
文件操作

- QuickSearch.py
快速正反搜索

- RecentClipboard.py
历史剪切板

- RecentClosed.py
最近关闭列表

- RecentSaved.py
位置记录

- ReplaceBar.py
搜索替换工具条

- RunMultiLine.py
Shell多行运行

- RunSelected.py
运行选中

- SahreQRCode.py
将选中代码转化为二维码

- SaveArchive.py
记录备份

- ScrollHorizontal.py
横向滚动条

- SmartCopy.py
仅拷贝Shell的代码

- SmartPairing.py
匹配成对括号

- SmartSelect.py
智能选取

- SwapCopy.py
交换复制

- TimeTag.py
插入时间戳注释

- WindowManager.py
窗口操作