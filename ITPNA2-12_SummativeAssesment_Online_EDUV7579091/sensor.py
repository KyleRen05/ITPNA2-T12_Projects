import requests
import time
import random

url = 'http://localhost:8000/events'

print("Starting Automated Flight Simulator")
print("Transmitting data every 5 seconds, Ctrl + C to stop...\n")


while True:
    autopilot = random.choice(['Engaged', 'Disengaged'])

    pressure = round(random.uniform(11.0, 12.5), 2)

    wifi = random.randint(100, 1000)


    payload = {
        "autopilot_status": autopilot,
        "cabin_pressure_psi": pressure,
        "wifi_usage_mb": wifi
    }


    try:
        response = requests.post(url, json=payload, timeout=3)

        if response.status_code == 201:
            print(f"[SUCCESS] Transmitted & Saved {payload}")
        else:
            print(f"[ERROR] Server responded with code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[CONNECTION FAILED] Is server.py running? Error: {e}") 
    
    time.sleep(5)