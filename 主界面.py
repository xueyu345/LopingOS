import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import sys as s
import os as o
import time as t

# 添加数据库模块路径
s.path.append(o.path.join(o.path.dirname(__file__), '..', '注册', 'database'))

# 导入数据库模块
try:
    from user_db import get_db
except ImportError:
    print("导入数据库模块失败")
    get_db = None

# 尝试导入Torch库
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# 导入爬虫模块
try:
    s.path.append(o.path.join(o.path.dirname(__file__), '..', '配置', '其他功能'))
    from TS import WebCrawlerGUI
    CRAWLER_AVAILABLE = True
except ImportError:
    print("导入爬虫模块失败")
    CRAWLER_AVAILABLE = False

# 用户数据管理函数
def load_users_data():
    """加载用户数据"""
    # 现在使用数据库，不需要从文件加载
    pass

def save_users_data():
    """保存用户数据"""
    # 现在使用数据库，不需要保存到文件
    pass

# 检查用户是否存在
def user_exists(username):
    """检查用户是否存在"""
    if get_db:
        db = get_db()
        return db.get_user(username) is not None
    return username.lower() in users_data

# 验证用户密码
def verify_user(username, password):
    """验证用户密码"""
    if get_db:
        db = get_db()
        return db.verify_user(username, password)
    username_lower = username.lower()
    if username_lower in users_data:
        return users_data[username_lower]["password"] == password
    return False

# 注册新用户
def register_user(username, password, fullname, email):
    """注册新用户"""
    if get_db:
        db = get_db()
        return db.add_user(username, password, fullname, email)
    
    # 备用方案：使用内存存储
    username_lower = username.lower()
    if username_lower in users_data:
        return False, "用户名已存在"
    
    users_data[username_lower] = {
        "password": password,
        "fullname": fullname,
        "email": email,
        "role": "user"
    }
    
    return True, "注册成功"

# Windows风格按钮创建函数
def create_windows_button(parent, text="Button", bg="#0078D4", fg="white", 
                         font=(), command=None, padx=5, pady=5, 
                         width=None, height=None):
    """创建Windows风格的按钮（无边框，有悬停效果）"""
    button = tk.Button(parent, text=text, bg=bg, fg=fg, font=font, 
                      relief=tk.FLAT, bd=0, command=command, 
                      width=width, height=height)
    
    # 添加悬停效果
    def on_enter(event):
        if bg == "#0078D4":  # 蓝色按钮
            button.config(bg="#106ebe")
        elif bg == "#4CAF50":  # 绿色按钮
            button.config(bg="#43a047")
        elif bg == "#f44336":  # 红色按钮
            button.config(bg="#e53935")
        elif bg == "#1f1f1f":  # 任务栏按钮
            button.config(bg="#323232")
        elif bg == "#0c0c0c":  # 终端按钮
            button.config(bg="#1e1e1e")
        elif bg == "#000080":  # 窗口标题栏按钮
            button.config(bg="#1a2b5a")
        else:
            # 浅色按钮
            button.config(bg="#e0e0e0")
    
    def on_leave(event):
        button.config(bg=bg)
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    
    return button

print('hello , It‘s LopingsOS')
print('you can inthe terminal by typing "terminal"')

o.environ["-v"] = '1.0.0'
o.environ["-shell"] = 'LopingsOS'
o.environ['users'] = 'guest'
o.environ['password'] = 'guest'

# 用户数据存储
users_data = {
    "guest": {
        "password": "guest",
        "fullname": "Guest User",
        "email": "guest@lopingos.com",
        "role": "user"
    }
}

# 用户数据文件路径
USERS_DATA_FILE = "users.json"

open = False
open1 = True

root = tk.Tk()
root.title("LopingsOS")
root.geometry("1024x768")
root.resizable(True, True)

# 加载用户数据
load_users_data()

desktop = tk.Frame(root, bg="#0078D7")
desktop.pack(fill=tk.BOTH, expand=True)

desktop_bg = tk.Canvas(desktop, bg="#0078D7", highlightthickness=0)
desktop_bg.place(x=0, y=0, relwidth=1, relheight=1)

def create_desktop_background():
    desktop_bg.delete("all")
    width = desktop.winfo_width()
    height = desktop.winfo_height()
    
    for i in range(height):
        color_intensity = int(120 + (i / height) * 30)
        color = f"#{0:02x}{color_intensity:02x}{215:02x}"
        desktop_bg.create_line(0, i, width, i, fill=color)

desktop.after(100, create_desktop_background)

context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="刷新", command=lambda: refresh_desktop())
context_menu.add_separator()
context_menu.add_command(label="新建文件夹", command=lambda: create_new_folder())
context_menu.add_command(label="新建文本文档", command=lambda: create_new_text_file())
context_menu.add_separator()
context_menu.add_command(label="属性", command=lambda: show_properties())

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

desktop.bind("<Button-3>", show_context_menu)

def refresh_desktop():
    print("桌面已刷新")

def create_new_folder():
    dialog = tk.Toplevel(root)
    dialog.title("新建文件夹")
    dialog.geometry("400x150")
    dialog.transient(root)
    dialog.grab_set()
    
    dialog_frame = tk.Frame(dialog, bg="white")
    dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(dialog_frame, text="文件夹名称:", font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=5)
    
    folder_name_entry = tk.Entry(dialog_frame, font=("Arial", 10))
    folder_name_entry.pack(fill=tk.X, pady=5)
    folder_name_entry.insert(0, "新建文件夹")
    folder_name_entry.select_range(0, tk.END)
    folder_name_entry.focus()
    
    def on_create():
        folder_name = folder_name_entry.get().strip()
        if folder_name:
            existing_names = [icon[0] for icon in desktop_icons] + [file["name"] for file in desktop_files]
            if folder_name not in existing_names:
                file_data = {
                    "name": folder_name,
                    "icon": "📁",
                    "type": "文件夹",
                    "size": ""
                }
                desktop_files.append(file_data)
                create_desktop_file_icon(file_data)
                dialog.destroy()
            else:
                messagebox.showwarning("警告", "该文件夹已存在！")
        else:
            messagebox.showwarning("警告", "请输入文件夹名称！")
    
    def on_cancel():
        dialog.destroy()
    
    button_frame = tk.Frame(dialog_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=10)
    
    tk.Button(button_frame, text="创建", bg="#4CAF50", fg="white", width=10, command=on_create).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="取消", bg="#f0f0f0", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)
    
    folder_name_entry.bind("<Return>", lambda e: on_create())
    folder_name_entry.bind("<Escape>", lambda e: on_cancel())

def create_new_text_file():
    print("新建文本文档")
    create_notepad_window()

def show_properties():
    print("显示属性")
    create_window("桌面属性")

taskbar = tk.Frame(root, bg="#1f1f1f", height=48)
taskbar.pack(side=tk.BOTTOM, fill=tk.X)
taskbar.pack_propagate(False)

taskbar_bg = tk.Canvas(taskbar, bg="#1f1f1f", highlightthickness=0)
taskbar_bg.place(x=0, y=0, relwidth=1, relheight=1)

start_button = create_windows_button(taskbar, text="⊞", bg="#1f1f1f", fg="white", 
                                   font=("Segoe UI", 16), command=lambda: toggle_start_menu())
start_button.pack(side=tk.LEFT, padx=8, pady=8)

search_frame = tk.Frame(taskbar, bg="#1f1f1f")
search_frame.pack(side=tk.LEFT, padx=8, pady=8)

search_entry = tk.Entry(search_frame, width=30, bg="#323232", fg="white", 
                      relief=tk.FLAT, bd=0, font=("Segoe UI", 9), insertbackground="white")
search_entry.pack(side=tk.LEFT, padx=5, pady=5)
search_entry.insert(0, "🔍  搜索")
search_entry.config(fg="#999999")

def search_entry_focus_in(event):
    if search_entry.get() == "🔍  搜索":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="white")

def search_entry_focus_out(event):
    if not search_entry.get():
        search_entry.insert(0, "🔍  搜索")
        search_entry.config(fg="#999999")

search_entry.bind("<FocusIn>", search_entry_focus_in)
search_entry.bind("<FocusOut>", search_entry_focus_out)
search_entry.bind("<Return>", lambda e: on_search())

time_label = tk.Label(taskbar, text="", bg="#1f1f1f", fg="white", font=("Segoe UI", 9))
time_label.pack(side=tk.RIGHT, padx=8, pady=8)

wifi_status = {"connected": False, "network": ""}

wifi_frame = tk.Frame(taskbar, bg="#1f1f1f")
wifi_frame.pack(side=tk.RIGHT, padx=8, pady=8)

wifi_icon = tk.Label(wifi_frame, text="📶", bg="#1f1f1f", fg="white", font=("Segoe UI", 12))
wifi_icon.pack(side=tk.LEFT)

wifi_label = tk.Label(wifi_frame, text="未连接", bg="#1f1f1f", fg="white", font=("Segoe UI", 9))
wifi_label.pack(side=tk.LEFT, padx=5)

def show_wifi_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("WiFi设置")
    dialog.geometry("400x300")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    dialog_frame = tk.Frame(dialog, bg="#2d2d2d")
    dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(dialog_frame, text="可用网络", font=("Segoe UI", 12, "bold"), bg="#2d2d2d", fg="white").pack(pady=10)
    
    networks_frame = tk.Frame(dialog_frame, bg="#3d3d3d")
    networks_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    networks = [
        ("Home-WiFi", "🔒", "强"),
        ("Office-Network", "🔒", "中"),
        ("Guest-WiFi", "🔓", "弱"),
        ("Coffee-Shop", "🔓", "弱")
    ]
    
    network_list = ttk.Treeview(networks_frame, columns=("name", "signal", "lock"), show="headings", selectmode="browse")
    network_list.heading("name", text="网络名称")
    network_list.heading("signal", text="信号")
    network_list.heading("lock", text="")
    
    network_list.column("name", width=200)
    network_list.column("signal", width=80)
    network_list.column("lock", width=40)
    
    for name, lock, signal in networks:
        network_list.insert("", "end", values=(name, signal, lock))
    
    network_scrollbar = ttk.Scrollbar(networks_frame, orient=tk.VERTICAL, command=network_list.yview)
    network_list.configure(yscrollcommand=network_scrollbar.set)
    
    network_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    network_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def connect_network():
        selection = network_list.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要连接的网络")
            return
        
        item = network_list.item(selection[0])
        network_name = item["values"][0]
        
        wifi_status["connected"] = True
        wifi_status["network"] = network_name
        update_wifi_display()
        messagebox.showinfo("连接成功", f"已连接到 {network_name}")
        dialog.destroy()
    
    connect_btn = tk.Button(dialog_frame, text="连接", bg="#0078D4", fg="white", font=("Segoe UI", 10), command=connect_network)
    connect_btn.pack(pady=10)
    
    def disconnect_network():
        wifi_status["connected"] = False
        wifi_status["network"] = ""
        update_wifi_display()
        messagebox.showinfo("断开连接", "已断开WiFi连接")
        dialog.destroy()
    
    disconnect_btn = tk.Button(dialog_frame, text="断开", bg="#d13438", fg="white", font=("Segoe UI", 10), command=disconnect_network)
    disconnect_btn.pack(pady=5)

def update_wifi_display():
    if wifi_status["connected"]:
        wifi_icon.config(text="📶")
        wifi_label.config(text=wifi_status["network"])
    else:
        wifi_icon.config(text="📴")
        wifi_label.config(text="未连接")

wifi_frame.bind("<Button-1>", lambda e: show_wifi_dialog())

volume_status = {"muted": False, "level": 75}

volume_frame = tk.Frame(taskbar, bg="#1f1f1f")
volume_frame.pack(side=tk.RIGHT, padx=8, pady=8)

volume_icon = tk.Label(volume_frame, text="🔊", bg="#1f1f1f", fg="white", font=("Segoe UI", 12))
volume_icon.pack(side=tk.LEFT)

volume_label = tk.Label(volume_frame, text="75%", bg="#1f1f1f", fg="white", font=("Segoe UI", 9))
volume_label.pack(side=tk.LEFT, padx=5)

def show_volume_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("音量控制")
    dialog.geometry("300x200")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    dialog_frame = tk.Frame(dialog, bg="#2d2d2d")
    dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(dialog_frame, text="音量控制", font=("Segoe UI", 12, "bold"), bg="#2d2d2d", fg="white").pack(pady=10)
    
    volume_scale = tk.Scale(dialog_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                            bg="#2d2d2d", fg="white", length=200, command=lambda v: update_volume(int(v)))
    volume_scale.set(volume_status["level"])
    volume_scale.pack(pady=10)
    
    def toggle_mute():
        volume_status["muted"] = not volume_status["muted"]
        update_volume_display()
        if volume_status["muted"]:
            volume_scale.set(0)
        else:
            volume_scale.set(volume_status["level"])
    
    mute_btn = tk.Button(dialog_frame, text="静音/取消静音", bg="#0078D4", fg="white", font=("Segoe UI", 10),
                        command=toggle_mute)
    mute_btn.pack(pady=10)
    
    def on_ok():
        dialog.destroy()
    
    tk.Button(dialog_frame, text="确定", bg="#3d3d3d", fg="white", font=("Segoe UI", 10), command=on_ok).pack(pady=5)

def update_volume(level):
    volume_status["level"] = level
    if level == 0:
        volume_status["muted"] = True
    else:
        volume_status["muted"] = False
    update_volume_display()

def update_volume_display():
    if volume_status["muted"]:
        volume_icon.config(text="🔇")
        volume_label.config(text="静音")
    else:
        volume_icon.config(text="🔊")
        volume_label.config(text=f"{volume_status['level']}%")

volume_frame.bind("<Button-1>", lambda e: show_volume_dialog())

battery_status = {"level": 85, "charging": False}

battery_frame = tk.Frame(taskbar, bg="#1f1f1f")
battery_frame.pack(side=tk.RIGHT, padx=8, pady=8)

battery_icon = tk.Label(battery_frame, text="🔋", bg="#1f1f1f", fg="white", font=("Segoe UI", 12))
battery_icon.pack(side=tk.LEFT)

battery_label = tk.Label(battery_frame, text="85%", bg="#1f1f1f", fg="white", font=("Segoe UI", 9))
battery_label.pack(side=tk.LEFT, padx=5)

def show_battery_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("电池状态")
    dialog.geometry("300x200")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    dialog_frame = tk.Frame(dialog, bg="#2d2d2d")
    dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(dialog_frame, text="电池状态", font=("Segoe UI", 12, "bold"), bg="#2d2d2d", fg="white").pack(pady=10)
    
    status_text = "充电中" if battery_status["charging"] else "使用电池"
    tk.Label(dialog_frame, text=f"状态: {status_text}", bg="#2d2d2d", fg="white", font=("Segoe UI", 10)).pack(pady=5)
    tk.Label(dialog_frame, text=f"电量: {battery_status['level']}%", bg="#2d2d2d", fg="white", font=("Segoe UI", 10)).pack(pady=5)
    
    def toggle_charging():
        battery_status["charging"] = not battery_status["charging"]
        update_battery_display()
        dialog.destroy()
        show_battery_dialog()
    
    tk.Button(dialog_frame, text="切换充电状态", bg="#0078D4", fg="white", font=("Segoe UI", 10),
              command=toggle_charging).pack(pady=10)
    
    def on_ok():
        dialog.destroy()
    
    tk.Button(dialog_frame, text="确定", bg="#3d3d3d", fg="white", font=("Segoe UI", 10), command=on_ok).pack(pady=5)

def update_battery_display():
    if battery_status["charging"]:
        battery_icon.config(text="⚡")
        battery_label.config(text=f"{battery_status['level']}%")
    else:
        battery_icon.config(text="🔋")
        battery_label.config(text=f"{battery_status['level']}%")

battery_frame.bind("<Button-1>", lambda e: show_battery_dialog())

def update_time():
    current_time = t.strftime("%H:%M:%S")
    current_date = t.strftime("%Y-%m-%d")
    time_label.config(text=f"{current_time}\n{current_date}")
    root.after(1000, update_time)

update_time()

start_menu = tk.Frame(root, bg="#2d2d2d", width=400, height=500)
start_menu_visible = False

def toggle_start_menu():
    global start_menu_visible
    if start_menu_visible:
        start_menu.place_forget()
        start_menu_visible = False
    else:
        start_menu.place(x=0, y=552, anchor="sw")
        start_menu_visible = True

