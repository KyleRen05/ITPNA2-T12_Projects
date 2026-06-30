import requests

# -- QUESTION 1.5 -- CLIENT SIDE FOR /events API

def fetch_flight_events():
    url = 'http://localhost:8000/events'

    print(f"Initiating connection to flight server {url} ...\n")

    try:
        response = requests.get(url, timeout=5)

        response.raise_for_status()

        events_data = response.json()


        print("--- IN-FLIGHT EVENTS LOG ---")
        for event in events_data:
            print(f"Event ID: {event.get('id')}")
            print(f"  Time:             {event.get('event_time')}")
            print(f"  Autopilot Status: {event.get('autopilot_status')}")
            print(f"  Cabin Pressure:   {event.get('cabin_pressure_psi')} PSI")
            print(f"  WiFi Usage:       {event.get('wifi_usage_mb')} MB")
            print("-" * 30)


    except requests.exceptions.ConnectionError:
        print("CRITICAL ERROR: Connection refused.")
        print(" -> Is your server.py currently running in another terminal?")
    except requests.exceptions.HTTPError as http_err:
        print(f"SERVER ERROR: Received an invalid response: {http_err}")
    except requests.exceptions.Timeout:
        print("TIMEOUT ERROR: The server took too long to respond.")
    except Exception as e:
        print(f"SYSTEM ERROR: An unexpected error occurred: {e}") 


if __name__ == '__main__':
    fetch_flight_events()