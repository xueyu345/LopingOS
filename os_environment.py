import os
import sys
import platform

OS_NAME = "LopingsOS"
OS_VERSION = "1.0.0"
OS_BUILD = "2025.02.18"

os.environ["OS_NAME"] = OS_NAME
os.environ["OS_VERSION"] = OS_VERSION
os.environ["OS_BUILD"] = OS_BUILD
os.environ["OS_FULL_VERSION"] = f"{OS_VERSION}-{OS_BUILD}"

os.environ["-v"] = OS_VERSION
os.environ["-shell"] = f"{OS_NAME}-Shell"
os.environ["-terminal"] = f"{OS_NAME}-Terminal"
os.environ["-emulator"] = f"{OS_NAME}-Emulator"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["OS_BASE_DIR"] = BASE_DIR

os.environ["OS_HOME_DIR"] = os.path.join(BASE_DIR, "home")
os.environ["OS_CONFIG_DIR"] = os.path.join(BASE_DIR, "config")
os.environ["OS_DATA_DIR"] = os.path.join(BASE_DIR, "data")
os.environ["OS_LOG_DIR"] = os.path.join(BASE_DIR, "logs")
os.environ["OS_TEMP_DIR"] = os.path.join(BASE_DIR, "temp")
os.environ["OS_CACHE_DIR"] = os.path.join(BASE_DIR, "cache")
os.environ["OS_APPS_DIR"] = os.path.join(BASE_DIR, "apps")
os.environ["OS_PLUGINS_DIR"] = os.path.join(BASE_DIR, "plugins")
os.environ["OS_SCRIPTS_DIR"] = os.path.join(BASE_DIR, "scripts")
os.environ["OS_LIB_DIR"] = os.path.join(BASE_DIR, "lib")
os.environ["OS_BIN_DIR"] = os.path.join(BASE_DIR, "bin")

os.environ["OS_CONFIG_FILE"] = os.path.join(os.environ["OS_CONFIG_DIR"], "config.json")
os.environ["OS_SETTINGS_FILE"] = os.path.join(os.environ["OS_CONFIG_DIR"], "settings.json")
os.environ["OS_USER_FILE"] = os.path.join(os.environ["OS_CONFIG_DIR"], "users.json")
os.environ["OS_LOG_FILE"] = os.path.join(os.environ["OS_LOG_DIR"], "system.log")
os.environ["OS_ERROR_LOG_FILE"] = os.path.join(os.environ["OS_LOG_DIR"], "error.log")

os.environ["OS_PATH_SEPARATOR"] = ";" if platform.system() == "Windows" else ":"
os.environ["OS_LINE_SEPARATOR"] = "\r\n" if platform.system() == "Windows" else "\n"
os.environ["OS_PLATFORM"] = platform.system()
os.environ["OS_ARCH"] = platform.machine()
os.environ["OS_PYTHON_VERSION"] = platform.python_version()

os.environ["OS_DEBUG"] = "false"
os.environ["OS_LOG_LEVEL"] = "INFO"
os.environ["OS_MAX_LOG_SIZE"] = "10485760"
os.environ["OS_LOG_BACKUP_COUNT"] = "5"

os.environ["OS_THEME"] = "light"
os.environ["OS_LANGUAGE"] = "zh-CN"
os.environ["OS_TIMEZONE"] = "Asia/Shanghai"
os.environ["OS_DATE_FORMAT"] = "%Y-%m-%d"
os.environ["OS_TIME_FORMAT"] = "%H:%M:%S"
os.environ["OS_DATETIME_FORMAT"] = "%Y-%m-%d %H:%M:%S"

os.environ["OS_SESSION_ID"] = os.urandom(16).hex()
os.environ["OS_STARTUP_TIME"] = str(os.path.getctime(__file__))
os.environ["OS_UPTIME"] = "0"

os.environ["OS_NETWORK_ENABLED"] = "true"
os.environ["OS_SOUND_ENABLED"] = "true"
os.environ["OS_AUTO_SAVE"] = "true"
os.environ["OS_AUTO_SAVE_INTERVAL"] = "300"

os.environ["OS_MAX_MEMORY"] = "1073741824"
os.environ["OS_MAX_CPU_USAGE"] = "80"
os.environ["OS_MAX_DISK_USAGE"] = "90"

os.environ["OS_APP_WINDOW_WIDTH"] = "800"
os.environ["OS_APP_WINDOW_HEIGHT"] = "600"
os.environ["OS_APP_MIN_WIDTH"] = "400"
os.environ["OS_APP_MIN_HEIGHT"] = "300"

os.environ["OS_FONT_FAMILY"] = "Microsoft YaHei"
os.environ["OS_FONT_SIZE"] = "12"
os.environ["OS_FONT_WEIGHT"] = "normal"