menu_items = [
    ("我的电脑", "💻"),
    ("回收站", "🗑️"),
    ("记事本", "📝"),
    ("计算器", "🔢"),
    ("设置", "⚙️"),
    ("文件资源管理器", "📁"),
    ("下载", "⬇️"),
    ("浏览器", "🌐"),
    ("运行", "▶️"),
    ("任务管理器", "📊"),
    ("终端", "💻"),
    ("Linux", "🐧"),
    ("部署", "🚀"),
    ("AI助手", "🤖"),
    ("用户注册", "👤"),
    ("爬虫", "🕷️")
]

for item, icon in menu_items:
    menu_frame = tk.Frame(start_menu, bg="#2d2d2d")
    menu_frame.pack(fill=tk.X, padx=10, pady=2)
    
    menu_icon = tk.Label(menu_frame, text=icon, bg="#2d2d2d", fg="white", font=("Segoe UI", 16))
    menu_icon.pack(side=tk.LEFT, padx=10, pady=8)
    
    menu_label = tk.Label(menu_frame, text=item, bg="#2d2d2d", fg="white", font=("Segoe UI", 10))
    menu_label.pack(side=tk.LEFT, padx=5, pady=8)
    
    def menu_on_enter(event, frame=menu_frame):
        frame.config(bg="#3d3d3d")
        for child in frame.winfo_children():
            child.config(bg="#3d3d3d")
    
    def menu_on_leave(event, frame=menu_frame):
        frame.config(bg="#2d2d2d")
        for child in frame.winfo_children():
            child.config(bg="#2d2d2d")
    
    menu_frame.bind("<Enter>", menu_on_enter)
    menu_frame.bind("<Leave>", menu_on_leave)
    menu_icon.bind("<Enter>", menu_on_enter)
    menu_icon.bind("<Leave>", menu_on_leave)
    menu_label.bind("<Enter>", menu_on_enter)
    menu_label.bind("<Leave>", menu_on_leave)
    menu_frame.bind("<Button-1>", lambda e, app=item: open_application(app))
    menu_icon.bind("<Button-1>", lambda e, app=item: open_application(app))
    menu_label.bind("<Button-1>", lambda e, app=item: open_application(app))

desktop_icons = [
    ("我的电脑", "💻"),
    ("回收站", "🗑️"),
    ("记事本", "📝"),
    ("计算器", "🔢"),
    ("设置", "⚙️"),
    ("文件资源管理器", "📁"),
    ("下载", "⬇️"),
    ("浏览器", "🌐"),
    ("终端2", "💻"),
    ("Linux", "🐧"),
    ("部署", "🚀"),
    ("AI助手", "🤖"),
    ("爬虫", "🕷️")
]

def open_application(app_name):
    print(f"打开应用程序: {app_name}")
    if app_name == "设置":
        create_settings_window()
    elif app_name == "记事本":
        create_notepad_window()
    elif app_name == "计算器":
        create_calculator_window()
    elif app_name == "我的电脑":
        create_mycomputer_window()
    elif app_name == "回收站":
        create_recyclebin_window()
    elif app_name == "文件资源管理器":
        create_file_explorer_window()
    elif app_name == "下载":
        create_download_window()
    elif app_name == "浏览器":
        create_browser_window()
    elif app_name == "终端":
        create_terminal_window()
    elif app_name == "运行":
        create_run_dialog()
    elif app_name == "任务管理器":
        create_task_manager_window()
    elif app_name == "Linux":
        create_linux_window()
    elif app_name == "部署":
        create_deploy_window()
    elif app_name == "AI助手":
        create_ai_assistant_window()
    elif app_name == "用户注册":
        create_register_window()
    elif app_name == "爬虫":
        create_crawler_window()
    else:
        create_window(app_name)

