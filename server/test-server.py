import platform
import subprocess

import requests

BASE_URL = "http://raspberrypi.local:5000"

# Ping the Raspberry Pi three times
ping_count_flag = "-n" if platform.system() == "Windows" else "-c"
subprocess.run(
    ["ping", ping_count_flag, "3", "raspberrypi.local"],
    check=False,
)

# Read the current LED state
response = requests.get(f"{BASE_URL}/led", timeout=5)
response.raise_for_status()
print("LED state:", response.json())

# Turn the LED on, then off
for state in (1, 0):
    response = requests.post(
        f"{BASE_URL}/led",
        json={"state": state},
        timeout=5,
    )
    response.raise_for_status()
    print("LED response:", response.json())

# Read the BME280 sensor
response = requests.get(f"{BASE_URL}/bme280", timeout=5)
response.raise_for_status()
print("BME280:", response.json())
