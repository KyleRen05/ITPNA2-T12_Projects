import requests
import time

# -- Question 2.1 a -- Safety Threshholds --
MIN_PRESSURE = 11.0 # standard minimum for commercial aircrafts
MAX_PRESSURE = 13.0 # standard maximum for commercial aircrafts
REQUIRED_AUTOPILOT = "Engaged" # standard procedure for commercial aircrafts
MAX_WIFI_MB = 900 # keeping below 900MB can help flag potential anomolies and prevent malicious attacks

# Endpoint from server created in question 1
URL = 'http://localhost:8000/events'


print("-- AIRLINE-SAFETY-MONITORING-SYSTEM --")

# -- Question 2.1 e -- Run continuously --
while True:
    try:
        # -- 2.1 b -- Data Acquisition --
        response = requests.get(URL, timeout=3)
        response.raise_for_status()

        flight_data_list = response.json()
        if not flight_data_list:
            print(f"[SYSTEM] No flight data available yet.")
            time.sleep(5)
            continue

        latest_reading = flight_data_list[-1]

        # extract variables
        pressure = latest_reading.get('cabin_pressure_psi', 0.0)
        autopilot = latest_reading.get('autopilot_status', "Unknown")
        wifi = latest_reading.get('wifi_usage_mb', 0)
        timestamp = latest_reading.get('event_time', "Unknown Time")

        # 2.1 c -- Alert Logic --
        alert_triggered = False

        # 2.1 d -- Alert Triggers --
        if not (MIN_PRESSURE <= pressure <= MAX_PRESSURE):
            print(f"[CRITICAL ALERT] CABIN PRESSURE OUT OF RANGE")
            print(f"\t-> Parameter: Cabin Pressure")
            print(f"\t-> Current Value: {pressure} PSI")
            print(f"\t-> Expected Range: {MIN_PRESSURE} - {MAX_PRESSURE} PSI")
            print(f"\t-> Time: {timestamp}\n")
            alert_triggered = True

        if autopilot != REQUIRED_AUTOPILOT:
            print(f"[WARNING ALERT] Autopilot Disengaged!")
            print(f"   -> Parameter: Autopilot Status")
            print(f"   -> Current Value: {autopilot}")
            print(f"   -> Expected Safe State: {REQUIRED_AUTOPILOT}")
            print(f"   -> Time: {timestamp}\n")
            alert_triggered = True
            
        if wifi > MAX_WIFI_MB:
            print(f"[NETWORK ALERT] Abnormal Wi-Fi Usage Detected!")
            print(f"   -> Parameter: Wi-Fi Usage")
            print(f"   -> Current Value: {wifi} MB")
            print(f"   -> Expected Safe Limit: Under {MAX_WIFI_MB} MB")
            print(f"   -> Time: {timestamp}\n")
            alert_triggered = True 

        if not alert_triggered:
            print(f"[{timestamp}] System Nominal | Pressure: {pressure} PSI | AP: {autopilot} | Wi-Fi: {wifi} MB ")
        
    except requests.exceptions.ConnectionError:
        print("[CONNECTION ERROR] Cannot reach the flight server. Is server.py running? Retrying in 5s...")
    except requests.exceptions.RequestException as e:
        print(f"[HTTP ERROR] Failed to fetch data: {e}")
    except Exception as e:
        print(f"[SYSTEM ERROR] An unexpected error occurred: {e}") 

    time.sleep(5)