def create_terminal_window():
    window_frame = tk.Frame(root, bg="#0c0c0c", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=800, height=500)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 100, "y": 50, "width": 800, "height": 500}
    
    title_bar = tk.Frame(window_frame, bg="#0c0c0c", relief=tk.FLAT)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="LopingsOS PowerShell", bg="#0c0c0c", fg="#cccccc", font=("Segoe UI", 10))
    title_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    close_btn = create_windows_button(title_bar, text="×", bg="#0c0c0c", fg="#cccccc", 
                                    font=("Segoe UI", 10), command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    maximize_btn = create_windows_button(title_bar, text="□", bg="#0c0c0c", fg="#cccccc",
                                        font=("Segoe UI", 10), command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    minimize_btn = create_windows_button(title_bar, text="−", bg="#0c0c0c", fg="#cccccc",
                                        font=("Segoe UI", 10), command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    content = tk.Frame(window_frame, bg="#0c0c0c")
    content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    terminal_text = tk.Text(content, bg="#0c0c0c", fg="#cccccc", 
                        font=("Consolas", 11), insertbackground="#cccccc",
                        relief=tk.FLAT, bd=0, wrap=tk.WORD)
    terminal_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    command_history = []
    history_index = -1
    
    def print_output(text, color="#cccccc"):
        terminal_text.insert(tk.END, text + "\n", (color,))
        terminal_text.see(tk.END)
    
    def print_prompt():
        terminal_text.insert(tk.END, "PS C:\\Users\\guest> ", ("prompt",))
        terminal_text.see(tk.END)
        terminal_text.mark_set("input_start", "insert-1c linestart")
    
    terminal_text.tag_config("prompt", foreground="#569cd6")
    terminal_text.tag_config("success", foreground="#4ec9b0")
    terminal_text.tag_config("error", foreground="#f14c4c")
    terminal_text.tag_config("warning", foreground="#dcdcaa")
    terminal_text.tag_config("info", foreground="#9cdcfe")
    
    print_output("LopingsOS PowerShell")
    print_output("Copyright (C) 2024 LopingsOS. All rights reserved.")
    print_output("")
    print_output("欢迎使用 LopingsOS PowerShell！")
    print_output("输入 'help' 查看可用命令。")
    print_output("")
    print_prompt()
    
    commands = {
        "help": {
            "description": "显示所有可用命令的帮助信息",
            "usage": "help [命令名]",
            "examples": ["help", "help dir"],
            "category": "基础"
        },
        "cls": {
            "description": "清除终端屏幕内容",
            "usage": "cls",
            "examples": ["cls"],
            "category": "基础"
        },
        "clear": {
            "description": "清除终端屏幕内容（同 cls）",
            "usage": "clear",
            "examples": ["clear"],
            "category": "基础"
        },
        "exit": {
            "description": "退出终端",
            "usage": "exit",
            "examples": ["exit"],
            "category": "基础"
        },
        "exit-system": {
            "description": "退出系统",
            "usage": "exit-system",
            "examples": ["exit-system"],
            "category": "系统"
        },
        "shutdown": {
            "description": "关闭系统",
            "usage": "shutdown",
            "examples": ["shutdown"],
            "category": "系统"
        },
        "dir": {
            "description": "列出当前目录的文件和文件夹",
            "usage": "dir [路径]",
            "examples": ["dir", "dir C:\\Users"],
            "category": "文件"
        },
        "cd": {
            "description": "更改当前目录",
            "usage": "cd [路径]",
            "examples": ["cd Documents", "cd ..", "cd C:\\"],
            "category": "文件"
        },
        "echo": {
            "description": "显示文本或消息",
            "usage": "echo [文本]",
            "examples": ["echo Hello World", "echo $env:USERNAME"],
            "category": "基础"
        },
        "date": {
            "description": "显示当前日期和时间",
            "usage": "date",
            "examples": ["date"],
            "category": "系统"
        },
        "time": {
            "description": "显示当前时间",
            "usage": "time",
            "examples": ["time"],
            "category": "系统"
        },
        "whoami": {
            "description": "显示当前用户名",
            "usage": "whoami",
            "examples": ["whoami"],
            "category": "系统"
        },
        "hostname": {
            "description": "显示计算机名称",
            "usage": "hostname",
            "examples": ["hostname"],
            "category": "系统"
        },
        "ver": {
            "description": "显示操作系统版本",
            "usage": "ver",
            "examples": ["ver"],
            "category": "系统"
        },
        "calc": {
            "description": "执行数学计算",
            "usage": "calc [表达式]",
            "examples": ["calc 2+2", "calc 10*5", "calc (3+5)*2"],
            "category": "工具"
        },
        "notepad": {
            "description": "打开记事本",
            "usage": "notepad",
            "examples": ["notepad"],
            "category": "应用"
        },
        "calcapp": {
            "description": "打开计算器",
            "usage": "calcapp",
            "examples": ["calcapp"],
            "category": "应用"
        },
        "browser": {
            "description": "打开浏览器",
            "usage": "browser",
            "examples": ["browser"],
            "category": "应用"
        },
        "explorer": {
            "description": "打开文件资源管理器",
            "usage": "explorer",
            "examples": ["explorer"],
            "category": "应用"
        },
        "settings": {
            "description": "打开设置",
            "usage": "settings",
            "examples": ["settings"],
            "category": "应用"
        },
        "taskmgr": {
            "description": "打开任务管理器",
            "usage": "taskmgr",
            "examples": ["taskmgr"],
            "category": "应用"
        },
        "download": {
            "description": "打开下载管理器",
            "usage": "download",
            "examples": ["download"],
            "category": "应用"
        },
        "sysinfo": {
            "description": "显示系统信息",
            "usage": "sysinfo",
            "examples": ["sysinfo"],
            "category": "系统"
        },
        "env": {
            "description": "显示或设置环境变量",
            "usage": "env [变量名] [值]",
            "examples": ["env", "env USERNAME", "env TEST value"],
            "category": "系统"
        },
        "history": {
            "description": "显示命令历史",
            "usage": "history",
            "examples": ["history"],
            "category": "基础"
        },
        "ipconfig": {
            "description": "显示网络配置信息",
            "usage": "ipconfig",
            "examples": ["ipconfig"],
            "category": "网络"
        },
        "ping": {
            "description": "测试网络连接",
            "usage": "ping [地址]",
            "examples": ["ping google.com", "ping 192.168.1.1"],
            "category": "网络"
        }
    }
    
    def show_help(command_name=None):
        if command_name:
            if command_name in commands:
                cmd = commands[command_name]
                print_output(f"\n命令: {command_name}", "info")
                print_output(f"描述: {cmd['description']}", "info")
                print_output(f"用法: {cmd['usage']}", "info")
                print_output(f"示例: {', '.join(cmd['examples'])}", "info")
                print_output(f"类别: {cmd['category']}", "info")
            else:
                print_output(f"\n错误: 未找到命令 '{command_name}'", "error")
                print_output("输入 'help' 查看所有可用命令。", "warning")
        else:
            print_output("\n可用命令:", "info")
            print_output("=" * 50, "info")
            
            categories = {}
            for cmd_name, cmd_info in commands.items():
                category = cmd_info["category"]
                if category not in categories:
                    categories[category] = []
                categories[category].append(cmd_name)
            
            for category in sorted(categories.keys()):
                print_output(f"\n【{category}】", "success")
                for cmd_name in sorted(categories[category]):
                    cmd_info = commands[cmd_name]
                    print_output(f"  {cmd_name:15s} - {cmd_info['description']}")
            
            print_output("\n" + "=" * 50, "info")
            print_output("提示: 输入 'help [命令名]' 查看特定命令的详细信息。", "warning")
            print_output("例如: help dir, help calc", "warning")
        
        print_prompt()
    
    def execute_command(cmd_input):
        cmd_input = cmd_input.strip()
        if not cmd_input:
            print_prompt()
            return
        
        if cmd_input not in command_history:
            command_history.append(cmd_input)
        history_index = len(command_history)
        
        parts = cmd_input.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if cmd == "help":
            show_help(args[0] if args else None)
        elif cmd == "cls" or cmd == "clear":
            terminal_text.delete(1.0, tk.END)
            print_prompt()
        elif cmd == "exit":
            close_window(window_frame)
        elif cmd == "exit-system" or cmd == "shutdown":
            print_output("正在退出系统...", "warning")
            print_output("保存系统状态...", "info")
            print_output("关闭所有应用程序...", "info")
            print_output("系统已退出", "success")
            root.after(1000, lambda: root.destroy())
            return
        elif cmd == "dir":
            print_output("\n 驱动器 C 中的卷是 Windows", "info")
            print_output(" 卷的序列号是 1234-5678", "info")
            print_output("\n C:\\Users\\guest 的目录", "info")
            print_output("\n2024/01/15  10:30    <DIR>          Documents", "success")
            print_output("2024/01/15  10:30    <DIR>          Downloads", "success")
            print_output("2024/01/15  10:30    <DIR>          Desktop", "success")
            print_output("2024/01/15  10:30    <DIR>          Pictures", "success")
            print_output("2024/01/15  10:30               1,024 readme.txt", "success")
            print_output("2024/01/15  10:30               5,120 notes.doc", "success")
            print_output("               2 个文件      6,144 字节", "info")
            print_output("               4 个目录  可用字节数...", "info")
            print_prompt()
        elif cmd == "cd":
            if not args:
                print_output("C:\\Users\\guest", "info")
            elif args[0] == "..":
                print_output("C:\\Users", "info")
            else:
                print_output(f"C:\\Users\\guest\\{args[0]}", "info")
            print_prompt()
        elif cmd == "echo":
            print_output("\n" + " ".join(args))
            print_prompt()
        elif cmd == "date":
            print_output(f"\n当前日期: {t.strftime('%Y-%m-%d %A')}", "success")
            print_prompt()
        elif cmd == "time":
            print_output(f"\n当前时间: {t.strftime('%H:%M:%S')}", "success")
            print_prompt()
        elif cmd == "whoami":
            print_output(f"\nguest", "success")
            print_prompt()
        elif cmd == "hostname":
            print_output(f"\nLopingsOS-PC", "success")
            print_prompt()
        elif cmd == "ver":
            print_output(f"\nLopingsOS [版本 1.0.0]", "success")
            print_prompt()
        elif cmd == "calc":
            if args:
                try:
                    expression = " ".join(args)
                    result = eval(expression)
                    print_output(f"\n{expression} = {result}", "success")
                except:
                    print_output(f"\n错误: 无效的表达式", "error")
            else:
                print_output("\n用法: calc [表达式]", "warning")
            print_prompt()
        elif cmd == "notepad":
            create_notepad_window()
            print_output("\n正在打开记事本...", "info")
            print_prompt()
        elif cmd == "calcapp":
            create_calculator_window()
            print_output("\n正在打开计算器...", "info")
            print_prompt()
        elif cmd == "browser":
            create_browser_window()
            print_output("\n正在打开浏览器...", "info")
            print_prompt()
        elif cmd == "explorer":
            create_file_explorer_window()
            print_output("\n正在打开文件资源管理器...", "info")
            print_prompt()
        elif cmd == "settings":
            create_settings_window()
            print_output("\n正在打开设置...", "info")
            print_prompt()
        elif cmd == "taskmgr":
            create_task_manager_window()
            print_output("\n正在打开任务管理器...", "info")
            print_prompt()
        elif cmd == "download":
            create_download_window()
            print_output("\n正在打开下载管理器...", "info")
            print_prompt()
        elif cmd == "sysinfo":
            print_output("\n系统信息:", "info")
            print_output(f"  操作系统: LopingsOS 1.0.0", "success")
            print_output(f"  Shell: LopingsOS PowerShell", "success")
            print_output(f"  用户: guest", "success")
            print_output(f"  Python: {s.version.split()[0]}", "success")
            print_output(f"  计算机: LopingsOS-PC", "success")
            print_prompt()
        elif cmd == "env":
            if not args:
                print_output("\n环境变量:", "info")
                print_output(f"  USERNAME=guest", "success")
                print_output(f"  USERPROFILE=C:\\Users\\guest", "success")
                print_output(f"  OS=LopingsOS", "success")
                print_output(f"  VERSION=1.0.0", "success")
            elif len(args) == 1:
                print_output(f"\n{args[0]}=guest", "success")
            else:
                print_output(f"\n已设置环境变量: {args[0]}={args[1]}", "success")
            print_prompt()
        elif cmd == "history":
            print_output("\n命令历史:", "info")
            for i, cmd in enumerate(command_history, 1):
                print_output(f"  {i:3d}  {cmd}", "success")
            print_prompt()
        elif cmd == "ipconfig":
            print_output("\nWindows IP 配置", "info")
            print_output("\n以太网适配器 本地连接:", "success")
            print_output("   连接特定的 DNS 后缀 . . . . . . : ", "info")
            print_output("   IPv4 地址 . . . . . . . . . . . : 192.168.1.100", "success")
            print_output("   子网掩码  . . . . . . . . . . . : 255.255.255.0", "info")
            print_output("   默认网关. . . . . . . . . . . : 192.168.1.1", "info")
            print_prompt()
        elif cmd == "ping":
            if args:
                target = args[0]
                print_output(f"\n正在 Ping {target} [32 字节的数据]:", "info")
                for i in range(4):
                    print_output(f"  来自 {target} 的回复: 字节=32 时间={i*10+5}ms TTL=64", "success")
                    t.sleep(0.5)
                print_output(f"\n  {target} 的 Ping 统计信息:", "info")
                print_output("    数据包: 已发送 = 4，已接收 = 4，丢失 = 0 (0% 丢失)", "success")
                print_output("往返行程的估计时间(以毫秒为单位):", "info")
                print_output("    最短 = 5ms，最长 = 35ms，平均 = 20ms", "success")
            else:
                print_output("\n用法: ping [地址]", "warning")
            print_prompt()
        else:
            print_output(f"\n'{cmd}' 不是内部或外部命令，也不是可运行的程序", "error")
            print_output("输入 'help' 查看可用命令。", "warning")
            print_prompt()
    
    def on_key_press(event):
        if event.keysym == "Return":
            current_line = terminal_text.get("end-2l linestart", "end-1c")
            if current_line.startswith("PS C:\\Users\\guest> "):
                command = current_line[19:]
                execute_command(command)
        elif event.keysym == "Up":
            if command_history and history_index > 0:
                history_index -= 1
                terminal_text.delete("end-2l linestart", "end-1c")
                terminal_text.insert("end-1c", command_history[history_index])
                terminal_text.see(tk.END)
        elif event.keysym == "Down":
            if command_history and history_index < len(command_history) - 1:
                history_index += 1
                terminal_text.delete("end-2l linestart", "end-1c")
                terminal_text.insert("end-1c", command_history[history_index])
                terminal_text.see(tk.END)
        elif event.keysym == "Tab":
            current_line = terminal_text.get("end-2l linestart", "end-1c")
            if current_line.startswith("PS C:\\Users\\guest> "):
                partial = current_line[19:].lower()
                matches = [cmd for cmd in commands.keys() if cmd.startswith(partial)]
                if matches:
                    terminal_text.delete("end-2l linestart", "end-1c")
                    terminal_text.insert("end-1c", matches[0])
                    terminal_text.see(tk.END)
            return "break"
    
    terminal_text.bind("<Key>", on_key_press)
    terminal_text.focus_set()
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_settings_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=150, y=50, width=500, height=400)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 150, "y": 50, "width": 500, "height": 400}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="设置", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = create_windows_button(title_bar, text="×", bg="#000080", fg="white", 
                                    command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = create_windows_button(title_bar, text="□", bg="#000080", fg="white",
                                        command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = create_windows_button(title_bar, text="−", bg="#000080", fg="white",
                                        command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="#f0f0f0")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    notebook = ttk.Notebook(content)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    system_tab = tk.Frame(notebook, bg="white")
    notebook.add(system_tab, text="系统")
    
    tk.Label(system_tab, text="系统信息", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
    
    info_frame = tk.Frame(system_tab, bg="white")
    info_frame.pack(pady=10, padx=20)
    
    tk.Label(info_frame, text=f"操作系统: LopingsOS {o.environ.get('-v', '1.0.0')}", bg="white").pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Shell: {o.environ.get('-shell', 'LopingsOS')}", bg="white").pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"用户: {o.environ.get('users', 'guest')}", bg="white").pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Python版本: {s.version.split()[0]}", bg="white").pack(anchor="w", pady=2)
    if TORCH_AVAILABLE:
        tk.Label(info_frame, text=f"Torch版本: {torch.__version__}", bg="white", fg="green").pack(anchor="w", pady=2)
        tk.Label(info_frame, text=f"CUDA可用: {torch.cuda.is_available()}", bg="white").pack(anchor="w", pady=2)
    else:
        tk.Label(info_frame, text="Torch版本: 未安装", bg="white", fg="red").pack(anchor="w", pady=2)
    
    appearance_tab = tk.Frame(notebook, bg="white")
    notebook.add(appearance_tab, text="外观")
    
    tk.Label(appearance_tab, text="主题设置", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
    
    theme_frame = tk.Frame(appearance_tab, bg="white")
    theme_frame.pack(pady=10)
    
    def change_theme(color):
        desktop.config(bg=color)
        for widget in desktop.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=color, fg="white")
    
    create_windows_button(theme_frame, text="经典绿色", bg="#008080", fg="white",
                         command=lambda: change_theme("#008080")).pack(pady=5, padx=10)
    create_windows_button(theme_frame, text="深蓝色", bg="#000080", fg="white",
                         command=lambda: change_theme("#000080")).pack(pady=5, padx=10)
    create_windows_button(theme_frame, text="深灰色", bg="#404040", fg="white",
                         command=lambda: change_theme("#404040")).pack(pady=5, padx=10)
    
    tk.Label(appearance_tab, text="鼠标图标", font=("Arial", 12, "bold"), bg="white").pack(pady=(20, 10))
    
    cursor_frame = tk.Frame(appearance_tab, bg="white")
    cursor_frame.pack(pady=10)
    
    def change_cursor(cursor_name, display_name):
        root.config(cursor=cursor_name)
        print(f"鼠标图标已更改为: {display_name}")
    
    cursor_options = [
        ("arrow", "默认箭头"),
        ("hand2", "手形指针"),
        ("watch", "等待图标"),
        ("crosshair", "十字光标"),
        ("question_arrow", "问号箭头"),
        ("fleur", "移动图标"),
        ("sb_v_double_arrow", "垂直调整"),
        ("sb_h_double_arrow", "水平调整"),
        ("circle", "圆形光标"),
        ("dotbox", "点框光标")
    ]
    
    for cursor_name, display_name in cursor_options:
        create_windows_button(cursor_frame, text=display_name, bg="#4CAF50", fg="white",
                             command=lambda c=cursor_name, d=display_name: change_cursor(c, d)).pack(pady=3, padx=10)
    
    users_tab = tk.Frame(notebook, bg="white")
    notebook.add(users_tab, text="用户")
    
    tk.Label(users_tab, text="用户管理", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
    
    users_frame = tk.Frame(users_tab, bg="white")
    users_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    users_list = ttk.Treeview(users_frame, columns=("username", "fullname", "email", "role"), show="headings", selectmode="browse")
    users_list.heading("username", text="用户名")
    users_list.heading("fullname", text="全名")
    users_list.heading("email", text="邮箱")
    users_list.heading("role", text="角色")
    
    users_list.column("username", width=100)
    users_list.column("fullname", width=150)
    users_list.column("email", width=200)
    users_list.column("role", width=80)
    
    users_scrollbar = ttk.Scrollbar(users_frame, orient=tk.VERTICAL, command=users_list.yview)
    users_list.configure(yscrollcommand=users_scrollbar.set)
    
    users_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    users_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh_users_list():
        for item in users_list.get_children():
            users_list.delete(item)
        
        if get_db:
            db = get_db()
            users = db.get_all_users()
            for user in users:
                users_list.insert("", "end", values=(user["username"], user["fullname"], user["email"], user["role"]))
        else:
            for username, user_data in users_data.items():
                users_list.insert("", "end", values=(username, user_data["fullname"], user_data["email"], user_data["role"]))
    
    refresh_users_list()
    
    def on_refresh():
        refresh_users_list()
        messagebox.showinfo("刷新成功", "用户列表已更新")
    
    refresh_btn = create_windows_button(users_tab, text="刷新用户列表", bg="#2196F3", fg="white",
                                      command=on_refresh)
    refresh_btn.pack(pady=10, padx=20, anchor=tk.W)
    
    about_tab = tk.Frame(notebook, bg="white")
    notebook.add(about_tab, text="关于")
    
    tk.Label(about_tab, text="关于 LopingsOS", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
    tk.Label(about_tab, text="LopingsOS 是一个模拟Windows操作系统的", bg="white").pack()
    tk.Label(about_tab, text="轻量级桌面环境，基于Python Tkinter开发。", bg="white").pack()
    tk.Label(about_tab, text="", bg="white").pack()
    tk.Label(about_tab, text="版本: 1.0.0", bg="white").pack()
    tk.Label(about_tab, text="开发者: Loping", bg="white").pack()
    
    apps_tab = tk.Frame(notebook, bg="white")
    notebook.add(apps_tab, text="应用")
    
    tk.Label(apps_tab, text="已安装应用", font=("Arial", 12, "bold"), bg="white").pack(pady=10)
    
    apps_frame = tk.Frame(apps_tab, bg="white")
    apps_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    apps_list = ttk.Treeview(apps_frame, columns=("name", "icon", "type"), show="headings", selectmode="browse")
    apps_list.heading("name", text="名称")
    apps_list.heading("icon", text="图标")
    apps_list.heading("type", text="类型")
    
    apps_list.column("name", width=180)
    apps_list.column("icon", width=50)
    apps_list.column("type", width=80)
    
    apps_scrollbar = ttk.Scrollbar(apps_frame, orient=tk.VERTICAL, command=apps_list.yview)
    apps_list.configure(yscrollcommand=apps_scrollbar.set)
    
    apps_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    apps_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def refresh_apps_list():
        for item in apps_list.get_children():
            apps_list.delete(item)
        
        for name, icon in desktop_icons:
            apps_list.insert("", "end", values=(name, icon, "应用"))
        
        for file_data in desktop_files:
            apps_list.insert("", "end", values=(file_data["name"], file_data["icon"], file_data["type"]))
    
    refresh_apps_list()
    
    def uninstall_app():
        selection = apps_list.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要卸载的应用或删除的文件")
            return
        
        item = apps_list.item(selection[0])
        values = item["values"]
        name = values[0]
        item_type = values[2]
        
        if item_type == "应用":
            if name in ["我的电脑", "回收站", "文件资源管理器", "下载"]:
                messagebox.showwarning("警告", f"{name} 是系统应用，无法卸载")
                return
            
            confirm = messagebox.askyesno("确认卸载", f"确定要卸载 {name} 吗？")
            if confirm:
                global desktop_icons
                desktop_icons = [icon for icon in desktop_icons if icon[0] != name]
                refresh_apps_list()
                refresh_desktop_icons()
                messagebox.showinfo("卸载成功", f"{name} 已成功卸载")
        else:
            confirm = messagebox.askyesno("确认删除", f"确定要删除文件 {name} 吗？")
            if confirm:
                global desktop_files
                desktop_files = [file for file in desktop_files if file["name"] != name]
                refresh_apps_list()
                refresh_desktop_icons()
                messagebox.showinfo("删除成功", f"{name} 已成功删除")
    
    uninstall_btn = create_windows_button(apps_tab, text="卸载/删除", bg="#f44336", fg="white",
                                         command=uninstall_app)
    uninstall_btn.pack(pady=10)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_file_explorer_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=50, y=30, width=700, height=500)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 50, "y": 30, "width": 700, "height": 500}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="文件资源管理器", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#000080", fg="white",
                            command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="white")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    toolbar = tk.Frame(content, bg="#f0f0f0", height=40)
    toolbar.pack(fill=tk.X, padx=2, pady=2)
    toolbar.pack_propagate(False)
    
    new_folder_btn = create_windows_button(toolbar, text="新建文件夹", bg="#4CAF50", fg="white",
                                          command=lambda: create_new_folder_dialog())
    new_folder_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    back_btn = create_windows_button(toolbar, text="◀", bg="#f0f0f0", fg="#333333",
                                   width=3, command=lambda: navigate_back())
    back_btn.pack(side=tk.LEFT, padx=2, pady=5)
    
    forward_btn = create_windows_button(toolbar, text="▶", bg="#f0f0f0", fg="#333333",
                                      width=3, command=lambda: navigate_forward())
    forward_btn.pack(side=tk.LEFT, padx=2, pady=5)
    
    up_btn = create_windows_button(toolbar, text="▲", bg="#f0f0f0", fg="#333333",
                                 width=3, command=lambda: navigate_up())
    up_btn.pack(side=tk.LEFT, padx=2, pady=5)
    
    address_frame = tk.Frame(toolbar, bg="white")
    address_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
    
    address_label = tk.Label(address_frame, text="地址: ", bg="white")
    address_label.pack(side=tk.LEFT)
    
    address_entry = tk.Entry(address_frame, bg="white")
    address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    address_entry.insert(0, "C:\\")
    
    path_history = ["C:\\"]
    current_index = 0
    folders = ["文档", "图片", "音乐", "视频", "下载", "桌面"]
    
    def update_address():
        address_entry.delete(0, tk.END)
        address_entry.insert(0, path_history[current_index])
    
    def navigate_back():
        nonlocal current_index
        if current_index > 0:
            current_index -= 1
            update_address()
            refresh_file_list()
    
    def navigate_forward():
        nonlocal current_index
        if current_index < len(path_history) - 1:
            current_index += 1
            update_address()
            refresh_file_list()
    
    def navigate_up():
        nonlocal current_index
        current_path = path_history[current_index]
        if current_path != "C:\\":
            parent_path = o.path.dirname(current_path.rstrip("\\"))
            if not parent_path:
                parent_path = "C:\\"
            path_history.append(parent_path)
            current_index = len(path_history) - 1
            update_address()
            refresh_file_list()
    
    def refresh_file_list():
        nonlocal folders
        current_path = path_history[current_index]
        for item in file_list.get_children():
            file_list.delete(item)
        
        for folder in folders:
            file_list.insert("", "end", values=("📁", folder, "文件夹", ""))
        
        files = [
            ("📄", "readme.txt", "文本文档", "1 KB"),
            ("📄", "notes.doc", "Word文档", "5 KB"),
            ("📊", "data.xlsx", "Excel表格", "10 KB"),
            ("🖼️", "photo.jpg", "JPEG图像", "500 KB"),
            ("🎵", "music.mp3", "MP3音频", "3 MB"),
            ("🎬", "video.mp4", "MP4视频", "50 MB")
        ]
        
        for file_info in files:
            file_list.insert("", "end", values=file_info)
    
    def create_new_folder_dialog():
        dialog = tk.Toplevel(root)
        dialog.title("新建文件夹")
        dialog.geometry("400x150")
        dialog.transient(root)
        dialog.grab_set()
        
        dialog_frame = tk.Frame(dialog, bg="white")
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(dialog_frame, text="文件夹名称:", font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=5)
        
        folder_name_entry = tk.Entry(dialog_frame, font=("Arial", 10))
        folder_name_entry.pack(fill=tk.X, pady=5)
        folder_name_entry.insert(0, "新建文件夹")
        folder_name_entry.select_range(0, tk.END)
        folder_name_entry.focus()
        
        def on_create():
            folder_name = folder_name_entry.get().strip()
            if folder_name:
                current_path = path_history[current_index]
                new_folder_path = o.path.join(current_path, folder_name)
                if new_folder_path not in [o.path.join(current_path, folder) for folder in folders]:
                    folders.append(folder_name)
                    refresh_file_list()
                    dialog.destroy()
                else:
                    messagebox.showwarning("警告", "该文件夹已存在！")
            else:
                messagebox.showwarning("警告", "请输入文件夹名称！")
        
        def on_cancel():
            dialog.destroy()
        
        button_frame = tk.Frame(dialog_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="创建", bg="#4CAF50", fg="white", width=10, command=on_create).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", bg="#f0f0f0", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)
        
        folder_name_entry.bind("<Return>", lambda e: on_create())
        folder_name_entry.bind("<Escape>", lambda e: on_cancel())
    
    file_list_frame = tk.Frame(content, bg="white")
    file_list_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    columns = ("icon", "name", "type", "size")
    file_list = ttk.Treeview(file_list_frame, columns=columns, show="headings", selectmode="browse")
    
    file_list.heading("icon", text="")
    file_list.heading("name", text="名称")
    file_list.heading("type", text="类型")
    file_list.heading("size", text="大小")
    
    file_list.column("icon", width=40, anchor="center")
    file_list.column("name", width=200)
    file_list.column("type", width=120)
    file_list.column("size", width=100)
    
    scrollbar = ttk.Scrollbar(file_list_frame, orient=tk.VERTICAL, command=file_list.yview)
    file_list.configure(yscrollcommand=scrollbar.set)
    
    file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    refresh_file_list()
    
    def on_double_click(event):
        selection = file_list.selection()
        if selection:
            item = file_list.item(selection[0])
            values = item["values"]
            if values[2] == "文件夹":
                folder_name = values[1]
                current_path = path_history[current_index]
                new_path = o.path.join(current_path, folder_name)
                path_history.append(new_path)
                current_index = len(path_history) - 1
                update_address()
                refresh_file_list()
    
    file_list.bind("<Double-1>", on_double_click)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_download_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=600, height=450)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 100, "y": 50, "width": 600, "height": 450}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="下载管理器", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#000080", fg="white",
                            command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="#f0f0f0")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    toolbar = tk.Frame(content, bg="#e0e0e0", height=40)
    toolbar.pack(fill=tk.X, padx=2, pady=2)
    toolbar.pack_propagate(False)
    
    new_download_btn = create_windows_button(toolbar, text="新建下载", bg="#4CAF50", fg="white",
                                          command=lambda: add_new_download())
    new_download_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    pause_all_btn = create_windows_button(toolbar, text="全部暂停", bg="#FF9800", fg="white",
                                        command=lambda: pause_all_downloads())
    pause_all_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    clear_completed_btn = create_windows_button(toolbar, text="清除已完成", bg="#2196F3", fg="white",
                                               command=lambda: clear_completed_downloads())
    clear_completed_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    downloads_frame = tk.Frame(content, bg="white")
    downloads_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    columns = ("name", "size", "progress", "speed", "status", "action")
    downloads_list = ttk.Treeview(downloads_frame, columns=columns, show="headings", selectmode="browse")
    
    downloads_list.heading("name", text="文件名")
    downloads_list.heading("size", text="大小")
    downloads_list.heading("progress", text="进度")
    downloads_list.heading("speed", text="速度")
    downloads_list.heading("status", text="状态")
    downloads_list.heading("action", text="操作")
    
    downloads_list.column("name", width=150)
    downloads_list.column("size", width=80)
    downloads_list.column("progress", width=100)
    downloads_list.column("speed", width=80)
    downloads_list.column("status", width=80)
    downloads_list.column("action", width=100)
    
    scrollbar = ttk.Scrollbar(downloads_frame, orient=tk.VERTICAL, command=downloads_list.yview)
    downloads_list.configure(yscrollcommand=scrollbar.set)
    
    downloads_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    downloads_data = []
    
    global desktop_files
    
    def show_custom_download_dialog():
        dialog = tk.Toplevel(root)
        dialog.title("新建下载")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(root)
        dialog.grab_set()
        
        dialog_frame = tk.Frame(dialog, bg="#f0f0f0")
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(dialog_frame, text="文件名:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(dialog_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(dialog_frame, text="文件大小:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        size_entry = tk.Entry(dialog_frame, width=30)
        size_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(dialog_frame, text="单位:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
        unit_var = tk.StringVar(value="MB")
        unit_combo = ttk.Combobox(dialog_frame, textvariable=unit_var, values=["KB", "MB", "GB"], state="readonly", width=27)
        unit_combo.grid(row=2, column=1, pady=5)
        
        tk.Label(dialog_frame, text="文件类型:", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
        type_var = tk.StringVar(value="文档")
        type_combo = ttk.Combobox(dialog_frame, textvariable=type_var, values=["文档", "图片", "音乐", "视频", "程序", "压缩包"], state="readonly", width=27)
        type_combo.grid(row=3, column=1, pady=5)
        
        result = {"confirmed": False, "data": None}
        
        def on_ok():
            name = name_entry.get().strip()
            size = size_entry.get().strip()
            unit = unit_var.get()
            file_type = type_var.get()
            
            if not name or not size:
                messagebox.showwarning("警告", "请填写完整的文件信息")
                return
            
            try:
                float(size)
            except ValueError:
                messagebox.showwarning("警告", "文件大小必须是数字")
                return
            
            result["confirmed"] = True
            result["data"] = (name, size, unit, file_type)
            dialog.destroy()
        
        def on_cancel():
            dialog.destroy()
        
        button_frame = tk.Frame(dialog_frame, bg="#f0f0f0")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="确定", width=10, command=on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)
        
        dialog.wait_window()
        return result
    
    def get_file_icon(file_type):
        icons = {
            "文档": "📄",
            "图片": "🖼️",
            "音乐": "🎵",
            "视频": "🎬",
            "程序": "⚙️",
            "压缩包": "📦"
        }
        return icons.get(file_type, "📄")
    
    def add_new_download():
        dialog_result = show_custom_download_dialog()
        
        if not dialog_result["confirmed"]:
            return
        
        name, size, unit, file_type = dialog_result["data"]
        file_size = f"{size} {unit}"
        download_id = len(downloads_data)
        
        download_item = {
            "id": download_id,
            "name": name,
            "size": file_size,
            "progress": 0,
            "speed": "0 KB/s",
            "status": "等待中",
            "paused": False,
            "file_type": file_type,
            "icon": get_file_icon(file_type)
        }
        
        downloads_data.append(download_item)
        update_download_list(download_item)
        start_download(download_item)
    
    def update_download_list(download_item):
        progress_text = f"{download_item['progress']}%"
        downloads_list.insert("", "end", iid=download_item["id"], 
                             values=(download_item["name"], download_item["size"], 
                                   progress_text, download_item["speed"], 
                                   download_item["status"], "暂停/继续"))
    
    def start_download(download_item):
        download_item["status"] = "下载中"
        download_item["paused"] = False
        update_download_item(download_item)
        simulate_download(download_item)
    
    def simulate_download(download_item):
        def update():
            if download_item["paused"]:
                root.after(500, update)
                return
            
            if download_item["progress"] >= 100:
                download_item["status"] = "已完成"
                download_item["speed"] = "0 KB/s"
                update_download_item(download_item)
                add_file_to_desktop(download_item)
                return
            
            import random
            increment = random.randint(1, 5)
            download_item["progress"] = min(100, download_item["progress"] + increment)
            download_item["speed"] = f"{random.randint(100, 500)} KB/s"
            update_download_item(download_item)
            root.after(200, update)
        
        update()
    
    def update_download_item(download_item):
        if downloads_list.exists(download_item["id"]):
            progress_text = f"{download_item['progress']}%"
            downloads_list.item(download_item["id"], 
                               values=(download_item["name"], download_item["size"], 
                                       progress_text, download_item["speed"], 
                                       download_item["status"], "暂停/继续"))
    
    def pause_all_downloads():
        for download in downloads_data:
            if download["status"] == "下载中":
                download["paused"] = True
                download["status"] = "已暂停"
                update_download_item(download)
    
    def clear_completed_downloads():
        to_remove = []
        for download in downloads_data:
            if download["status"] == "已完成":
                to_remove.append(download["id"])
                downloads_list.delete(download["id"])
        
        for download_id in to_remove:
            downloads_data[:] = [d for d in downloads_data if d["id"] != download_id]
    
    def add_file_to_desktop(download_item):
        file_name = download_item["name"]
        file_icon = download_item["icon"]
        file_type = download_item["file_type"]
        
        file_data = {
            "name": file_name,
            "icon": file_icon,
            "type": file_type,
            "size": download_item["size"]
        }
        
        desktop_files.append(file_data)
        create_desktop_file_icon(file_data)
    
    def create_desktop_file_icon(file_data):
        icon_frame = tk.Frame(desktop, bg="#0078D7")
        
        total_icons = len(desktop_icons) + len(desktop_files) - 1
        row = total_icons // 5
        col = total_icons % 5
        x = 20 + col * 100
        y = 20 + row * 100
        icon_frame.place(x=x, y=y)
        
        desktop_file_frames[file_data["name"]] = icon_frame
        
        icon_label = tk.Label(icon_frame, text=file_data["icon"], font=("Arial", 32), bg="#0078D7")
        icon_label.pack()
        name_label = tk.Label(icon_frame, text=file_data["name"], bg="#0078D7", fg="white", font=("Arial", 9))
        name_label.pack()
        
        def on_enter(event, frame=icon_frame, il=icon_label, nl=name_label):
            il.config(bg="#005a9e")
            nl.config(bg="#005a9e")
        
        def on_leave(event, frame=icon_frame, il=icon_label, nl=name_label):
            il.config(bg="#0078D7")
            nl.config(bg="#0078D7")
        
        icon_frame.bind("<Enter>", on_enter)
        icon_frame.bind("<Leave>", on_leave)
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
        name_label.bind("<Enter>", on_enter)
        name_label.bind("<Leave>", on_leave)
        
        drag_data = {"x": 0, "y": 0, "dragging": False}
        
        def on_drag_start(event, frame=icon_frame, data=drag_data):
            data["x"] = event.x
            data["y"] = event.y
            data["dragging"] = False
            frame.config(relief=tk.RIDGE, bd=3)
        
        def on_drag_motion(event, frame=icon_frame, data=drag_data):
            data["dragging"] = True
            x = event.x_root - data["x"] - frame.winfo_rootx() + frame.winfo_x()
            y = event.y_root - data["y"] - frame.winfo_rooty() + frame.winfo_y()
            frame.place(x=x, y=y)
        
        def on_drag_end(event, frame=icon_frame, data=drag_data):
            frame.config(relief=tk.FLAT, bd=0)
            if not data["dragging"]:
                open_file(file_data)
        
        icon_frame.bind("<Button-1>", on_drag_start)
        icon_frame.bind("<B1-Motion>", on_drag_motion)
        icon_frame.bind("<ButtonRelease-1>", on_drag_end)
        
        icon_label.bind("<Button-1>", on_drag_start)
        icon_label.bind("<B1-Motion>", on_drag_motion)
        icon_label.bind("<ButtonRelease-1>", on_drag_end)
        
        name_label.bind("<Button-1>", on_drag_start)
        name_label.bind("<B1-Motion>", on_drag_motion)
        name_label.bind("<ButtonRelease-1>", on_drag_end)
    
    def open_file(file_data):
        file_type = file_data["type"]
        file_name = file_data["name"]
        
        if file_type == "文档":
            create_notepad_window()
        elif file_type == "图片":
            create_image_viewer_window(file_name)
        elif file_type == "音乐":
            create_music_player_window(file_name)
        elif file_type == "视频":
            create_video_player_window(file_name)
        elif file_type == "程序":
            messagebox.showinfo("程序", f"正在运行程序: {file_name}")
        elif file_type == "压缩包":
            messagebox.showinfo("压缩包", f"已解压: {file_name}")
    
    def create_image_viewer_window(file_name):
        window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
        window_frame.place(x=150, y=50, width=500, height=400)
        
        title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
        title_bar.pack(fill=tk.X)
        
        title_label = tk.Label(title_bar, text=f"图片查看器 - {file_name}", bg="#000080", fg="white")
        title_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                             command=lambda: close_window(window_frame))
        close_btn.pack(side=tk.RIGHT, padx=2)
        
        minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                                command=lambda: minimize_window(window_frame))
        minimize_btn.pack(side=tk.RIGHT, padx=2)
        
        content = tk.Frame(window_frame, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        tk.Label(content, text="🖼️", font=("Arial", 100), bg="white").pack(expand=True)
        
        window_frame.drag_data = {"x": 0, "y": 0}
        
        def start_drag(event):
            window_frame.drag_data["x"] = event.x
            window_frame.drag_data["y"] = event.y
        
        def do_drag(event):
            x = event.x_root - window_frame.drag_data["x"]
            y = event.y_root - window_frame.drag_data["y"]
            window_frame.place(x=x, y=y)
        
        title_bar.bind("<Button-1>", start_drag)
        title_bar.bind("<B1-Motion>", do_drag)
        
        windows.append(window_frame)
        return window_frame
    
    def create_music_player_window(file_name):
        window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
        window_frame.place(x=150, y=50, width=400, height=200)
        
        title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
        title_bar.pack(fill=tk.X)
        
        title_label = tk.Label(title_bar, text=f"音乐播放器 - {file_name}", bg="#000080", fg="white")
        title_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                             command=lambda: close_window(window_frame))
        close_btn.pack(side=tk.RIGHT, padx=2)
        
        minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                                command=lambda: minimize_window(window_frame))
        minimize_btn.pack(side=tk.RIGHT, padx=2)
        
        content = tk.Frame(window_frame, bg="white")
        content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        tk.Label(content, text="🎵", font=("Arial", 50), bg="white").pack(pady=10)
        tk.Label(content, text=f"正在播放: {file_name}", bg="white").pack()
        
        control_frame = tk.Frame(content, bg="white")
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="⏮️", width=3).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="▶️", width=3).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="⏭️", width=3).pack(side=tk.LEFT, padx=5)
        
        window_frame.drag_data = {"x": 0, "y": 0}
        
        def start_drag(event):
            window_frame.drag_data["x"] = event.x
            window_frame.drag_data["y"] = event.y
        
        def do_drag(event):
            x = event.x_root - window_frame.drag_data["x"]
            y = event.y_root - window_frame.drag_data["y"]
            window_frame.place(x=x, y=y)
        
        title_bar.bind("<Button-1>", start_drag)
        title_bar.bind("<B1-Motion>", do_drag)
        
        windows.append(window_frame)
        return window_frame
    
    def create_video_player_window(file_name):
        window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
        window_frame.place(x=100, y=50, width=600, height=450)
        
        title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
        title_bar.pack(fill=tk.X)
        
        title_label = tk.Label(title_bar, text=f"视频播放器 - {file_name}", bg="#000080", fg="white")
        title_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                             command=lambda: close_window(window_frame))
        close_btn.pack(side=tk.RIGHT, padx=2)
        
        minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                                command=lambda: minimize_window(window_frame))
        minimize_btn.pack(side=tk.RIGHT, padx=2)
        
        content = tk.Frame(window_frame, bg="black")
        content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        tk.Label(content, text="🎬", font=("Arial", 80), fg="white", bg="black").pack(expand=True)
        
        control_frame = tk.Frame(content, bg="black")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Button(control_frame, text="⏮️", bg="gray", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="▶️", bg="gray", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="⏭️", bg="gray", fg="white").pack(side=tk.LEFT, padx=5)
        
        window_frame.drag_data = {"x": 0, "y": 0}
        
        def start_drag(event):
            window_frame.drag_data["x"] = event.x
            window_frame.drag_data["y"] = event.y
        
        def do_drag(event):
            x = event.x_root - window_frame.drag_data["x"]
            y = event.y_root - window_frame.drag_data["y"]
            window_frame.place(x=x, y=y)
        
        title_bar.bind("<Button-1>", start_drag)
        title_bar.bind("<B1-Motion>", do_drag)
        
        windows.append(window_frame)
        return window_frame
    
    def on_double_click(event):
        selection = downloads_list.selection()
        if selection:
            download_id = int(selection[0])
            download_item = next((d for d in downloads_data if d["id"] == download_id), None)
            if download_item:
                if download_item["status"] == "下载中":
                    download_item["paused"] = True
                    download_item["status"] = "已暂停"
                    download_item["speed"] = "0 KB/s"
                elif download_item["status"] == "已暂停":
                    download_item["paused"] = False
                    download_item["status"] = "下载中"
                    simulate_download(download_item)
                update_download_item(download_item)
    
    downloads_list.bind("<Double-1>", on_double_click)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_notepad_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=500, height=400)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 100, "y": 50, "width": 500, "height": 400}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="记事本 - 无标题", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#000080", fg="white",
                            command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="white")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    text_area = tk.Text(content, wrap=tk.WORD, font=("Arial", 10))
    text_area.pack(fill=tk.BOTH, expand=True)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_calculator_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=200, y=100, width=300, height=400)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 200, "y": 100, "width": 300, "height": 400}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="计算器", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#000080", fg="white",
                            command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="#f0f0f0")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    display = tk.Entry(content, font=("Arial", 14), justify="right")
    display.pack(fill=tk.X, padx=5, pady=5)
    
    buttons_frame = tk.Frame(content, bg="#f0f0f0")
    buttons_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    buttons = [
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        'C', '0', '=', '+'
    ]
    
    def on_button_click(value):
        current = display.get()
        if value == 'C':
            display.delete(0, tk.END)
        elif value == '=':
            try:
                result = eval(current)
                display.delete(0, tk.END)
                display.insert(0, str(result))
            except:
                display.delete(0, tk.END)
                display.insert(0, "错误")
        else:
            display.insert(tk.END, value)
    
    for i, btn_text in enumerate(buttons):
        btn = tk.Button(buttons_frame, text=btn_text, font=("Arial", 12),
                       command=lambda t=btn_text: on_button_click(t))
        btn.grid(row=i//4, column=i%4, padx=2, pady=2, sticky="nsew")
    
    for i in range(4):
        buttons_frame.grid_columnconfigure(i, weight=1)
    for i in range(4):
        buttons_frame.grid_rowconfigure(i, weight=1)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_mycomputer_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=500, height=350)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 100, "y": 50, "width": 500, "height": 350}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="我的电脑", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#000080", fg="white",
                            command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="white")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    drives_frame = tk.Frame(content, bg="white")
    drives_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(drives_frame, text="本地磁盘 (C:)", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=5)
    tk.Label(drives_frame, text="  容量: 100 GB", bg="white").pack(anchor="w", pady=2)
    tk.Label(drives_frame, text="  可用空间: 50 GB", bg="white").pack(anchor="w", pady=2)
    
    tk.Frame(drives_frame, height=2, bg="gray").pack(fill=tk.X, pady=10)
    
    tk.Label(drives_frame, text="本地磁盘 (D:)", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=5)
    tk.Label(drives_frame, text="  容量: 200 GB", bg="white").pack(anchor="w", pady=2)
    tk.Label(drives_frame, text="  可用空间: 150 GB", bg="white").pack(anchor="w", pady=2)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_recyclebin_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=150, y=80, width=400, height=300)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 150, "y": 80, "width": 400, "height": 300}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="回收站", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#000080", fg="white",
                            command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="white")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    tk.Label(content, text="回收站为空", font=("Arial", 12), bg="white", fg="gray").pack(pady=50)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

