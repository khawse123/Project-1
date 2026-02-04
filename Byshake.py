import asyncio
from bleak import BleakScanner

async def detect_bluetooth_devices():
    print("--- Scanning for Bluetooth Devices (5 seconds) ---")
    
    # This captures both nearby and currently connected/paired devices
    devices = await BleakScanner.discover()
    
    if not devices:
        print("No Bluetooth devices found. Check if your Bluetooth is turned ON.")
    else:
        print(f"Found {len(devices)} device(s):")
        print("-" * 40)
        for d in devices:
            # Name might be None for some devices, so we provide a fallback
            name = d.name if d.name else "Unknown Device"
            print(f"Name: {name}")
            print(f"Address: {d.address}")
            print(f"Signal Strength (RSSI): {d.rssi} dBm")
            print("-" * 40)

# Run the async function
if __name__ == "__main__":
    asyncio.run(detect_bluetooth_devices())