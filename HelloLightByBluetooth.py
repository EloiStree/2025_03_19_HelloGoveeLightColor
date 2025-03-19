import asyncio
from bleak import BleakClient

# Govee H6008 MAC Address
MAC_ADDRESS = "D0:C9:07:E5:EE:B6"
MAC_ADDRESS = "D0:C9:07:D5:B9:E6"

# Govee BLE Characteristics
SERVICE_UUID = "00010203-0405-0607-0809-0a0b0c0d1910"
CHARACTERISTIC_UUID = "00010203-0405-0607-0809-0a0b0c0d2b10"

# Commands (Hexadecimal)
POWER_ON = bytes.fromhex("3301010000000000000000000000000000000033")
POWER_OFF = bytes.fromhex("3301000000000000000000000000000000000032")

def create_color_command(r, g, b):
    """Create a command to change color to (r, g, b)."""
    return bytes.fromhex(f"3305{r:02x}{g:02x}{b:02x}00000000000000000000000000{(0x33 + 5 + r + g + b) % 256:02x}")

def create_brightness_command(brightness):
    """Create a command to set brightness (0-100%)."""
    brightness = max(0, min(100, brightness))  # Clamp value between 0-100
    return bytes.fromhex(f"3304{brightness:02x}000000000000000000000000000000{(0x33 + 4 + brightness) % 256:02x}")

async def send_command(command):
    """Send a command to the Govee light over BLE."""
    async with BleakClient(MAC_ADDRESS) as client:
        if await client.is_connected():
            print("Connected to Govee Light")
            await client.write_gatt_char(CHARACTERISTIC_UUID, command, response=True)
            print("Command sent successfully!")
        else:
            print("Failed to connect.")

async def main():
    """Test the Govee light control."""
    print("Turning light ON...")
    await send_command(POWER_ON)
    await asyncio.sleep(2)

    print("Changing color to Red...")
    await send_command(create_color_command(255, 0, 0))
    await asyncio.sleep(2)

    print("Setting brightness to 50%...")
    await send_command(create_brightness_command(50))
    await asyncio.sleep(2)

    print("Turning light OFF...")
    await send_command(POWER_OFF)

# Run the script
asyncio.run(main())