windows = []

def create_register_window():
    """创建用户注册窗口"""
    dialog = tk.Toplevel(root)
    dialog.title("用户注册")
    dialog.geometry("500x400")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    dialog_frame = tk.Frame(dialog, bg="#f0f0f0")
    dialog_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    tk.Label(dialog_frame, text="用户注册", font=("Segoe UI", 16, "bold"), bg="#f0f0f0").pack(pady=10)
    
    form_frame = tk.Frame(dialog_frame, bg="white", relief=tk.RAISED, bd=1)
    form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # 用户名
    username_frame = tk.Frame(form_frame, bg="white")
    username_frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(username_frame, text="用户名:", font=("Segoe UI", 10), bg="white", width=10).pack(side=tk.LEFT)
    username_entry = tk.Entry(username_frame, font=("Segoe UI", 10), width=30)
    username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # 密码
    password_frame = tk.Frame(form_frame, bg="white")
    password_frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(password_frame, text="密码:", font=("Segoe UI", 10), bg="white", width=10).pack(side=tk.LEFT)
    password_entry = tk.Entry(password_frame, font=("Segoe UI", 10), width=30, show="*")
    password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # 确认密码
    confirm_frame = tk.Frame(form_frame, bg="white")
    confirm_frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(confirm_frame, text="确认密码:", font=("Segoe UI", 10), bg="white", width=10).pack(side=tk.LEFT)
    confirm_entry = tk.Entry(confirm_frame, font=("Segoe UI", 10), width=30, show="*")
    confirm_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # 全名
    fullname_frame = tk.Frame(form_frame, bg="white")
    fullname_frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(fullname_frame, text="全名:", font=("Segoe UI", 10), bg="white", width=10).pack(side=tk.LEFT)
    fullname_entry = tk.Entry(fullname_frame, font=("Segoe UI", 10), width=30)
    fullname_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # 邮箱
    email_frame = tk.Frame(form_frame, bg="white")
    email_frame.pack(fill=tk.X, padx=20, pady=10)
    tk.Label(email_frame, text="邮箱:", font=("Segoe UI", 10), bg="white", width=10).pack(side=tk.LEFT)
    email_entry = tk.Entry(email_frame, font=("Segoe UI", 10), width=30)
    email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # 消息标签
    message_var = tk.StringVar()
    message_label = tk.Label(dialog_frame, textvariable=message_var, font=("Segoe UI", 10), fg="red", bg="#f0f0f0")
    message_label.pack(pady=10)
    
    def on_register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        confirm_password = confirm_entry.get().strip()
        fullname = fullname_entry.get().strip()
        email = email_entry.get().strip()
        
        # 验证输入
        if not all([username, password, confirm_password, fullname, email]):
            message_var.set("请填写所有必填字段")
            return
        
        if password != confirm_password:
            message_var.set("两次输入的密码不一致")
            return
        
        if len(password) < 6:
            message_var.set("密码长度至少为6位")
            return
        
        if "@" not in email:
            message_var.set("请输入有效的邮箱地址")
            return
        
        # 注册用户
        success, message = register_user(username, password, fullname, email)
        if success:
            message_var.set("")
            messagebox.showinfo("注册成功", message)
            dialog.destroy()
        else:
            message_var.set(message)
    
    def on_cancel():
        dialog.destroy()
    
    button_frame = tk.Frame(dialog_frame, bg="#f0f0f0")
    button_frame.pack(fill=tk.X, pady=10)
    
    create_windows_button(button_frame, text="注册", bg="#4CAF50", fg="white",
                         font=("Segoe UI", 10), command=on_register).pack(side=tk.LEFT, padx=5)
    create_windows_button(button_frame, text="取消", bg="#f44336", fg="white",
                         font=("Segoe UI", 10), command=on_cancel).pack(side=tk.LEFT, padx=5)

