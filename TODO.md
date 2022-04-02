## Todo
- 比较引擎显示更新

### Features
X 记录shell历史记录到文件
X shell自由编辑模式（F12）
- About显示readme.md
- 大小写切换

### Fix
- help引擎修复
- 关闭未保存时不记录untitled
- .idlerc路径读取问题
- 插件顺序整理
- 把各个插件的文件读写需求情况写明

### For Test
```
python -m idlealib
print(__import__('os').getcwd())
print(__import__('os').path.expanduser('~'))
print('\n'.join(__import__('sys').path))
```
## TODO NOTE
- 选中两个文件右键交换文件名
