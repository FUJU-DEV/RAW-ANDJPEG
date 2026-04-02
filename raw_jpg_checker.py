import os
import sys
import argparse
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class RawJpgCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RAW和JPG文件自动核对工具 v1.0")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 默认扩展名
        self.raw_extensions = ['.CR2', '.NEF', '.ARW', '.DNG', '.CR3', '.ORF', '.RAF', '.PEF', '.SRF', '.SR2', '.X3F']
        self.jpg_extensions = ['.JPG', '.JPEG', '.jpg', '.jpeg']
        
        # 变量
        self.raw_dir_var = tk.StringVar()
        self.jpg_dir_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.results_text = tk.StringVar()
        self.matched_raw_files = []
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 开发者菜单
        dev_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="开发者", menu=dev_menu)
        dev_menu.add_command(label="显示详细信息", command=self.show_dev_info)
        dev_menu.add_command(label="清空结果", command=self.clear_results)
        dev_menu.add_command(label="重置设置", command=self.reset_settings)
        dev_menu.add_separator()
        dev_menu.add_command(label="退出", command=self.root.quit)
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 目录选择区域
        dir_frame = ttk.LabelFrame(main_frame, text="目录设置", padding="10")
        dir_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dir_frame, text="RAW文件目录:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(dir_frame, textvariable=self.raw_dir_var, width=60).grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Button(dir_frame, text="浏览", command=self.browse_raw_directory).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(dir_frame, text="JPEG文件目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(dir_frame, textvariable=self.jpg_dir_var, width=60).grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Button(dir_frame, text="浏览", command=self.browse_jpg_directory).grid(row=1, column=2, padx=5, pady=5)
        
        ttk.Label(dir_frame, text="输出目录:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=60).grid(row=2, column=1, sticky=tk.W, pady=5)
        ttk.Button(dir_frame, text="浏览", command=self.browse_output_directory).grid(row=2, column=2, padx=5, pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="扫描文件", command=self.scan_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="移动匹配的RAW文件", command=self.move_raw_files).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="匹配结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
    
    def browse_raw_directory(self):
        directory = filedialog.askdirectory(title="选择RAW文件目录")
        if directory:
            self.raw_dir_var.set(directory)
    
    def browse_jpg_directory(self):
        directory = filedialog.askdirectory(title="选择JPEG文件目录")
        if directory:
            self.jpg_dir_var.set(directory)
    
    def browse_output_directory(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir_var.set(directory)
    
    def get_files_by_extension(self, directory, extensions):
        """获取指定目录下指定扩展名的文件"""
        files = {}
        for ext in extensions:
            for file_path in Path(directory).rglob(f"*{ext}"):
                base_name = file_path.stem
                files[base_name] = file_path
        return files
    
    def scan_files(self):
        raw_dir = self.raw_dir_var.get()
        jpg_dir = self.jpg_dir_var.get()
        
        if not raw_dir:
            messagebox.showerror("错误", "请选择RAW文件目录")
            return
        
        if not jpg_dir:
            messagebox.showerror("错误", "请选择JPEG文件目录")
            return
        
        if not os.path.exists(raw_dir):
            messagebox.showerror("错误", f"RAW目录 '{raw_dir}' 不存在")
            return
        
        if not os.path.exists(jpg_dir):
            messagebox.showerror("错误", f"JPEG目录 '{jpg_dir}' 不存在")
            return
        
        # 获取RAW和JPG文件
        raw_files = self.get_files_by_extension(raw_dir, self.raw_extensions)
        jpg_files = self.get_files_by_extension(jpg_dir, self.jpg_extensions)
        
        # 分析结果
        results = []
        results.append(f"RAW文件目录: {raw_dir}")
        results.append(f"JPEG文件目录: {jpg_dir}")
        results.append(f"找到 {len(raw_files)} 个RAW文件")
        results.append(f"找到 {len(jpg_files)} 个JPG文件")
        results.append("\n=== 匹配结果 ===")
        
        # 检查每个JPG文件是否有对应的RAW文件
        jpg_with_raw = 0
        jpg_without_raw = []
        self.matched_raw_files = []
        
        for jpg_name, jpg_path in jpg_files.items():
            if jpg_name in raw_files:
                jpg_with_raw += 1
                results.append(f"✓ JPG文件 '{jpg_path.name}' 有对应的RAW文件: '{raw_files[jpg_name].name}'")
                self.matched_raw_files.append(raw_files[jpg_name])
            else:
                jpg_without_raw.append(jpg_path.name)
                results.append(f"✗ JPG文件 '{jpg_path.name}' 没有对应的RAW文件")
        
        results.append("\n=== 总结 ===")
        results.append(f"有 {jpg_with_raw} 个JPG文件找到了对应的RAW文件")
        results.append(f"有 {len(jpg_without_raw)} 个JPG文件没有找到对应的RAW文件")
        
        if jpg_without_raw:
            results.append("\n=== 没有对应RAW文件的JPG列表 ===")
            for jpg_name in jpg_without_raw:
                results.append(f"- {jpg_name}")
        
        # 检查是否有RAW文件没有对应的JPG文件
        raw_without_jpg = []
        for raw_name, raw_path in raw_files.items():
            if raw_name not in jpg_files:
                raw_without_jpg.append(raw_path.name)
        
        if raw_without_jpg:
            results.append("\n=== 没有对应JPG文件的RAW列表 ===")
            for raw_name in raw_without_jpg:
                results.append(f"- {raw_name}")
        
        # 显示结果
        output_text = '\n'.join(results)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, output_text)
    
    def move_raw_files(self):
        output_dir = self.output_dir_var.get()
        if not output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"创建输出目录失败: {e}")
                return
        
        if not self.matched_raw_files:
            messagebox.showinfo("信息", "没有找到匹配的RAW文件")
            return
        
        # 移动文件
        moved_count = 0
        for raw_file in self.matched_raw_files:
            try:
                dest_path = os.path.join(output_dir, raw_file.name)
                shutil.copy2(raw_file, dest_path)  # 使用copy2保留文件元数据
                moved_count += 1
            except Exception as e:
                messagebox.showerror("错误", f"移动文件 {raw_file.name} 失败: {e}")
                continue
        
        messagebox.showinfo("完成", f"成功移动 {moved_count} 个RAW文件到 {output_dir}")
    
    def show_dev_info(self):
        """显示开发者信息"""
        info = "RAW和JPG文件自动核对工具 v1.0\n"
        info += "开发者：福橘Mikan\n"
        info += "版本：1.0\n"
        info += "日期：2026-04-02\n"
        info += "功能：自动核对RAW和JPEG文件并移动匹配的RAW文件\n"
        messagebox.showinfo("开发者信息", info)
    
    def clear_results(self):
        """清空结果显示"""
        self.result_text.delete(1.0, tk.END)
    
    def reset_settings(self):
        """重置所有设置"""
        self.raw_dir_var.set("")
        self.jpg_dir_var.set("")
        self.output_dir_var.set("")
        self.result_text.delete(1.0, tk.END)
        self.matched_raw_files = []
        messagebox.showinfo("信息", "设置已重置")