def create_run_dialog():
    dialog = tk.Toplevel(root)
    dialog.title("运行")
    dialog.geometry("400x150")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    dialog_frame = tk.Frame(dialog, bg="#f0f0f0")
    dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(dialog_frame, text="打开:", bg="#f0f0f0").pack(anchor="w", pady=5)
    
    run_entry = tk.Entry(dialog_frame, width=40)
    run_entry.pack(fill=tk.X, pady=5)
    run_entry.focus()
    
    def on_run():
        command = run_entry.get().strip()
        if command:
            if command.lower() == "notepad":
                create_notepad_window()
            elif command.lower() == "calc":
                create_calculator_window()
            elif command.lower() == "cmd":
                messagebox.showinfo("命令提示符", "命令提示符功能正在开发中")
            elif command.lower() == "explorer":
                create_file_explorer_window()
            elif command.lower() == "settings":
                create_settings_window()
            elif command.lower() == "taskmgr":
                create_task_manager_window()
            else:
                messagebox.showinfo("运行", f"执行命令: {command}")
            dialog.destroy()
    
    def on_browse():
        messagebox.showinfo("浏览", "浏览功能正在开发中")
    
    button_frame = tk.Frame(dialog_frame, bg="#f0f0f0")
    button_frame.pack(fill=tk.X, pady=10)
    
    tk.Button(button_frame, text="确定", width=10, command=on_run).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="取消", width=10, command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="浏览", width=10, command=on_browse).pack(side=tk.RIGHT, padx=5)
    
    run_entry.bind("<Return>", lambda e: on_run())

def create_task_manager_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=600, height=450)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 100, "y": 50, "width": 600, "height": 450}
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="任务管理器", bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#000080", fg="white",
                            command=lambda: toggle_maximize(window_frame))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="#f0f0f0")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    toolbar = tk.Frame(content, bg="#e0e0e0", height=40)
    toolbar.pack(fill=tk.X, padx=2, pady=2)
    toolbar.pack_propagate(False)
    
    tk.Button(toolbar, text="结束任务", bg="#f44336", fg="white", 
             command=lambda: end_task()).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(toolbar, text="刷新", bg="#2196F3", fg="white",
             command=lambda: refresh_tasks()).pack(side=tk.LEFT, padx=5, pady=5)
    
    tasks_frame = tk.Frame(content, bg="white")
    tasks_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    columns = ("name", "pid", "cpu", "memory", "status")
    tasks_list = ttk.Treeview(tasks_frame, columns=columns, show="headings", selectmode="browse")
    
    tasks_list.heading("name", text="进程名称")
    tasks_list.heading("pid", text="PID")
    tasks_list.heading("cpu", text="CPU")
    tasks_list.heading("memory", text="内存")
    tasks_list.heading("status", text="状态")
    
    tasks_list.column("name", width=200)
    tasks_list.column("pid", width=80)
    tasks_list.column("cpu", width=80)
    tasks_list.column("memory", width=100)
    tasks_list.column("status", width=80)
    
    scrollbar = ttk.Scrollbar(tasks_frame, orient=tk.VERTICAL, command=tasks_list.yview)
    tasks_list.configure(yscrollcommand=scrollbar.set)
    
    tasks_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    import random
    system_processes = [
        ("System", 4, 0, 100, "运行中"),
        ("System Idle Process", 0, 98, 0, "运行中"),
        ("svchost.exe", 1234, 1, 50, "运行中"),
        ("explorer.exe", 5678, 2, 120, "运行中"),
        ("python.exe", 9012, 5, 200, "运行中"),
        ("chrome.exe", 3456, 8, 300, "运行中"),
        ("notepad.exe", 7890, 0, 20, "运行中"),
        ("calc.exe", 2345, 0, 15, "运行中"),
        ("cmd.exe", 6789, 1, 10, "运行中"),
        ("winlogon.exe", 4567, 0, 30, "运行中")
    ]
    
    def refresh_tasks():
        for item in tasks_list.get_children():
            tasks_list.delete(item)
        
        for process in system_processes:
            name, pid, cpu, memory, status = process
            cpu_usage = cpu + random.randint(-1, 1)
            if cpu_usage < 0:
                cpu_usage = 0
            tasks_list.insert("", "end", values=(name, pid, f"{cpu_usage}%", f"{memory} MB", status))
    
    def end_task():
        selection = tasks_list.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要结束的进程")
            return
        
        item = tasks_list.item(selection[0])
        values = item["values"]
        process_name = values[0]
        
        if process_name in ["System", "System Idle Process", "winlogon.exe"]:
            messagebox.showwarning("警告", f"{process_name} 是系统进程，无法结束")
            return
        
        confirm = messagebox.askyesno("确认结束", f"确定要结束进程 {process_name} 吗？")
        if confirm:
            for i, process in enumerate(system_processes):
                if process[0] == process_name:
                    system_processes.pop(i)
                    break
            refresh_tasks()
            messagebox.showinfo("成功", f"已结束进程: {process_name}")
    
    refresh_tasks()
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def create_window(title):
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=400, height=300)
    
    title_bar = tk.Frame(window_frame, bg="#000080", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text=title, bg="#000080", fg="white")
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#000080", fg="white", 
                         command=lambda: close_window(window_frame))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#000080", fg="white",
                            command=lambda: minimize_window(window_frame))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="white")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def close_window(window_frame):
    window_frame.destroy()
    if window_frame in windows:
        windows.remove(window_frame)