os.environ["OS_BORDER_RADIUS"] = "8"
os.environ["OS_SHADOW_ENABLED"] = "true"
os.environ["OS_ANIMATION_ENABLED"] = "true"
os.environ["OS_ANIMATION_DURATION"] = "300"

os.environ["OS_CLIPBOARD_ENABLED"] = "true"
os.environ["OS_DRAG_DROP_ENABLED"] = "true"
os.environ["OS_MULTI_WINDOW_ENABLED"] = "true"
os.environ["OS_FULLSCREEN_ENABLED"] = "true"

os.environ["OS_SECURITY_LEVEL"] = "medium"
os.environ["OS_ENCRYPTION_ENABLED"] = "false"
os.environ["OS_BACKUP_ENABLED"] = "true"
os.environ["OS_BACKUP_INTERVAL"] = "86400"

os.environ["OS_UPDATE_CHECK_ENABLED"] = "true"
os.environ["OS_UPDATE_AUTO_DOWNLOAD"] = "false"
os.environ["OS_UPDATE_SERVER"] = "https://api.lopingsos.com"
os.environ["OS_UPDATE_CHANNEL"] = "stable"

os.environ["OS_TELEMETRY_ENABLED"] = "false"
os.environ["OS_TELEMETRY_URL"] = "https://telemetry.lopingsos.com"

os.environ["OS_SUPPORT_EMAIL"] = "support@lopingsos.com"
os.environ["OS_SUPPORT_URL"] = "https://support.lopingsos.com"
os.environ["OS_DOCUMENTATION_URL"] = "https://docs.lopingsos.com"
os.environ["OS_COMMUNITY_URL"] = "https://community.lopingsos.com"

os.environ["OS_LICENSE"] = "MIT"
os.environ["OS_AUTHOR"] = "LopingsOS Team"
os.environ["OS_WEBSITE"] = "https://www.lopingsos.com"
os.environ["OS_REPOSITORY"] = "https://github.com/lopingsos/LopingsOS"

os.environ["OS_DEFAULT_APP"] = "filemanager"
os.environ["OS_STARTUP_APPS"] = "filemanager,settings,terminal"
os.environ["OS_PINNED_APPS"] = "filemanager,terminal,browser,settings,calculator"

os.environ["OS_FILE_ASSOCIATIONS"] = "txt:editor,py:editor,json:editor,log:viewer"
os.environ["OS_MIME_TYPES"] = "text/plain:txt,application/json:json,application/python:py"

os.environ["OS_SHORTCUTS_ENABLED"] = "true"
os.environ["OS_SHORTCUT_NEW_FILE"] = "Ctrl+N"
os.environ["OS_SHORTCUT_OPEN_FILE"] = "Ctrl+O"
os.environ["OS_SHORTCUT_SAVE_FILE"] = "Ctrl+S"
os.environ["OS_SHORTCUT_CLOSE_WINDOW"] = "Ctrl+W"
os.environ["OS_SHORTCUT_QUIT"] = "Ctrl+Q"
os.environ["OS_SHORTCUT_FULLSCREEN"] = "F11"
os.environ["OS_SHORTCUT_SETTINGS"] = "Ctrl+,"

os.environ["OS_NOTIFICATION_ENABLED"] = "true"
os.environ["OS_NOTIFICATION_SOUND"] = "true"
os.environ["OS_NOTIFICATION_DURATION"] = "3000"

os.environ["OS_SEARCH_ENABLED"] = "true"
os.environ["OS_SEARCH_INDEX_ENABLED"] = "true"
os.environ["OS_SEARCH_HISTORY_ENABLED"] = "true"
os.environ["OS_SEARCH_MAX_RESULTS"] = "50"

os.environ["OS_TASKBAR_ENABLED"] = "true"
os.environ["OS_TASKBAR_POSITION"] = "bottom"
os.environ["OS_TASKBAR_AUTO_HIDE"] = "false"

os.environ["OS_DESKTOP_ICONS_ENABLED"] = "true"
os.environ["OS_DESKTOP_WALLPAPER"] = ""
os.environ["OS_DESKTOP_GRID_SIZE"] = "100"

os.environ["OS_TRAY_ENABLED"] = "true"
os.environ["OS_TRAY_MINIMIZE_TO_TRAY"] = "true"

os.environ["OS_CONTEXT_MENU_ENABLED"] = "true"
os.environ["OS_CONTEXT_MENU_ITEMS"] = "open,rename,delete,properties,copy,cut,paste"

os.environ["OS_STATUS_BAR_ENABLED"] = "true"
os.environ["OS_STATUS_BAR_SHOW_TIME"] = "true"
os.environ["OS_STATUS_BAR_SHOW_CPU"] = "true"
os.environ["OS_STATUS_BAR_SHOW_MEMORY"] = "true"
