import time
import pythoncom
from pycaw.pycaw import AudioUtilities

def log_device_states():
    # Sign the Windows guestbook
    pythoncom.CoInitialize()
    
    print("--- Sniffer Active ---")
    print("Unplug/Disconnect your devices now. Check 'audio_log.txt' when done.")
    
    with open("audio_log.txt", "w", encoding="utf-8") as f:
        f.write(f"Audio Handshake Log - Started at {time.ctime()}\n")
        f.write("-" * 50 + "\n")

        last_snapshot = ""

        try:
            while True:
                # Capture all devices and their current states
                devices = AudioUtilities.GetAllDevices()
                current_snapshot = ""
                
                for dev in devices:
                    # State 1 = Active, State 2 = Disabled, State 8 = Unplugged
                    try:
                        name = dev.GetFriendlyName()
                        state = dev.State
                        current_snapshot += f"Device: {name} | State: {state}\n"
                    except:
                        continue

                # Only log if something actually changed
                if current_snapshot != last_snapshot:
                    timestamp = time.strftime("%H:%M:%S")
                    log_entry = f"\n[CHANGE DETECTED AT {timestamp}]\n{current_snapshot}"
                    
                    print(log_entry) # Show in terminal
                    f.write(log_entry) # Save to file
                    f.flush() # Force write to disk immediately
                    
                    last_snapshot = current_snapshot
                
                time.sleep(1) # Check every second
        except KeyboardInterrupt:
            print("\nSniffing stopped. Please open 'audio_log.txt'.")

if __name__ == "__main__":
    log_device_states()