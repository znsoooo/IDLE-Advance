# Specification of extensions

- __\_\_init\_\_.py__  
运行__main__.py获得一个加载所有插件的IDLE-Advance的示例文件。  
运行__init__.py获得一个打开自身脚本并加载所有插件的editor的例子。  
分别运行idlealib目录下的扩展文件，可以得到一个打开自身的editor或shell的例子。  
如果需要停用部分扩展，将对应的脚本移出目录后重启IDLE即可。

- __\_\_main\_\_.py__  
主程序入口

- __About.py__  
显示版本信息和自动升级

- __AutoReload.py__  
重载文件

- __AutoSave.py__  
自动备份

- __CalltipSelect.py__  
可选中函数提示

- __ClearShell.py__  
清空Shell

- __CompareFile.py__  
文本比较

- __CopyNoSelect.py__  
当选区为空时复制/剪切复制当前行

- __CursorHistory.py__  
光标记录

- __DragOpen.py__  
拖拽打开

- __FileManager.py__  
文件操作

- __HelpViewer.py__  
帮助查看器

- __PrintCr.py__  
打印回车符换成换行符

- __QuickOpen.py__  
快速打开选中的文本

- __QuickSearch.py__  
快速正反搜索

- __RecentClipboard.py__  
历史剪切板

- __RecentClosed.py__  
最近关闭列表

- __RecentSaved.py__  
位置记录

- __ReplaceBar.py__  
搜索替换工具条

- __RunArgs.py__  
带参数运行

- __RunMultiLine.py__  
Shell多行运行

- __RunSelected.py__  
运行选中

- __SahreQRCode.py__  
将选中代码转化为二维码

- __SaveArchive.py__  
记录备份

- __SaveUntitled.py__  
自动保存Untitled

- __ScrollHorizontal.py__  
横向滚动条

- __SelectVertical.py__  
纵向选择

- __SmartCopy.py__  
仅拷贝Shell的代码

- __SmartPairing.py__  
匹配输入和删除成对括号

- __SmartSelect.py__  
智能选取

- __SwapCopy.py__  
交换复制

- __TimeTag.py__  
插入时间戳注释

- __WindowManager.py__  
窗口操作

- __WrapShell.py__  
Shell换行
