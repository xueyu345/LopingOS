import os
from os_environment import *

def print_environment_info():
    print(f"系统名称: {os.environ.get('OS_NAME')}")
    print(f"系统版本: {os.environ.get('OS_VERSION')}")
    print(f"系统构建: {os.environ.get('OS_BUILD')}")
    print(f"完整版本: {os.environ.get('OS_FULL_VERSION')}")
    print(f"Shell: {os.environ.get('-shell')}")
    print(f"终端: {os.environ.get('-terminal')}")
    print(f"模拟器: {os.environ.get('-emulator')}")
    print()

def print_directories():
    print("系统目录:")
    print(f"  基础目录: {os.environ.get('OS_BASE_DIR')}")
    print(f"  主目录: {os.environ.get('OS_HOME_DIR')}")
    print(f"  配置目录: {os.environ.get('OS_CONFIG_DIR')}")
    print(f"  数据目录: {os.environ.get('OS_DATA_DIR')}")
    print(f"  日志目录: {os.environ.get('OS_LOG_DIR')}")
    print(f"  应用目录: {os.environ.get('OS_APPS_DIR')}")
    print(f"  插件目录: {os.environ.get('OS_PLUGINS_DIR')}")
    print()

def print_system_info():
    print("系统信息:")
    print(f"  平台: {os.environ.get('OS_PLATFORM')}")
    print(f"  架构: {os.environ.get('OS_ARCH')}")
    print(f"  Python版本: {os.environ.get('OS_PYTHON_VERSION')}")
    print(f"  调试模式: {os.environ.get('OS_DEBUG')}")
    print(f"  日志级别: {os.environ.get('OS_LOG_LEVEL')}")
    print(f"  主题: {os.environ.get('OS_THEME')}")
    print(f"  语言: {os.environ.get('OS_LANGUAGE')}")
    print(f"  时区: {os.environ.get('OS_TIMEZONE')}")
    print()

def print_ui_settings():
    print("界面设置:")
    print(f"  窗口宽度: {os.environ.get('OS_APP_WINDOW_WIDTH')}")
    print(f"  窗口高度: {os.environ.get('OS_APP_WINDOW_HEIGHT')}")
    print(f"  字体: {os.environ.get('OS_FONT_FAMILY')}")
    print(f"  字号: {os.environ.get('OS_FONT_SIZE')}")
    print(f"  圆角: {os.environ.get('OS_BORDER_RADIUS')}")
    print(f"  动画: {os.environ.get('OS_ANIMATION_ENABLED')}")
    print()

def print_shortcuts():
    print("快捷键:")
    print(f"  新建: {os.environ.get('OS_SHORTCUT_NEW_FILE')}")
    print(f"  打开: {os.environ.get('OS_SHORTCUT_OPEN_FILE')}")
    print(f"  保存: {os.environ.get('OS_SHORTCUT_SAVE_FILE')}")
    print(f"  关闭: {os.environ.get('OS_SHORTCUT_CLOSE_WINDOW')}")
    print(f"  退出: {os.environ.get('OS_SHORTCUT_QUIT')}")
    print(f"  全屏: {os.environ.get('OS_SHORTCUT_FULLSCREEN')}")
    print(f"  设置: {os.environ.get('OS_SHORTCUT_SETTINGS')}")
    print()

def get_env_var(key, default=None):
    return os.environ.get(key, default)

def set_env_var(key, value):
    os.environ[key] = str(value)

if __name__ == "__main__":
    print("=" * 50)
    print("LopingsOS 环境变量系统")
    print("=" * 50)
    print()
    
    print_environment_info()
    print_directories()
    print_system_info()
    print_ui_settings()
    print_shortcuts()
    
    print("=" * 50)
    print("使用示例:")
    print("=" * 50)
    print()
    
    print(f"获取系统版本: {get_env_var('OS_VERSION')}")
    print(f"获取配置目录: {get_env_var('OS_CONFIG_DIR')}")
    print(f"获取日志文件: {get_env_var('OS_LOG_FILE')}")
    print()
    
    set_env_var("OS_CUSTOM_VAR", "自定义值")
    print(f"设置自定义变量: {get_env_var('OS_CUSTOM_VAR')}")
