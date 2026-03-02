import os
import tkinter as tk
from tkinter import filedialog, messagebox, END
from tkinter import ttk
import sys
import platform

def exit_program():
    """退出整个程序"""
    sys.exit()

def rename_selected_files():
    """重命名选中的文件"""
    selected_files = [file_listbox.get(i) for i in file_listbox.curselection()]
    old_string = old_string_entry.get()
    new_string = new_string_entry.get()
    delete_string = delete_string_entry.get()

    if not old_string or not new_string:
        messagebox.showwarning("警告", "请输入要替换的字符串和新字符串。")
        return

    for filename in selected_files:
        old_file_path = os.path.join(folder_path, filename)
        new_filename = filename.replace(old_string, new_string)
        new_filename = new_filename.replace(delete_string, "")
        new_file_path = os.path.join(folder_path, new_filename)
        try:
            os.rename(old_file_path, new_file_path)
        except Exception as e:
            messagebox.showerror("错误", f"重命名文件 {filename} 时出错：{e}")
        else:
            print(f"将文件名 {filename} 替换为 {new_filename}")

    messagebox.showinfo("完成", "文件重命名完成。")

def select_folder_and_show_files():
    """选择文件夹并显示文件"""
    global folder_path
    folder_path = filedialog.askdirectory(title="选择文件夹")
    if not folder_path:
        return

    file_listbox.delete(0, END)
    file_types_set.clear()  # 清空文件类型集合
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            file_listbox.insert(END, filename)
            # 提取文件扩展名并添加到集合
            file_extension = os.path.splitext(filename)[1]
            if file_extension:
                file_types_set.add(file_extension)

    # 更新文件类型按钮
    update_file_type_buttons()

    # 更新状态栏
    status_var.set(f"已加载 {file_listbox.size()} 个文件")

def show_instructions():
    """显示工具使用说明"""
    instructions = (
        "文件批量改名工具使用说明：\n\n",
        "1. 点击'选择文件夹'按钮，选择需要批量改名的文件所在的文件夹。\n",
        "2. 在输入框中输入要替换的字符串、新的字符串以及要删除的字符。\n",
        "3. 选中需要改名的文件，点击\"重命名选中的文件\"按钮。\n",
        "4. 工具会自动批量修改文件名。\n\n",
        "注意：\n",
        "- 请确保输入的字符串正确无误。\n",
        "- 如果遇到问题，请检查文件权限或联系开发者2195786717@qq.com。"
    )
    messagebox.showinfo("使用说明", instructions)

def update_file_type_buttons():
    """根据文件类型动态生成按钮"""
    for widget in file_type_frame.winfo_children():
        widget.destroy()  # 清空之前的按钮

    selected_file_types.clear()  # 清空选中的文件类型
    for file_type in sorted(file_types_set):
        btn = tk.Button(
            file_type_frame, 
            text=file_type, 
            command=lambda ft=file_type: toggle_file_type_selection(ft),
            bg="#f0f0f0",
            fg="#333333",
            font=("Segoe UI", 9),
            relief="ridge",
            bd=1,
            padx=5,
            pady=3,
            activebackground="#e0e0e0",
            activeforeground="#000000"
        )
        btn.pack(pady=2, fill=tk.X, padx=5)

    # 更新文件列表框背景色
    update_file_colors()

def toggle_file_type_selection(file_type):
    """切换文件类型的选中状态"""
    if file_type in selected_file_types:
        selected_file_types.remove(file_type)
    else:
        selected_file_types.add(file_type)

    # 更新文件列表框背景色
    update_file_colors()

def update_file_colors():
    """根据选中的文件类型更新文件列表框中的背景颜色和选中状态"""
    # 先清除所有选中状态
    file_listbox.selection_clear(0, END)

    for idx, filename in enumerate(file_listbox.get(0, END)):
        file_extension = os.path.splitext(filename)[1]
        if file_extension in selected_file_types:
            file_listbox.itemconfig(idx, bg="#E8F4FD")  # 设置选中的文件背景为浅蓝色
            file_listbox.selection_set(idx)  # 选中该文件
        else:
            file_listbox.itemconfig(idx, bg="white")  # 恢复未选中的文件背景为白色

# 初始化全选状态变量
is_all_selected = False

def toggle_select_all_files():
    """切换全选和取消全选状态"""
    global is_all_selected
    if is_all_selected:
        # 取消全选
        file_listbox.selection_clear(0, END)  # 取消所有选中
        for idx in range(file_listbox.size()):
            file_listbox.itemconfig(idx, bg="white")  # 恢复背景色为白色
        select_all_button.config(text="全选", bg=button_bg, fg=button_fg)
        is_all_selected = False
    else:
        # 全选
        file_listbox.select_set(0, END)  # 选中所有文件
        for idx in range(file_listbox.size()):
            file_listbox.itemconfig(idx, bg="#E8F4FD")  # 设置背景色为浅蓝色
        select_all_button.config(text="取消全选", bg="#5CB3FF", fg="white")
        is_all_selected = True

