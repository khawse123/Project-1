import time
import threading
import pystray
from PIL import Image, ImageDraw
import pyautogui
import pythoncom
from pycaw.pycaw import AudioUtilities
from win10toast import ToastNotifier

# --- CONFIGURATION ---
enabled = True
toaster = ToastNotifier()

def notify(msg):
    """Background notification."""
    try:
        toaster.show_toast("Silent Ear", msg, duration=2, threaded=True)
    except:
        pass

def pause_media():
    """Universal Pause."""
    pyautogui.press('playpause')

def monitor_audio_hardware():
    global enabled
    pythoncom.CoInitialize()
    
    # We are specifically watching for a switch to these internal speakers
    internal_name = "realtek"
    
    # State tracking
    was_on_safe_device = False

    while True:
        if enabled:
            try:
                # Get the currently active output device
                default_device = AudioUtilities.GetSpeakers()
                device_name = default_device.GetFriendlyName().lower()
                
                # Check if we are currently using the internal Realtek speakers
                is_internal = internal_name in device_name

                # LOGIC: If we were previously on a 'safe' device (BT/Aux/Type-C) 
                # and the system just switched to Realtek...
                if was_on_safe_device and is_internal:
                    pause_media()
                    notify(f"Earphones Disconnected - Paused!")
                    was_on_safe_device = False 
                
                # If the current device is NOT Realtek, it's a safe device
                elif not is_internal:
                    was_on_safe_device = True
                    
            except Exception:
                # If everything is unplugged and no device is found
                if was_on_safe_device:
                    pause_media()
                    was_on_safe_device = False
        
        # Check every 300ms for a near-instant response
        time.sleep(0.3)

# --- SYSTEM TRAY ICON ---
def create_image(is_enabled):
    """Generates the icon: Green for Active, Red for Paused."""
    image = Image.new('RGB', (64, 64), (30, 30, 30))
    dc = ImageDraw.Draw(image)
    color = (0, 255, 128) if is_enabled else (255, 80, 80)
    # Draw a simple 'Speaker' or 'Circle' icon
    dc.ellipse((10, 10, 54, 54), outline=color, width=6)
    dc.ellipse((25, 25, 39, 39), fill=color)
    return image

def on_clicked(icon, item):
    global enabled
    if str(item) == "Enable":
        enabled = True
        notify("Protection Enabled")
    elif str(item) == "Disable":
        enabled = False
        notify("Protection Disabled")
    elif str(item) == "Exit":
        icon.stop()
    icon.icon = create_image(enabled)

menu = pystray.Menu(
    pystray.MenuItem("Enable", on_clicked, checked=lambda item: enabled),
    pystray.MenuItem("Disable", on_clicked, checked=lambda item: not enabled),
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Exit", on_clicked)
)

icon = pystray.Icon("SilentEar", create_image(enabled), "Silent Ear", menu)

# Start hardware monitoring in a background thread
threading.Thread(target=monitor_audio_hardware, daemon=True).start()

# Run the Tray Icon
icon.run()