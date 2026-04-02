# RAW和JPG文件自动核对工具

这个工具可以帮助摄影爱好者自动核对RAW和JPG文件的对应关系，特别适合那些使用JPG选片、RAW做后期处理的用户。

## 功能特点

- 自动扫描指定目录下的RAW和JPG文件
- 支持常见相机厂商的RAW格式（如Canon的CR2/CR3、Nikon的NEF、Sony的ARW等）
- 自动核对文件名，找出有对应关系的文件和缺少对应文件的情况
- 生成详细的匹配报告
- 支持将匹配的RAW文件移动到指定目录
- 提供直观的GUI界面，同时保留命令行模式

## 如何使用

### GUI模式（推荐）

1. 打开命令行窗口（Windows用户可以使用PowerShell或命令提示符）
2. 导航到脚本所在目录：
   ```
   cd e:\RAW to JPEG
   ```
3. 运行脚本：
   ```
   python raw_jpg_checker.py
   ```
4. 在弹出的GUI界面中：
   - 点击"浏览"按钮选择要扫描的目录
   - 点击"浏览"按钮选择输出目录（用于存放匹配的RAW文件）
   - 点击"扫描文件"按钮开始扫描和匹配
   - 查看匹配结果
   - 点击"移动匹配的RAW文件"按钮将匹配的RAW文件移动到指定输出目录

### 命令行模式

#### 基本用法

```
python raw_jpg_checker.py
```

#### 扫描指定目录

```
python raw_jpg_checker.py "D:\Photos\2023-01-01"
```

#### 自定义文件扩展名

```
# 自定义RAW和JPG扩展名
python raw_jpg_checker.py --raw-ext .CR2 .NEF --jpg-ext .jpg .jpeg
```

#### 输出结果到文件

```
python raw_jpg_checker.py --output results.txt
```

## 示例输出

```
扫描目录: D:\Photos\2023-01-01
找到 15 个RAW文件
找到 15 个JPG文件

=== 匹配结果 ===
✓ JPG文件 'IMG_1234.JPG' 有对应的RAW文件: 'IMG_1234.CR2'
✓ JPG文件 'IMG_1235.JPG' 有对应的RAW文件: 'IMG_1235.CR2'
✗ JPG文件 'IMG_1236.JPG' 没有对应的RAW文件

=== 总结 ===
有 14 个JPG文件找到了对应的RAW文件
有 1 个JPG文件没有找到对应的RAW文件

=== 没有对应RAW文件的JPG列表 ===
- IMG_1236.JPG

=== 没有对应JPG文件的RAW列表 ===
- IMG_1237.CR2
```

## 支持的RAW格式

默认支持以下RAW格式：
- .CR2, .CR3 (Canon)
- .NEF (Nikon)
- .ARW (Sony)
- .DNG (Adobe)
- .ORF (Olympus)
- .RAF (Fujifilm)
- .PEF (Pentax)
- .SRF, .SR2 (Sony)
- .X3F (Sigma)

## 注意事项

1. 工具通过文件名（不含扩展名）来匹配RAW和JPG文件，因此请确保同一照片的RAW和JPG文件具有相同的文件名（除扩展名外）
2. 工具会递归扫描指定目录及其子目录
3. 对于大量文件的目录，扫描可能需要一些时间
4. 移动文件时，工具会使用复制方式（保留文件元数据），不会删除原始文件

## 系统要求

- Python 3.6或更高版本
- 无需安装额外依赖（使用Python标准库）