def get_files_by_extension(directory, extensions):
    """获取指定目录下指定扩展名的文件"""
    files = {}
    for ext in extensions:
        for file_path in Path(directory).rglob(f"*{ext}"):
            base_name = file_path.stem
            files[base_name] = file_path
    return files

def main():
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        # 命令行模式
        parser = argparse.ArgumentParser(description='RAW和JPG文件自动核对工具')
        parser.add_argument('directory', nargs='?', default='.', help='要扫描的目录（默认为当前目录）')
        parser.add_argument('--raw-ext', nargs='+', default=['.CR2', '.NEF', '.ARW', '.DNG', '.CR3', '.ORF', '.RAF', '.PEF', '.SRF', '.SR2', '.X3F'], 
                            help='RAW文件扩展名列表（默认为常见相机厂商的RAW格式）')
        parser.add_argument('--jpg-ext', nargs='+', default=['.JPG', '.JPEG', '.jpg', '.jpeg'], 
                            help='JPG文件扩展名列表')
        parser.add_argument('--output', '-o', help='输出结果到指定文件')
        
        args = parser.parse_args()
        directory = args.directory
        
        # 确保目录存在
        if not os.path.exists(directory):
            print(f"错误：目录 '{directory}' 不存在")
            sys.exit(1)
        
        # 获取RAW和JPG文件
        raw_files = get_files_by_extension(directory, args.raw_ext)
        jpg_files = get_files_by_extension(directory, args.jpg_ext)
        
        # 分析结果
        results = []
        results.append(f"扫描目录: {directory}")
        results.append(f"找到 {len(raw_files)} 个RAW文件")
        results.append(f"找到 {len(jpg_files)} 个JPG文件")
        results.append("\n=== 匹配结果 ===")
        
        # 检查每个JPG文件是否有对应的RAW文件
        jpg_with_raw = 0
        jpg_without_raw = []
        
        for jpg_name, jpg_path in jpg_files.items():
            if jpg_name in raw_files:
                jpg_with_raw += 1
                results.append(f"✓ JPG文件 '{jpg_path.name}' 有对应的RAW文件: '{raw_files[jpg_name].name}'")
            else:
                jpg_without_raw.append(jpg_path.name)
                results.append(f"✗ JPG文件 '{jpg_path.name}' 没有对应的RAW文件")
        
        results.append("\n=== 总结 ===")
        results.append(f"有 {jpg_with_raw} 个JPG文件找到了对应的RAW文件")
        results.append(f"有 {len(jpg_without_raw)} 个JPG文件没有找到对应的RAW文件")
        
        if jpg_without_raw:
            results.append("\n=== 没有对应RAW文件的JPG列表 ===")
            for jpg_name in jpg_without_raw:
                results.append(f"- {jpg_name}")
        
        # 检查是否有RAW文件没有对应的JPG文件
        raw_without_jpg = []
        for raw_name, raw_path in raw_files.items():
            if raw_name not in jpg_files:
                raw_without_jpg.append(raw_path.name)
        
        if raw_without_jpg:
            results.append("\n=== 没有对应JPG文件的RAW列表 ===")
            for raw_name in raw_without_jpg:
                results.append(f"- {raw_name}")
        
        # 输出结果
        output_text = '\n'.join(results)
        print(output_text)
        
        # 如果指定了输出文件，将结果写入文件
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"\n结果已保存到: {args.output}")
    else:
        # GUI模式
        root = tk.Tk()
        app = RawJpgCheckerGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