def create_browser_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=50, y=20, width=900, height=600)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 50, "y": 20, "width": 900, "height": 600}
    
    title_bar = tk.Frame(window_frame, bg="#202124", relief=tk.FLAT)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="Chrome 浏览器", bg="#202124", fg="white", font=("Arial", 9))
    title_label.pack(side=tk.LEFT, padx=10, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#202124", fg="white", 
                         command=lambda: close_window(window_frame), relief=tk.FLAT, font=("Arial", 10))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#202124", fg="white",
                            command=lambda: toggle_maximize(window_frame), relief=tk.FLAT, font=("Arial", 10))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#202124", fg="white",
                            command=lambda: minimize_window(window_frame), relief=tk.FLAT, font=("Arial", 10))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="#dee2e6")
    content.pack(fill=tk.BOTH, expand=True)
    
    tabs_frame = tk.Frame(content, bg="#dee2e6", height=40)
    tabs_frame.pack(fill=tk.X, padx=5, pady=5)
    tabs_frame.pack_propagate(False)
    
    browser_tabs = []
    current_tab = 0
    tab_contents = []
    address_entry = None
    star_btn = None
    content_text = None
    back_btn = None
    forward_btn = None
    refresh_btn = None
    home_btn = None
    more_btn = None
    
    def create_tab(title="新标签页"):
        tab = tk.Frame(tabs_frame, bg="#dee2e6", relief=tk.FLAT, bd=1)
        tab.pack(side=tk.LEFT, padx=2)
        
        tab_inner = tk.Frame(tab, bg="#e8eaed", relief=tk.FLAT, bd=1)
        tab_inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        tab_icon = tk.Label(tab_inner, text="🌐", bg="#e8eaed", font=("Arial", 8))
        tab_icon.pack(side=tk.LEFT, padx=2)
        
        tab_label = tk.Label(tab_inner, text=title, bg="#e8eaed", font=("Arial", 9))
        tab_label.pack(side=tk.LEFT, padx=2)
        
        close_tab_btn = tk.Button(tab_inner, text="×", bg="#e8eaed", relief=tk.FLAT, font=("Arial", 8),
                                command=lambda: close_tab(len(browser_tabs)))
        close_tab_btn.pack(side=tk.LEFT, padx=2)
        
        def on_tab_click():
            nonlocal current_tab
            current_tab = browser_tabs.index(tab)
            update_tab_display()
        
        tab.bind("<Button-1>", lambda e: on_tab_click())
        tab_inner.bind("<Button-1>", lambda e: on_tab_click())
        tab_icon.bind("<Button-1>", lambda e: on_tab_click())
        tab_label.bind("<Button-1>", lambda e: on_tab_click())
        
        browser_tabs.append(tab)
        tab_contents.append({"title": title, "url": "", "history": [], "history_index": -1})
        current_tab = len(browser_tabs) - 1
        update_tab_display()
    
    def close_tab(index):
        if len(browser_tabs) <= 1:
            return
        
        browser_tabs[index].destroy()
        browser_tabs.pop(index)
        tab_contents.pop(index)
        
        if current_tab >= len(browser_tabs):
            current_tab = len(browser_tabs) - 1
        
        update_tab_display()
    
    def update_tab_display():
        for i, tab in enumerate(browser_tabs):
            tab_inner = tab.winfo_children()[0]
            if i == current_tab:
                tab_inner.config(bg="white")
                for child in tab_inner.winfo_children():
                    child.config(bg="white")
            else:
                tab_inner.config(bg="#e8eaed")
                for child in tab_inner.winfo_children():
                    child.config(bg="#e8eaed")
        
        if address_entry and tab_contents and current_tab < len(tab_contents):
            current_data = tab_contents[current_tab]
            address_entry.delete(0, tk.END)
            address_entry.insert(0, current_data["url"])
    
    create_tab("新标签页")
    
    new_tab_btn = tk.Button(tabs_frame, text="+", bg="#dee2e6", relief=tk.FLAT, font=("Arial", 12),
                           command=lambda: create_tab("新标签页"))
    new_tab_btn.pack(side=tk.LEFT, padx=2)
    
    toolbar = tk.Frame(content, bg="#dee2e6", height=50)
    toolbar.pack(fill=tk.X, padx=5, pady=2)
    toolbar.pack_propagate(False)
    
    nav_frame = tk.Frame(toolbar, bg="#f1f3f4", relief=tk.FLAT, bd=1)
    nav_frame.pack(side=tk.LEFT, padx=2)
    
    back_btn = tk.Button(nav_frame, text="◀", bg="#f1f3f4", relief=tk.FLAT, font=("Arial", 10),
                         command=lambda: browser_back())
    back_btn.pack(side=tk.LEFT, padx=1)
    
    forward_btn = tk.Button(nav_frame, text="▶", bg="#f1f3f4", relief=tk.FLAT, font=("Arial", 10),
                            command=lambda: browser_forward())
    forward_btn.pack(side=tk.LEFT, padx=1)
    
    refresh_btn = tk.Button(nav_frame, text="↻", bg="#f1f3f4", relief=tk.FLAT, font=("Arial", 10),
                           command=lambda: browser_refresh())
    refresh_btn.pack(side=tk.LEFT, padx=1)
    
    home_btn = tk.Button(nav_frame, text="⌂", bg="#f1f3f4", relief=tk.FLAT, font=("Arial", 10),
                        command=lambda: browser_home())
    home_btn.pack(side=tk.LEFT, padx=1)
    
    address_frame = tk.Frame(toolbar, bg="#f1f3f4", relief=tk.FLAT, bd=1)
    address_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    lock_icon = tk.Label(address_frame, text="🔒", bg="#f1f3f4", font=("Arial", 8))
    lock_icon.pack(side=tk.LEFT, padx=5)
    
    address_entry = tk.Entry(address_frame, bg="#f1f3f4", relief=tk.FLAT, font=("Arial", 10), bd=0)
    address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    address_entry.insert(0, "")
    
    star_btn = tk.Button(address_frame, text="☆", bg="#f1f3f4", relief=tk.FLAT, font=("Arial", 10),
                        command=lambda: add_bookmark())
    star_btn.pack(side=tk.LEFT, padx=5)
    
    more_btn = tk.Button(toolbar, text="⋮", bg="#f1f3f4", relief=tk.FLAT, font=("Arial", 10),
                        command=lambda: show_more_menu())
    more_btn.pack(side=tk.LEFT, padx=2)
    
    browser_content = tk.Frame(content, bg="white")
    browser_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    content_text = tk.Text(browser_content, wrap=tk.WORD, bg="white", font=("Arial", 11))
    content_text.pack(fill=tk.BOTH, expand=True)
    
    bookmarks = []
    bookmark_folders = []
    
    def browser_navigate():
        url = address_entry.get().strip()
        if url:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            
            current_data = tab_contents[current_tab]
            current_data["url"] = url
            current_data["history"].append(url)
            current_data["history_index"] = len(current_data["history"]) - 1
            load_page(url)
    
    def browser_back():
        current_data = tab_contents[current_tab]
        if current_data["history_index"] > 0:
            current_data["history_index"] -= 1
            url = current_data["history"][current_data["history_index"]]
            current_data["url"] = url
            address_entry.delete(0, tk.END)
            address_entry.insert(0, url)
            load_page(url)
    
    def browser_forward():
        current_data = tab_contents[current_tab]
        if current_data["history_index"] < len(current_data["history"]) - 1:
            current_data["history_index"] += 1
            url = current_data["history"][current_data["history_index"]]
            current_data["url"] = url
            address_entry.delete(0, tk.END)
            address_entry.insert(0, url)
            load_page(url)
    
    def browser_refresh():
        url = address_entry.get()
        load_page(url)
    
    def browser_home():
        url = "https://www.google.com"
        current_data = tab_contents[current_tab]
        current_data["url"] = url
        current_data["history"].append(url)
        current_data["history_index"] = len(current_data["history"]) - 1
        address_entry.delete(0, tk.END)
        address_entry.insert(0, url)
        load_page(url)
    
    def add_bookmark():
        url = address_entry.get()
        if url:
            dialog = tk.Toplevel(root)
            dialog.title("添加书签")
            dialog.geometry("400x250")
            dialog.transient(root)
            dialog.grab_set()
            
            dialog_frame = tk.Frame(dialog, bg="white")
            dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            tk.Label(dialog_frame, text="书签名称:", font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)
            
            name_entry = tk.Entry(dialog_frame, font=("Arial", 10))
            name_entry.pack(fill=tk.X, pady=2)
            name_entry.insert(0, url)
            
            tk.Label(dialog_frame, text="文件夹:", font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=2)
            
            folder_frame = tk.Frame(dialog_frame, bg="white")
            folder_frame.pack(fill=tk.X, pady=2)
            
            folder_var = tk.StringVar(value="未分类")
            folder_combo = ttk.Combobox(folder_frame, textvariable=folder_var, values=["未分类"] + bookmark_folders, state="readonly")
            folder_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            
            new_folder_btn = tk.Button(folder_frame, text="+", width=3, command=lambda: create_new_bookmark_folder(folder_combo))
            new_folder_btn.pack(side=tk.LEFT)
            
            def on_add():
                bookmark_name = name_entry.get().strip()
                folder = folder_var.get()
                if bookmark_name:
                    bookmark_data = {
                        "name": bookmark_name,
                        "url": url,
                        "folder": folder
                    }
                    bookmarks.append(bookmark_data)
                    star_btn.config(text="★")
                    dialog.destroy()
                    messagebox.showinfo("书签", f"已添加书签: {bookmark_name}")
                else:
                    messagebox.showwarning("警告", "请输入书签名称！")
            
            def on_cancel():
                dialog.destroy()
            
            button_frame = tk.Frame(dialog_frame, bg="white")
            button_frame.pack(fill=tk.X, pady=10)
            
            tk.Button(button_frame, text="添加", bg="#4CAF50", fg="white", width=10, command=on_add).pack(side=tk.LEFT, padx=5)
            tk.Button(button_frame, text="取消", bg="#f0f0f0", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)
            
            name_entry.bind("<Return>", lambda e: on_add())
            name_entry.bind("<Escape>", lambda e: on_cancel())
        else:
            messagebox.showwarning("警告", "请先访问一个网址！")
    
    def create_new_bookmark_folder(folder_combo):
        dialog = tk.Toplevel(root)
        dialog.title("新建书签文件夹")
        dialog.geometry("300x150")
        dialog.transient(root)
        dialog.grab_set()
        
        dialog_frame = tk.Frame(dialog, bg="white")
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(dialog_frame, text="文件夹名称:", font=("Arial", 10), bg="white").pack(anchor=tk.W, pady=5)
        
        folder_name_entry = tk.Entry(dialog_frame, font=("Arial", 10))
        folder_name_entry.pack(fill=tk.X, pady=5)
        folder_name_entry.insert(0, "新建文件夹")
        folder_name_entry.select_range(0, tk.END)
        folder_name_entry.focus()
        
        def on_create():
            folder_name = folder_name_entry.get().strip()
            if folder_name:
                if folder_name not in bookmark_folders:
                    bookmark_folders.append(folder_name)
                    folder_combo["values"] = ["未分类"] + bookmark_folders
                    folder_combo.set(folder_name)
                    dialog.destroy()
                else:
                    messagebox.showwarning("警告", "该文件夹已存在！")
            else:
                messagebox.showwarning("警告", "请输入文件夹名称！")
        
        def on_cancel():
            dialog.destroy()
        
        button_frame = tk.Frame(dialog_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(button_frame, text="创建", bg="#4CAF50", fg="white", width=10, command=on_create).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", bg="#f0f0f0", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)
        
        folder_name_entry.bind("<Return>", lambda e: on_create())
        folder_name_entry.bind("<Escape>", lambda e: on_cancel())
    
    def show_more_menu():
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="新建标签页", command=lambda: create_tab("新标签页"))
        menu.add_command(label="书签管理器", command=lambda: show_bookmark_manager())
        menu.add_command(label="历史记录", command=lambda: show_history())
        menu.add_command(label="下载内容", command=lambda: create_download_window())
        menu.add_separator()
        menu.add_command(label="打印", command=lambda: messagebox.showinfo("打印", "打印功能开发中"))
        menu.add_command(label="设置", command=lambda: create_settings_window())
        menu.post(root.winfo_pointerx(), root.winfo_pointery())
    
    def show_bookmark_manager():
        dialog = tk.Toplevel(root)
        dialog.title("书签管理器")
        dialog.geometry("500x400")
        dialog.transient(root)
        dialog.grab_set()
        
        dialog_frame = tk.Frame(dialog, bg="white")
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(dialog_frame, text="书签管理器", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
        
        paned_window = tk.PanedWindow(dialog_frame, orient=tk.HORIZONTAL, bg="white")
        paned_window.pack(fill=tk.BOTH, expand=True, pady=5)
        
        folder_frame = tk.Frame(paned_window, bg="white", width=150)
        paned_window.add(folder_frame)
        
        bookmark_frame = tk.Frame(paned_window, bg="white")
        paned_window.add(bookmark_frame)
        
        tk.Label(folder_frame, text="文件夹", font=("Arial", 10, "bold"), bg="white").pack(pady=5)
        
        folder_list = tk.Listbox(folder_frame, bg="white", height=15)
        folder_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        folder_list.insert(tk.END, "全部书签")
        folder_list.insert(tk.END, "未分类")
        for folder in bookmark_folders:
            folder_list.insert(tk.END, folder)
        
        tk.Label(bookmark_frame, text="书签", font=("Arial", 10, "bold"), bg="white").pack(pady=5)
        
        bookmark_list = tk.Listbox(bookmark_frame, bg="white", height=15)
        bookmark_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        def update_bookmark_list():
            bookmark_list.delete(0, tk.END)
            selection = folder_list.curselection()
            if selection:
                selected_folder = folder_list.get(selection[0])
                if selected_folder == "全部书签":
                    for bookmark in bookmarks:
                        bookmark_list.insert(tk.END, f"{bookmark['name']}")
                else:
                    for bookmark in bookmarks:
                        if bookmark["folder"] == selected_folder:
                            bookmark_list.insert(tk.END, f"{bookmark['name']}")
        
        def on_folder_select(event):
            update_bookmark_list()
        
        folder_list.bind("<<ListboxSelect>>", on_folder_select)
        
        def on_bookmark_double_click(event):
            selection = bookmark_list.curselection()
            if selection:
                index = selection[0]
                folder_selection = folder_list.curselection()
                if folder_selection:
                    selected_folder = folder_list.get(folder_selection[0])
                    if selected_folder == "全部书签":
                        bookmark = bookmarks[index]
                    else:
                        filtered_bookmarks = [b for b in bookmarks if b["folder"] == selected_folder]
                        bookmark = filtered_bookmarks[index]
                    dialog.destroy()
                    address_entry.delete(0, tk.END)
                    address_entry.insert(0, bookmark["url"])
                    browser_navigate()
        
        bookmark_list.bind("<Double-Button-1>", on_bookmark_double_click)
        
        update_bookmark_list()
        
        button_frame = tk.Frame(dialog_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="打开", command=lambda: on_bookmark_double_click(None)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="关闭", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_history():
        dialog = tk.Toplevel(root)
        dialog.title("历史记录")
        dialog.geometry("400x300")
        dialog.transient(root)
        dialog.grab_set()
        
        dialog_frame = tk.Frame(dialog, bg="white")
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(dialog_frame, text="浏览历史", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
        
        history_list = tk.Listbox(dialog_frame, bg="white", height=15)
        history_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        for data in tab_contents:
            for url in data["history"]:
                history_list.insert(tk.END, url)
        
        def on_select():
            selection = history_list.curselection()
            if selection:
                url = history_list.get(selection[0])
                dialog.destroy()
                address_entry.delete(0, tk.END)
                address_entry.insert(0, url)
                browser_navigate()
        
        history_list.bind("<Double-Button-1>", lambda e: on_select())
        
        tk.Button(dialog_frame, text="打开", command=on_select).pack(pady=5)
    
    def load_page(url):
        nonlocal content_text
        content_text.config(state=tk.NORMAL)
        content_text.delete(1.0, tk.END)
        
        if "google.com" in url:
            page_content = f"""
            <html>
            <head><title>Google</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 100px;">
            <div style="font-size: 80px; color: #4285f4;">G</div>
            <div style="font-size: 80px; color: #ea4335;">o</div>
            <div style="font-size: 80px; color: #fbbc05;">o</div>
            <div style="font-size: 80px; color: #4285f4;">g</div>
            <div style="font-size: 80px; color: #34a853;">l</div>
            <div style="font-size: 80px; color: #ea4335;">e</div>
            <br><br>
            <input type="text" style="width: 500px; padding: 15px; border: 1px solid #dfe1e5; border-radius: 24px; font-size: 16px;" placeholder="在 Google 上搜索">
            <br><br>
            <div style="color: #70757a;">Google 提供: English</div>
            </body>
            </html>
            """
        else:
            page_content = f"""
            <html>
            <head><title>网页标题</title></head>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #1a73e8;">欢迎来到 {url}</h1>
            <p>这是一个模拟的浏览器界面，参考了 Google Chrome 的设计风格。</p>
            <h2 style="color: #1a73e8;">功能说明：</h2>
            <ul>
            <li>现代化的标签页设计</li>
            <li>简洁的地址栏</li>
            <li>后退/前进/刷新/主页按钮</li>
            <li>多标签页支持</li>
            <li>书签功能</li>
            <li>历史记录</li>
            </ul>
            <p style="color: #70757a;">当前时间: {t.strftime("%Y-%m-%d %H:%M:%S")}</p>
            </body>
            </html>
            """
        
        content_text.insert(tk.END, page_content)
        content_text.config(state=tk.DISABLED)
    
    browser_home()
    
    address_entry.bind("<Return>", lambda e: browser_navigate())
    
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

def minimize_window(window_frame):
    window_frame.place_forget()

def toggle_maximize(window_frame):
    if not hasattr(window_frame, 'maximized'):
        window_frame.maximized = False
        window_frame.normal_geometry = {"x": 0, "y": 0, "width": 500, "height": 400}
    
    if window_frame.maximized:
        window_frame.place(x=window_frame.normal_geometry["x"], 
                          y=window_frame.normal_geometry["y"],
                          width=window_frame.normal_geometry["width"],
                          height=window_frame.normal_geometry["height"])
        window_frame.maximized = False
    else:
        current_info = window_frame.place_info()
        window_frame.normal_geometry = {
            "x": int(current_info.get("x", 0)),
            "y": int(current_info.get("y", 0)),
            "width": int(current_info.get("width", 500)),
            "height": int(current_info.get("height", 400))
        }
        window_frame.place(x=0, y=0, width=800, height=560)
        window_frame.maximized = True

icon_positions = {}
desktop_files = []
desktop_icon_frames = {}
desktop_file_frames = {}

def on_search():
    search_text = search_entry.get().strip().lower()
    if not search_text:
        return
    
    found_apps = []
    for app_name, app_icon in desktop_icons:
        if search_text in app_name.lower():
            found_apps.append((app_name, app_icon))
    
    for file_data in desktop_files:
        if search_text in file_data["name"].lower():
            found_apps.append((file_data["name"], file_data["icon"]))
    
    if found_apps:
        if len(found_apps) == 1:
            app_name, app_icon = found_apps[0]
            open_application(app_name)
        else:
            show_search_results(found_apps)
    else:
        messagebox.showinfo("搜索结果", f"未找到与 '{search_text}' 匹配的应用或文件")

def show_search_results(results):
    dialog = tk.Toplevel(root)
    dialog.title("搜索结果")
    dialog.geometry("300x400")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.grab_set()
    
    dialog_frame = tk.Frame(dialog, bg="#f0f0f0")
    dialog_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(dialog_frame, text=f"找到 {len(results)} 个结果", bg="#f0f0f0").pack(pady=5)
    
    results_list = tk.Listbox(dialog_frame, bg="white", height=15)
    results_list.pack(fill=tk.BOTH, expand=True, pady=5)
    
    for app_name, app_icon in results:
        results_list.insert(tk.END, f"{app_icon} {app_name}")
    
    def on_select():
        selection = results_list.curselection()
        if selection:
            index = selection[0]
            app_name, app_icon = results[index]
            dialog.destroy()
            open_application(app_name)
    
    results_list.bind("<Double-Button-1>", lambda e: on_select())
    
    tk.Button(dialog_frame, text="打开", command=on_select).pack(pady=5)

def refresh_desktop_icons():
    global desktop_icon_frames, desktop_file_frames
    
    for frame in desktop_icon_frames.values():
        frame.destroy()
    
    for frame in desktop_file_frames.values():
        frame.destroy()
    
    desktop_icon_frames.clear()
    desktop_file_frames.clear()
    icon_positions.clear()
    
    for i, (name, icon) in enumerate(desktop_icons):
        icon_frame = tk.Frame(desktop, bg="#0078D7")
        initial_x = 20 + (i % 8) * 100
        initial_y = 20 + (i // 8) * 100
        icon_frame.place(x=initial_x, y=initial_y)
        icon_positions[name] = {"x": initial_x, "y": initial_y}
        desktop_icon_frames[name] = icon_frame
        
        icon_label = tk.Label(icon_frame, text=icon, font=("Arial", 32), bg="#0078D7")
        icon_label.pack()
        name_label = tk.Label(icon_frame, text=name, bg="#0078D7", fg="white", font=("Arial", 9))
        name_label.pack()
        
        def on_enter(event, frame=icon_frame, il=icon_label, nl=name_label):
            il.config(bg="#005a9e")
            nl.config(bg="#005a9e")
        
        def on_leave(event, frame=icon_frame, il=icon_label, nl=name_label):
            il.config(bg="#0078D7")
            nl.config(bg="#0078D7")
        
        icon_frame.bind("<Enter>", on_enter)
        icon_frame.bind("<Leave>", on_leave)
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
        name_label.bind("<Enter>", on_enter)
        name_label.bind("<Leave>", on_leave)
        
        drag_data = {"x": 0, "y": 0, "dragging": False}
        
        def on_drag_start(event, frame=icon_frame, data=drag_data, app_name=name):
            data["x"] = event.x
            data["y"] = event.y
            data["dragging"] = False
            frame.config(relief=tk.RIDGE, bd=3)
        
        def on_drag_motion(event, frame=icon_frame, data=drag_data, app_name=name):
            data["dragging"] = True
            x = event.x_root - data["x"] - frame.winfo_rootx() + frame.winfo_x()
            y = event.y_root - data["y"] - frame.winfo_rooty() + frame.winfo_y()
            frame.place(x=x, y=y)
        
        def on_drag_end(event, frame=icon_frame, data=drag_data, app_name=name):
            frame.config(relief=tk.FLAT, bd=0)
            if data["dragging"]:
                x = event.x_root - data["x"] - frame.winfo_rootx() + frame.winfo_x()
                y = event.y_root - data["y"] - frame.winfo_rooty() + frame.winfo_y()
                icon_positions[app_name] = {"x": x, "y": y}
            else:
                open_application(app_name)
        
        icon_frame.bind("<Button-1>", on_drag_start)
        icon_frame.bind("<B1-Motion>", on_drag_motion)
        icon_frame.bind("<ButtonRelease-1>", on_drag_end)
        
        icon_label.bind("<Button-1>", on_drag_start)
        icon_label.bind("<B1-Motion>", on_drag_motion)
        icon_label.bind("<ButtonRelease-1>", on_drag_end)
        
        name_label.bind("<Button-1>", on_drag_start)
        name_label.bind("<B1-Motion>", on_drag_motion)
        name_label.bind("<ButtonRelease-1>", on_drag_end)
    
    for i, file_data in enumerate(desktop_files):
        icon_frame = tk.Frame(desktop, bg="#0078D7")
        
        total_icons = len(desktop_icons) + i
        row = total_icons // 5
        col = total_icons % 5
        x = 20 + col * 100
        y = 20 + row * 100
        icon_frame.place(x=x, y=y)
        
        desktop_file_frames[file_data["name"]] = icon_frame
        
        icon_label = tk.Label(icon_frame, text=file_data["icon"], font=("Arial", 32), bg="#0078D7")
        icon_label.pack()
        name_label = tk.Label(icon_frame, text=file_data["name"], bg="#0078D7", fg="white", font=("Arial", 9))
        name_label.pack()
        
        def on_enter(event, frame=icon_frame, il=icon_label, nl=name_label):
            il.config(bg="#005a9e")
            nl.config(bg="#005a9e")
        
        def on_leave(event, frame=icon_frame, il=icon_label, nl=name_label):
            il.config(bg="#0078D7")
            nl.config(bg="#0078D7")
        
        icon_frame.bind("<Enter>", on_enter)
        icon_frame.bind("<Leave>", on_leave)
        icon_label.bind("<Enter>", on_enter)
        icon_label.bind("<Leave>", on_leave)
        name_label.bind("<Enter>", on_enter)
        name_label.bind("<Leave>", on_leave)
        
        drag_data = {"x": 0, "y": 0, "dragging": False}
        
        def on_drag_start(event, frame=icon_frame, data=drag_data):
            data["x"] = event.x
            data["y"] = event.y
            data["dragging"] = False
            frame.config(relief=tk.RIDGE, bd=3)
        
        def on_drag_motion(event, frame=icon_frame, data=drag_data):
            data["dragging"] = True
            x = event.x_root - data["x"] - frame.winfo_rootx() + frame.winfo_x()
            y = event.y_root - data["y"] - frame.winfo_rooty() + frame.winfo_y()
            frame.place(x=x, y=y)
        
        def on_drag_end(event, frame=icon_frame, data=drag_data):
            frame.config(relief=tk.FLAT, bd=0)
            if not data["dragging"]:
                open_file(file_data)
        
        icon_frame.bind("<Button-1>", on_drag_start)
        icon_frame.bind("<B1-Motion>", on_drag_motion)
        icon_frame.bind("<ButtonRelease-1>", on_drag_end)
        
        icon_label.bind("<Button-1>", on_drag_start)
        icon_label.bind("<B1-Motion>", on_drag_motion)
        icon_label.bind("<ButtonRelease-1>", on_drag_end)
        
        name_label.bind("<Button-1>", on_drag_start)
        name_label.bind("<B1-Motion>", on_drag_motion)
        name_label.bind("<ButtonRelease-1>", on_drag_end)

refresh_desktop_icons()

def create_linux_window():
    window_frame = tk.Frame(root, bg="#1e1e1e", relief=tk.RAISED, bd=2)
    window_frame.place(x=50, y=20, width=900, height=600)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 50, "y": 20, "width": 900, "height": 600}
    
    title_bar = tk.Frame(window_frame, bg="#2d2d2d", relief=tk.FLAT)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="🐧 LopingOS Linux", bg="#2d2d2d", fg="#4ec9b0", font=("Segoe UI", 10, "bold"))
    title_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    close_btn = tk.Button(title_bar, text="×", bg="#2d2d2d", fg="#cccccc", 
                         command=lambda: close_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    close_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#2d2d2d", fg="#cccccc",
                            command=lambda: toggle_maximize(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    maximize_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#2d2d2d", fg="#cccccc",
                            command=lambda: minimize_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    minimize_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    content = tk.Frame(window_frame, bg="#1e1e1e")
    content.pack(fill=tk.BOTH, expand=True)
    
    sidebar = tk.Frame(content, bg="#252526", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)
    
    sidebar_items = [
        ("系统状态", "📊"),
        ("服务管理", "⚙️"),
        ("硬件监控", "💻"),
        ("网络管理", "🌐"),
        ("存储管理", "💾"),
        ("用户管理", "👥"),
        ("内核参数", "🔧"),
        ("系统日志", "📝")
    ]
    
    current_panel = None
    
    for item, icon in sidebar_items:
        item_frame = tk.Frame(sidebar, bg="#252526")
        item_frame.pack(fill=tk.X, padx=5, pady=2)
        
        item_icon = tk.Label(item_frame, text=icon, bg="#252526", fg="#cccccc", font=("Segoe UI", 14))
        item_icon.pack(side=tk.LEFT, padx=10, pady=8)
        
        item_label = tk.Label(item_frame, text=item, bg="#252526", fg="#cccccc", font=("Segoe UI", 9))
        item_label.pack(side=tk.LEFT, padx=5, pady=8)
        
        def on_sidebar_enter(event, frame=item_frame):
            frame.config(bg="#37373d")
            for child in frame.winfo_children():
                child.config(bg="#37373d")
        
        def on_sidebar_leave(event, frame=item_frame):
            frame.config(bg="#252526")
            for child in frame.winfo_children():
                child.config(bg="#252526")
        
        item_frame.bind("<Enter>", on_sidebar_enter)
        item_frame.bind("<Leave>", on_sidebar_leave)
        item_icon.bind("<Enter>", on_sidebar_enter)
        item_icon.bind("<Leave>", on_sidebar_leave)
        item_label.bind("<Enter>", on_sidebar_enter)
        item_label.bind("<Leave>", on_sidebar_leave)
    
    main_panel = tk.Frame(content, bg="#1e1e1e")
    main_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    status_frame = tk.Frame(main_panel, bg="#252526", relief=tk.FLAT, bd=1)
    status_frame.pack(fill=tk.X, pady=5)
    
    tk.Label(status_frame, text="🐧 Linux 6.6.0 | Ubuntu 24.04 LTS", bg="#252526", fg="#4ec9b0", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
    
    status_label = tk.Label(status_frame, text="状态: 未运行", bg="#252526", fg="#f14c4c", font=("Segoe UI", 9))
    status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    uptime_label = tk.Label(status_frame, text="运行时间: 00:00:00", bg="#252526", fg="#cccccc", font=("Segoe UI", 9))
    uptime_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    info_frame = tk.Frame(main_panel, bg="#252526")
    info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    info_text = tk.Text(info_frame, bg="#1e1e1e", fg="#cccccc", font=("Consolas", 10), 
                       relief=tk.FLAT, bd=0, wrap=tk.WORD, state=tk.DISABLED)
    info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_info():
        try:
            import requests
            response = requests.get('http://localhost:6000/api/status', timeout=1)
            if response.status_code == 200:
                data = response.json()
                status_label.config(text=f"状态: 运行中", fg="#4ec9b0")
                uptime_label.config(text=f"运行时间: {data.get('uptime', '00:00:00')}")
                
                info_text.config(state=tk.NORMAL)
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, "🐧 LopingOS Linux 系统信息\n")
                info_text.insert(tk.END, "=" * 50 + "\n\n")
                info_text.insert(tk.END, f"Linux版本: {data.get('linux_version', 'N/A')}\n")
                info_text.insert(tk.END, f"内核版本: {data.get('kernel_version', 'N/A')}\n")
                info_text.insert(tk.END, f"发行版: {data.get('distribution', 'N/A')}\n")
                info_text.insert(tk.END, f"启动时间: {data.get('boot_time', 'N/A')}\n")
                info_text.insert(tk.END, f"运行时间: {data.get('uptime', 'N/A')}\n")
                info_text.insert(tk.END, f"服务状态: {data.get('services_count', 0)}/{data.get('total_services', 0)}\n\n")
                info_text.insert(tk.END, "📡 Web界面: http://localhost:6000\n")
                info_text.insert(tk.END, "📊 API接口: http://localhost:6000/api/status\n\n")
                info_text.insert(tk.END, "可用API端点:\n")
                info_text.insert(tk.END, "  /api/status     - 系统状态\n")
                info_text.insert(tk.END, "  /api/services   - 服务状态\n")
                info_text.insert(tk.END, "  /api/hardware   - 硬件状态\n")
                info_text.insert(tk.END, "  /api/network    - 网络状态\n")
                info_text.insert(tk.END, "  /api/storage    - 存储状态\n")
                info_text.insert(tk.END, "  /api/processes  - 进程列表\n")
                info_text.insert(tk.END, "  /api/users      - 用户信息\n")
                info_text.insert(tk.END, "  /api/sysctl     - 内核参数\n")
                info_text.insert(tk.END, "  /api/logs       - 系统日志\n")
                info_text.config(state=tk.DISABLED)
            else:
                status_label.config(text="状态: 未运行", fg="#f14c4c")
                info_text.config(state=tk.NORMAL)
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, "🐧 LopingOS Linux 模拟系统\n")
                info_text.insert(tk.END, "=" * 50 + "\n\n")
                info_text.insert(tk.END, "Linux系统未运行\n\n")
                info_text.insert(tk.END, "请启动Linux系统:\n")
                info_text.insert(tk.END, "1. 打开终端\n")
                info_text.insert(tk.END, "2. 切换到Linux目录: cd 配置/Linux\n")
                info_text.insert(tk.END, "3. 运行启动脚本: start_linux.bat\n\n")
                info_text.insert(tk.END, "或直接双击: 配置/Linux/start_linux.bat\n\n")
                info_text.insert(tk.END, "启动后访问: http://localhost:6000\n")
                info_text.config(state=tk.DISABLED)
        except:
            status_label.config(text="状态: 未运行", fg="#f14c4c")
            info_text.config(state=tk.NORMAL)
            info_text.delete(1.0, tk.END)
            info_text.insert(tk.END, "🐧 LopingOS Linux 模拟系统\n")
            info_text.insert(tk.END, "=" * 50 + "\n\n")
            info_text.insert(tk.END, "Linux系统未运行\n\n")
            info_text.insert(tk.END, "请启动Linux系统:\n")
            info_text.insert(tk.END, "1. 打开终端\n")
            info_text.insert(tk.END, "2. 切换到Linux目录: cd 配置/Linux\n")
            info_text.insert(tk.END, "3. 运行启动脚本: start_linux.bat\n\n")
            info_text.insert(tk.END, "或直接双击: 配置/Linux/start_linux.bat\n\n")
            info_text.insert(tk.END, "启动后访问: http://localhost:6000\n")
            info_text.config(state=tk.DISABLED)
    
    def open_web_browser():
        import webbrowser
        webbrowser.open('http://localhost:6000')
    
    button_frame = tk.Frame(main_panel, bg="#252526")
    button_frame.pack(fill=tk.X, pady=5)
    
    refresh_btn = tk.Button(button_frame, text="🔄 刷新状态", bg="#0e639c", fg="white", 
                          font=("Segoe UI", 9), command=update_info, relief=tk.FLAT, padx=10)
    refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    web_btn = tk.Button(button_frame, text="🌐 打开Web界面", bg="#0e639c", fg="white", 
                       font=("Segoe UI", 9), command=open_web_browser, relief=tk.FLAT, padx=10)
    web_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    update_info()
    window_frame.after(5000, update_info)

def create_deploy_window():
    window_frame = tk.Frame(root, bg="#1e1e1e", relief=tk.RAISED, bd=2)
    window_frame.place(x=50, y=20, width=900, height=600)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 50, "y": 20, "width": 900, "height": 600}
    
    title_bar = tk.Frame(window_frame, bg="#2d2d2d", relief=tk.FLAT)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="🚀 LopingOS 部署管理", bg="#2d2d2d", fg="#4ec9b0", font=("Segoe UI", 10, "bold"))
    title_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    close_btn = tk.Button(title_bar, text="×", bg="#2d2d2d", fg="#cccccc", 
                         command=lambda: close_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    close_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#2d2d2d", fg="#cccccc",
                            command=lambda: toggle_maximize(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    maximize_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#2d2d2d", fg="#cccccc",
                            command=lambda: minimize_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    minimize_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    content = tk.Frame(window_frame, bg="#1e1e1e")
    content.pack(fill=tk.BOTH, expand=True)
    
    sidebar = tk.Frame(content, bg="#252526", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar.pack_propagate(False)
    
    sidebar_items = [
        ("系统状态", "📊"),
        ("项目管理", "📁"),
        ("环境管理", "🌍"),
        ("部署目标", "🎯"),
        ("部署操作", "🚀"),
        ("部署历史", "📋"),
        ("系统日志", "📝")
    ]
    
    for item, icon in sidebar_items:
        item_frame = tk.Frame(sidebar, bg="#252526")
        item_frame.pack(fill=tk.X, padx=5, pady=2)
        
        item_icon = tk.Label(item_frame, text=icon, bg="#252526", fg="#cccccc", font=("Segoe UI", 14))
        item_icon.pack(side=tk.LEFT, padx=10, pady=8)
        
        item_label = tk.Label(item_frame, text=item, bg="#252526", fg="#cccccc", font=("Segoe UI", 9))
        item_label.pack(side=tk.LEFT, padx=5, pady=8)
        
        def on_sidebar_enter(event, frame=item_frame):
            frame.config(bg="#37373d")
            for child in frame.winfo_children():
                child.config(bg="#37373d")
        
        def on_sidebar_leave(event, frame=item_frame):
            frame.config(bg="#252526")
            for child in frame.winfo_children():
                child.config(bg="#252526")
        
        item_frame.bind("<Enter>", on_sidebar_enter)
        item_frame.bind("<Leave>", on_sidebar_leave)
        item_icon.bind("<Enter>", on_sidebar_enter)
        item_icon.bind("<Leave>", on_sidebar_leave)
        item_label.bind("<Enter>", on_sidebar_enter)
        item_label.bind("<Leave>", on_sidebar_leave)
    
    main_panel = tk.Frame(content, bg="#1e1e1e")
    main_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    status_frame = tk.Frame(main_panel, bg="#252526", relief=tk.FLAT, bd=1)
    status_frame.pack(fill=tk.X, pady=5)
    
    tk.Label(status_frame, text="🚀 LopingOS Deploy Manager v1.0.0", bg="#252526", fg="#4ec9b0", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
    
    status_label = tk.Label(status_frame, text="状态: 未运行", bg="#252526", fg="#f14c4c", font=("Segoe UI", 9))
    status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    uptime_label = tk.Label(status_frame, text="运行时间: 00:00:00", bg="#252526", fg="#cccccc", font=("Segoe UI", 9))
    uptime_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    info_frame = tk.Frame(main_panel, bg="#252526")
    info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    info_text = tk.Text(info_frame, bg="#1e1e1e", fg="#cccccc", font=("Consolas", 10), 
                       relief=tk.FLAT, bd=0, wrap=tk.WORD, state=tk.DISABLED)
    info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def update_info():
        try:
            import requests
            response = requests.get('http://localhost:7000/api/status', timeout=1)
            if response.status_code == 200:
                data = response.json()
                status_label.config(text=f"状态: 运行中", fg="#4ec9b0")
                uptime_label.config(text=f"运行时间: {data.get('uptime', '00:00:00')}")
                
                info_text.config(state=tk.NORMAL)
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, "🚀 LopingOS 部署管理系统\n")
                info_text.insert(tk.END, "=" * 50 + "\n\n")
                info_text.insert(tk.END, f"版本: {data.get('version', 'N/A')}\n")
                info_text.insert(tk.END, f"启动时间: {data.get('start_time', 'N/A')}\n")
                info_text.insert(tk.END, f"运行时间: {data.get('uptime', 'N/A')}\n")
                info_text.insert(tk.END, f"项目数量: {data.get('projects_count', 0)}\n")
                info_text.insert(tk.END, f"部署目标: {data.get('targets_count', 0)}\n")
                info_text.insert(tk.END, f"部署历史: {data.get('deployments_count', 0)}\n\n")
                info_text.insert(tk.END, "📡 Web界面: http://localhost:7000\n")
                info_text.insert(tk.END, "📊 API接口: http://localhost:7000/api/status\n\n")
                info_text.insert(tk.END, "可用API端点:\n")
                info_text.insert(tk.END, "  /api/status     - 系统状态\n")
                info_text.insert(tk.END, "  /api/projects   - 项目列表\n")
                info_text.insert(tk.END, "  /api/environments - 环境列表\n")
                info_text.insert(tk.END, "  /api/targets    - 部署目标\n")
                info_text.insert(tk.END, "  /api/deployments - 部署历史\n")
                info_text.insert(tk.END, "  /api/logs       - 系统日志\n")
                info_text.insert(tk.END, "  POST /api/deploy - 部署项目\n")
                info_text.config(state=tk.DISABLED)
            else:
                status_label.config(text="状态: 未运行", fg="#f14c4c")
                info_text.config(state=tk.NORMAL)
                info_text.delete(1.0, tk.END)
                info_text.insert(tk.END, "🚀 LopingOS 部署管理系统\n")
                info_text.insert(tk.END, "=" * 50 + "\n\n")
                info_text.insert(tk.END, "部署系统未运行\n\n")
                info_text.insert(tk.END, "请启动部署系统:\n")
                info_text.insert(tk.END, "1. 打开终端\n")
                info_text.insert(tk.END, "2. 切换到部署目录: cd 部署\n")
                info_text.insert(tk.END, "3. 运行启动脚本: start_deploy.bat\n\n")
                info_text.insert(tk.END, "或直接双击: 部署/start_deploy.bat\n\n")
                info_text.insert(tk.END, "启动后访问: http://localhost:7000\n")
                info_text.config(state=tk.DISABLED)
        except:
            status_label.config(text="状态: 未运行", fg="#f14c4c")
            info_text.config(state=tk.NORMAL)
            info_text.delete(1.0, tk.END)
            info_text.insert(tk.END, "🚀 LopingOS 部署管理系统\n")
            info_text.insert(tk.END, "=" * 50 + "\n\n")
            info_text.insert(tk.END, "部署系统未运行\n\n")
            info_text.insert(tk.END, "请启动部署系统:\n")
            info_text.insert(tk.END, "1. 打开终端\n")
            info_text.insert(tk.END, "2. 切换到部署目录: cd 部署\n")
            info_text.insert(tk.END, "3. 运行启动脚本: start_deploy.bat\n\n")
            info_text.insert(tk.END, "或直接双击: 部署/start_deploy.bat\n\n")
            info_text.insert(tk.END, "启动后访问: http://localhost:7000\n")
            info_text.config(state=tk.DISABLED)
    
    def open_web_browser():
        import webbrowser
        webbrowser.open('http://localhost:7000')
    
    button_frame = tk.Frame(main_panel, bg="#252526")
    button_frame.pack(fill=tk.X, pady=5)
    
    refresh_btn = tk.Button(button_frame, text="🔄 刷新状态", bg="#0e639c", fg="white", 
                          font=("Segoe UI", 9), command=update_info, relief=tk.FLAT, padx=10)
    refresh_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    web_btn = tk.Button(button_frame, text="🌐 打开Web界面", bg="#0e639c", fg="white", 
                       font=("Segoe UI", 9), command=open_web_browser, relief=tk.FLAT, padx=10)
    web_btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    update_info()
    window_frame.after(5000, update_info)

def create_crawler_window():
    if not CRAWLER_AVAILABLE:
        messagebox.showerror("错误", "爬虫模块未安装或导入失败")
        return
    
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=1000, height=700)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 100, "y": 50, "width": 1000, "height": 700}
    
    title_bar = tk.Frame(window_frame, bg="#0078D7", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="🕷️ 网页爬虫", bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"))
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#0078D7", fg="white", 
                         command=lambda: close_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#0078D7", fg="white",
                            command=lambda: toggle_maximize(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#0078D7", fg="white",
                            command=lambda: minimize_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="#f0f0f0")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    crawler_window = tk.Toplevel(root)
    crawler_window.title("网页爬虫")
    crawler_window.geometry("1000x700")
    crawler_window.transient(root)
    crawler_window.grab_set()
    
    app = WebCrawlerGUI(crawler_window)
    
    def on_crawler_close():
        crawler_window.destroy()
        close_window(window_frame)
    
    crawler_window.protocol("WM_DELETE_WINDOW", on_crawler_close)
    
    windows.append(window_frame)
    return window_frame

def create_ai_assistant_window():
    window_frame = tk.Frame(root, bg="#ffffff", relief=tk.RAISED, bd=2)
    window_frame.place(x=100, y=50, width=800, height=600)
    window_frame.maximized = False
    window_frame.normal_geometry = {"x": 100, "y": 50, "width": 800, "height": 600}
    
    title_bar = tk.Frame(window_frame, bg="#0078D7", relief=tk.RAISED)
    title_bar.pack(fill=tk.X)
    
    title_label = tk.Label(title_bar, text="AI助手", bg="#0078D7", fg="white", font=("Segoe UI", 10))
    title_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    close_btn = tk.Button(title_bar, text="×", bg="#0078D7", fg="white", 
                         command=lambda: close_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    close_btn.pack(side=tk.RIGHT, padx=2)
    
    maximize_btn = tk.Button(title_bar, text="□", bg="#0078D7", fg="white",
                            command=lambda: toggle_maximize(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    maximize_btn.pack(side=tk.RIGHT, padx=2)
    
    minimize_btn = tk.Button(title_bar, text="−", bg="#0078D7", fg="white",
                            command=lambda: minimize_window(window_frame), relief=tk.FLAT, font=("Segoe UI", 10))
    minimize_btn.pack(side=tk.RIGHT, padx=2)
    
    content = tk.Frame(window_frame, bg="#f0f0f0")
    content.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
    
    # 创建主面板
    main_panel = tk.Frame(content, bg="white")
    main_panel.pack(fill=tk.BOTH, expand=True)
    
    # 创建聊天区域
    chat_frame = tk.Frame(main_panel, bg="white")
    chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # 聊天历史
    chat_history = tk.Text(chat_frame, bg="#f5f5f5", fg="#333333", 
                         font=("Segoe UI", 11), wrap=tk.WORD, 
                         relief=tk.FLAT, bd=1, highlightbackground="#e0e0e0")
    chat_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    chat_history.config(state=tk.DISABLED)
    
    # 输入区域
    input_frame = tk.Frame(chat_frame, bg="white", relief=tk.FLAT, bd=1, highlightbackground="#e0e0e0")
    input_frame.pack(fill=tk.X, padx=5, pady=5)
    
    input_text = tk.Text(input_frame, bg="white", fg="#333333", 
                        font=("Segoe UI", 11), wrap=tk.WORD, 
                        height=3, relief=tk.FLAT, bd=0)
    input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # 发送按钮
    send_btn = create_windows_button(input_frame, text="发送", bg="#0078D7", fg="white", 
                                   font=("Segoe UI", 10), command=lambda: send_message())
    send_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # AI工具面板
    tools_frame = tk.Frame(content, bg="#f0f0f0", height=100)
    tools_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
    tools_frame.pack_propagate(False)
    
    tools_label = tk.Label(tools_frame, text="AI工具", font=("Segoe UI", 10, "bold"), bg="#f0f0f0")
    tools_label.pack(anchor=tk.W, padx=5, pady=5)
    
    tools_buttons = tk.Frame(tools_frame, bg="#f0f0f0")
    tools_buttons.pack(fill=tk.X, padx=5, pady=5)
    
    def create_tool_button(text, icon, command):
        btn = tk.Button(tools_buttons, text=f"{icon} {text}", 
                      bg="white", fg="#333333", font=("Segoe UI", 9), 
                      relief=tk.FLAT, bd=1, highlightbackground="#e0e0e0",
                      command=command)
        btn.pack(side=tk.LEFT, padx=5, pady=2)
        return btn
    
    # 添加工具按钮
    create_tool_button("智能问答", "💬", lambda: insert_prompt("智能问答: "))
    create_tool_button("代码生成", "💻", lambda: insert_prompt("生成代码: "))
    create_tool_button("文本摘要", "📝", lambda: insert_prompt("摘要: "))
    create_tool_button("创意写作", "✍️", lambda: insert_prompt("写作: "))
    create_tool_button("翻译", "🌐", lambda: insert_prompt("翻译: "))
    create_tool_button("Torch AI", "🔥", lambda: insert_prompt("Torch AI: "))
    create_tool_button("深度学习", "🧠", lambda: insert_prompt("深度学习: "))
    
    # 智能建议
    suggestions_frame = tk.Frame(content, bg="#f0f0f0", height=80)
    suggestions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
    suggestions_frame.pack_propagate(False)
    
    suggestions_label = tk.Label(suggestions_frame, text="智能建议", font=("Segoe UI", 10, "bold"), bg="#f0f0f0")
    suggestions_label.pack(anchor=tk.W, padx=5, pady=5)
    
    suggestions_buttons = tk.Frame(suggestions_frame, bg="#f0f0f0")
    suggestions_buttons.pack(fill=tk.X, padx=5, pady=5)
    
    suggestions = [
        "如何使用系统的部署功能？",
        "创建一个简单的Python脚本",
        "解释什么是AI机器学习",
        "如何优化系统性能？"
    ]
    
    for suggestion in suggestions:
        btn = tk.Button(suggestions_buttons, text=suggestion, 
                      bg="white", fg="#0078D7", font=("Segoe UI", 9), 
                      relief=tk.FLAT, bd=1, highlightbackground="#e0e0e0",
                      command=lambda s=suggestion: insert_suggestion(s))
        btn.pack(side=tk.LEFT, padx=5, pady=2)
    
    # 发送消息函数
    def send_message():
        message = input_text.get(1.0, tk.END).strip()
        if not message:
            return
        
        # 显示用户消息
        display_message("你", message, "#0078D7")
        
        # 清空输入
        input_text.delete(1.0, tk.END)
        
        # 显示AI正在输入
        display_message("AI", "正在思考...", "#666666")
        
        # 模拟AI响应
        import threading
        threading.Thread(target=generate_response, args=(message,)).start()
    
    # 生成AI响应
    def generate_response(message):
        import time
        time.sleep(1)  # 模拟思考时间
        
        # 简单的响应逻辑
        response = ""
        message_lower = message.lower()
        
        if "部署" in message_lower:
            response = "部署功能可以通过部署管理器使用。你可以创建项目，配置环境，然后选择部署策略（如直接部署、滚动部署、蓝绿部署或金丝雀部署）来发布你的应用程序。"
        elif "代码" in message_lower or "脚本" in message_lower:
            response = "这是一个简单的Python脚本示例：\n\n"\
                      "def hello_world():\n"\
                      "    print('Hello, LopingOS!')\n"\
                      "\n"\
                      "if __name__ == '__main__':\n"\
                      "    hello_world()"
        elif "ai" in message_lower or "机器学习" in message_lower:
            response = "人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。机器学习是AI的一个子集，它使计算机能够从数据中学习而不需要明确编程。"
        elif "优化" in message_lower or "性能" in message_lower:
            response = "要优化系统性能，你可以：\n1. 关闭不需要的应用程序\n2. 清理临时文件\n3. 增加系统内存\n4. 使用SSD存储\n5. 定期更新系统\n6. 优化启动项"
        elif "torch" in message_lower or "深度学习" in message_lower:
            if TORCH_AVAILABLE:
                response = "Torch库已成功安装！\n\n"\
                          f"Torch版本: {torch.__version__}\n"\
                          f"CUDA可用: {torch.cuda.is_available()}\n"\
                          f"CUDA设备数: {torch.cuda.device_count()}\n\n"\
                          "你可以使用Torch进行深度学习任务，如：\n"\
                          "1. 构建神经网络\n"\
                          "2. 训练模型\n"\
                          "3. 进行推理\n"\
                          "4. 图像处理\n"\
                          "5. 自然语言处理"
            else:
                response = "Torch库未安装。你可以通过以下命令安装：\n\n"\
                          "pip install torch torchvision torchaudio\n\n"\
                          "安装后，你将能够使用Torch进行深度学习任务。"
        else:
            response = f"我是LopingOS的AI助手，很高兴为你服务！你刚才提到：{message}\n\n我可以帮助你了解系统功能、生成代码、提供技术支持，或者回答你的问题。"
        
        # 更新聊天历史，移除"正在思考"消息并添加实际响应
        root.after(100, lambda: update_ai_response(response))
    
    # 更新AI响应
    def update_ai_response(response):
        # 移除"正在思考"消息
        chat_history.config(state=tk.NORMAL)
        lines = chat_history.get(1.0, tk.END).split('\n')
        if len(lines) > 2 and lines[-3].startswith("AI: ") and lines[-3].endswith("正在思考..."):
            chat_history.delete(f"end-{len(lines[-3])+1}c", tk.END)
        # 添加实际响应
        chat_history.insert(tk.END, f"AI: {response}\n\n", ("ai",))
        chat_history.config(state=tk.DISABLED)
        chat_history.see(tk.END)
    
    # 显示消息
    def display_message(sender, message, color):
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"{sender}: {message}\n\n", (sender.lower(),))
        chat_history.config(state=tk.DISABLED)
        chat_history.see(tk.END)
    
    # 插入提示
    def insert_prompt(prompt):
        input_text.insert(tk.END, prompt)
        input_text.focus_set()
    
    # 插入建议
    def insert_suggestion(suggestion):
        input_text.delete(1.0, tk.END)
        input_text.insert(tk.END, suggestion)
        input_text.focus_set()
    
    # 绑定回车键发送消息
    def on_enter_press(event):
        if not (event.state & 0x0001):  # 没有按下Shift键
            send_message()
            return "break"
    
    input_text.bind("<Return>", on_enter_press)
    
    # 设置输入框焦点
    input_text.focus_set()
    
    # 初始欢迎消息
    def init_welcome_message():
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, "🤖 LopingOS AI助手\n", ("ai",))
        chat_history.insert(tk.END, "=" * 50 + "\n\n", ("ai",))
        chat_history.insert(tk.END, "你好！我是LopingOS的AI助手，很高兴为你服务。\n\n", ("ai",))
        chat_history.insert(tk.END, "我可以帮助你：\n", ("ai",))
        chat_history.insert(tk.END, "• 了解系统功能和使用方法\n", ("ai",))
        chat_history.insert(tk.END, "• 生成代码和脚本\n", ("ai",))
        chat_history.insert(tk.END, "• 回答技术问题\n", ("ai",))
        chat_history.insert(tk.END, "• 提供系统优化建议\n", ("ai",))
        chat_history.insert(tk.END, "• 帮助你使用部署功能\n\n", ("ai",))
        chat_history.insert(tk.END, "请输入你的问题或指令，我会尽力帮助你！\n\n", ("ai",))
        chat_history.config(state=tk.DISABLED)
        chat_history.see(tk.END)
    
    # 配置文本标签
    chat_history.tag_config("你", foreground="#0078D7", font=("Segoe UI", 11, "bold"))
    chat_history.tag_config("ai", foreground="#666666", font=("Segoe UI", 11))
    
    # 初始化欢迎消息
    init_welcome_message()
    
    # 拖动窗口
    window_frame.drag_data = {"x": 0, "y": 0}
    
    def start_drag(event):
        window_frame.drag_data["x"] = event.x
        window_frame.drag_data["y"] = event.y
    
    def do_drag(event):
        x = event.x_root - window_frame.drag_data["x"]
        y = event.y_root - window_frame.drag_data["y"]
        window_frame.place(x=x, y=y)
    
    title_bar.bind("<Button-1>", start_drag)
    title_bar.bind("<B1-Motion>", do_drag)
    
    windows.append(window_frame)
    return window_frame

if __name__ == "__main__":
    # 初始化桌面图标
    refresh_desktop_icons()
    root.mainloop()