def change_theme(event):
    """更改界面主题"""
    selected_theme = theme_combobox.get()
    style.theme_use(selected_theme)

    # 根据主题更新颜色
    if selected_theme == "clam":
        update_colors("#f0f0f0", "#333333", "#ffffff", "#4285F4", "#ffffff")
    elif selected_theme == "alt":
        update_colors("#f0f0f0", "#333333", "#ffffff", "#4285F4", "#ffffff")
    elif selected_theme == "default":
        update_colors("#f0f0f0", "#333333", "#ffffff", "#4285F4", "#ffffff")
    elif selected_theme == "classic":
        update_colors("#f0f0f0", "#333333", "#ffffff", "#4285F4", "#ffffff")

    # 重新应用字体样式
    style.configure("TLabel", font=("Segoe UI", 10), background=bg_color)
    style.configure("TButton", font=("Segoe UI", 10), background=button_bg, foreground=button_fg)
    style.configure("TEntry", font=("Segoe UI", 10), fieldbackground="white")
    style.configure("TCombobox", font=("Segoe UI", 10), fieldbackground="white")

def update_colors(bg, fg, entry_bg, button_bg, button_fg):
    """更新界面颜色"""
    global bg_color, fg_color, button_bg_color, button_fg_color
    bg_color = bg
    fg_color = fg
    button_bg_color = button_bg
    button_fg_color = button_fg

    root.configure(bg=bg_color)

    # 更新框架背景
    for frame in [top_frame, main_frame, button_frame, status_frame, file_type_frame]:
        frame.configure(bg=bg_color)

    # 更新标签背景
    for label in [old_string_label, new_string_label, delete_string_label, theme_label]:
        label.configure(bg=bg_color, fg=fg_color)

    # 更新按钮
    select_folder_button.configure(bg=button_bg, fg=button_fg)
    rename_button.configure(bg=button_bg, fg=button_fg)
    select_all_button.configure(bg=button_bg, fg=button_fg)
    instructions_button.configure(bg=button_bg, fg=button_fg)

def create_rounded_button(parent, text, command, bg="#4285F4", fg="white", width=15, height=1):
    """创建圆角按钮"""
    btn = tk.Button(
        parent, 
        text=text, 
        command=command,
        bg=bg,
        fg=fg,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=15,
        pady=8,
        width=width,
        height=height,
        cursor="hand2"
    )
    return btn

def add_hover_effect(button, bg_color="#4285F4", hover_color="#3367D6"):
    """添加悬停效果"""
    def on_enter(e):
        button['background'] = hover_color

    def on_leave(e):
        button['background'] = bg_color

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

# 创建主窗口
root = tk.Tk()
root.title("音符文件批量改名工具 - 美化版")
root.geometry("900x600")  # 调整窗口大小
root.minsize(800, 500)  # 设置最小窗口大小

# 初始化颜色
bg_color = "#F5F7FA"
fg_color = "#333333"
button_bg = "#4285F4"
button_fg = "white"

root.configure(bg=bg_color)

# 使用 ttk.Style 设置样式
style = ttk.Style()
style.theme_use("clam")  # 默认主题为 "clam"

# 创建顶部框架 - 用于标题
top_frame = tk.Frame(root, bg="#4285F4", height=60)
top_frame.pack(fill=tk.X, padx=0, pady=0)
top_frame.pack_propagate(False)  # 禁止框架根据内容调整大小

# 添加标题
title_label = tk.Label(
    top_frame, 
    text="INF文件批量改名工具", 
    font=("Segoe UI", 18, "bold"),
    bg="#4285F4",
    fg="white"
)
title_label.pack(pady=15)

# 创建主框架
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# 创建左侧输入区域
input_frame = tk.Frame(main_frame, bg=bg_color)
input_frame.pack(fill=tk.X, padx=5, pady=5)

# 创建标签和输入框 - 使用更现代的布局
old_string_label = tk.Label(
    input_frame, 
    text="要替换的字符串：", 
    font=("Segoe UI", 11),
    bg=bg_color,
    fg=fg_color
)
old_string_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")

old_string_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
old_string_entry.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

new_string_label = tk.Label(
    input_frame, 
    text="新的字符串：", 
    font=("Segoe UI", 11),
    bg=bg_color,
    fg=fg_color
)
new_string_label.grid(row=1, column=0, padx=10, pady=8, sticky="w")

new_string_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
new_string_entry.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

