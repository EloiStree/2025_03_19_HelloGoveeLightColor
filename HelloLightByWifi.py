import struct
import requests
import os
import socket
import threading


# NOT IF YOU USE ONLINE API THERE IS A RATE LIMIT.

api_key_path ="Keys/api_key.txt"
start_color = "#FF00FF"
API_KEY = ""

if not os.path.exists(os.path.join(os.path.dirname(__file__), "Keys")):
    print("What is your API key?")
    API_KEY = input()
    os.makedirs(os.path.join(os.path.dirname(__file__), "Keys"))
    with open(os.path.join(os.path.dirname(__file__), api_key_path), "w") as file:
        file.write(API_KEY)

API_KEY = open(os.path.join(os.path.dirname(__file__), api_key_path), "r").read()

print(f"Key is : {API_KEY[2:]}...")


def get_device_list():
    """Retrieve the list of Govee devices linked to your account."""
    url = "https://developer-api.govee.com/v1/devices"
    headers = {
        "Govee-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        devices = response.json()["data"]["devices"]
        for i, device in enumerate(devices):
            print(f"{i+1}. Name: {device['deviceName']}, ID: {device['device']}, Model: {device['model']}")
        return devices
    else:
        print("Error fetching device list:", response.text)
        return []

# Get and display devices
device_list = get_device_list()


def change_color(device_in_list, hex_color="#FF0000"):
    """Change Govee light color using HEX code."""
    # Convert HEX to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    url = "https://developer-api.govee.com/v1/devices/control"
    headers = {
        "Govee-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "device": device_in_list["device"],
        "model": device_in_list["model"],
        "cmd": {
            "name": "color",
            "value": {"r": rgb[0], "g": rgb[1], "b": rgb[2]}
        }
    }

    response = requests.put(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"Light color changed to {hex_color}")
    else:
        print("Error:", response.text)

for i, device in enumerate(device_list):
    print(f"{i+1}. Name: {device['deviceName']}, ID: {device['device']}, Model: {device['model']}")
    change_color(device, start_color)


   
dico_int_color = {}
dico_int_color["700"] = "#000000"
dico_int_color["701"] = "#FF0000"
dico_int_color["702"] = "#00FF00"
dico_int_color["703"] = "#0000FF"
dico_int_color["704"] = "#FFA500"
dico_int_color["705"] = "#FFFF00"
dico_int_color["706"] = "#800080"
dico_int_color["707"] = "#FFC0CB"
dico_int_color["708"] = "#FFFFFF"




def udp_listener():
    """Thread to listen for binary UDP packets on port 7000."""
    udp_port = 7000
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", udp_port))
    print(f"Listening for UDP packets on port {udp_port}...")

    while True:
        data, addr = udp_socket.recvfrom(1024)  # Buffer size is 1024 bytes
        l = len(data)
        integer = 0  # Ensure integer is always defined
        
        if l == 4:
            integer, = struct.unpack('<i', data)  # Correct unpacking
        elif l == 8:
            _, integer = struct.unpack('<ii', data)  # Correct unpacking
        elif l == 12:
            integer, _ = struct.unpack('<iq', data)  # Correct unpacking
        elif l == 16:
            _, integer, _ = struct.unpack('<iiq', data)  # Correct unpacking
        
        if isinstance(integer, int):
            print(f"Received {integer} from {addr}")
            
            if str(integer) in dico_int_color:  # Ensure dico_int_color is defined elsewhere
                for device in device_list:  # Ensure device_list is defined elsewhere
                    print(f"Changing color to {dico_int_color[str(integer)]}")
                    change_color(device, dico_int_color[str(integer)])  # Ensure c

# Start the UDP listener in a separate thread
udp_thread = threading.Thread(target=udp_listener, daemon=True)
udp_thread.start()

while True:
    number = input("Enter a number between 700 and 708: ")
    if number.isdigit() and 700 <= int(number) <= 708:
        for device in device_list:
            change_color(device, dico_int_color[number])