delete_string_label = tk.Label(
    input_frame, 
    text="要删除的字符：", 
    font=("Segoe UI", 11),
    bg=bg_color,
    fg=fg_color
)
delete_string_label.grid(row=2, column=0, padx=10, pady=8, sticky="w")

delete_string_entry = ttk.Entry(input_frame, font=("Segoe UI", 10))
delete_string_entry.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

# 创建中间区域 - 文件列表和文件类型按钮
middle_frame = tk.Frame(main_frame, bg=bg_color)
middle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# 创建文件列表框架
list_frame = tk.Frame(middle_frame, bg=bg_color)
list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

# 添加文件列表标题
list_title = tk.Label(
    list_frame,
    text="文件列表",
    font=("Segoe UI", 12, "bold"),
    bg=bg_color,
    fg=fg_color
)
list_title.pack(anchor="w", padx=5, pady=(0, 5))

# 创建带滚动条的文件列表框
list_scroll_frame = tk.Frame(list_frame, bg=bg_color)
list_scroll_frame.pack(fill=tk.BOTH, expand=True)

file_listbox = tk.Listbox(
    list_scroll_frame,
    selectmode='multiple',
    font=("Segoe UI", 10),
    bg="white",
    selectbackground="#5CB3FF",
    activestyle="none"
)

# 添加垂直滚动条
v_scrollbar = ttk.Scrollbar(list_scroll_frame, orient="vertical", command=file_listbox.yview)
file_listbox.configure(yscrollcommand=v_scrollbar.set)

v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建文件类型按钮区域
file_type_frame = tk.Frame(middle_frame, bg=bg_color, width=200)
file_type_frame.pack(side=tk.RIGHT, fill=tk.Y)
file_type_frame.pack_propagate(False)  # 保持固定宽度

# 添加文件类型标题
type_title = tk.Label(
    file_type_frame,
    text="文件类型筛选",
    font=("Segoe UI", 12, "bold"),
    bg=bg_color,
    fg=fg_color
)
type_title.pack(anchor="w", padx=5, pady=(0, 5))

# 创建按钮框架
button_frame = tk.Frame(main_frame, bg=bg_color)
button_frame.pack(fill=tk.X, padx=5, pady=10)

# 创建美化按钮
select_folder_button = create_rounded_button(
    button_frame, 
    "选择文件夹", 
    select_folder_and_show_files,
    bg="#34A853"
)
select_folder_button.pack(side=tk.LEFT, padx=5)
add_hover_effect(select_folder_button, "#34A853", "#2E8B47")

rename_button = create_rounded_button(
    button_frame, 
    "重命名选中的文件", 
    rename_selected_files
)
rename_button.pack(side=tk.LEFT, padx=5)
add_hover_effect(rename_button)

select_all_button = create_rounded_button(
    button_frame, 
    "全选", 
    toggle_select_all_files,
    bg="#FBBC05",
    fg="#333333"
)
select_all_button.pack(side=tk.LEFT, padx=5)
add_hover_effect(select_all_button, "#FBBC05", "#F9AB00")

instructions_button = create_rounded_button(
    button_frame, 
    "使用说明", 
    show_instructions,
    bg="#EA4335"
)
instructions_button.pack(side=tk.LEFT, padx=5)
add_hover_effect(instructions_button, "#EA4335", "#D23121")

# 创建底部区域
bottom_frame = tk.Frame(main_frame, bg=bg_color)
bottom_frame.pack(fill=tk.X, padx=5, pady=5)

# 添加主题选择
theme_label = tk.Label(
    bottom_frame,
    text="选择界面主题：",
    font=("Segoe UI", 10),
    bg=bg_color,
    fg=fg_color
)
theme_label.pack(side=tk.LEFT, padx=5)

theme_combobox = ttk.Combobox(
    bottom_frame, 
    values=style.theme_names(), 
    state="readonly",
    font=("Segoe UI", 10)
)
theme_combobox.pack(side=tk.LEFT, padx=5)
theme_combobox.set("vista")  # 设置默认主题为 "clam"
theme_combobox.bind("<<ComboboxSelected>>", change_theme)

# 创建状态栏
status_frame = tk.Frame(root, bg="#E0E0E0", height=25)
status_frame.pack(fill=tk.X, side=tk.BOTTOM)
status_frame.pack_propagate(False)  # 禁止框架根据内容调整大小

status_var = tk.StringVar()
status_var.set("就绪")

status_label = tk.Label(
    status_frame,
    textvariable=status_var,
    font=("Segoe UI", 9),
    bg="#E0E0E0",
    fg="#555555",
    anchor="w"
)
status_label.pack(side=tk.LEFT, padx=10)

# 调整输入框列权重
input_frame.columnconfigure(1, weight=1)

# 初始化文件类型集合和变量
file_types_set = set()
selected_file_types = set()
folder_path = ""

# 运行主循环
root.mainloop()
