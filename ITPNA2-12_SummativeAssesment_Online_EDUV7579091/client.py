import json
import urllib.request
import urllib.error

# QUESTION 1.2

def fetch_flight_data():
    url = 'http://localhost:8000/flight'

    print(f"Attempting to connect to {url} ...\n")

    try:
        ''' attempting to connect to the given url '''
        with urllib.request.urlopen(url) as response:

            ''' decoding the data given from the server '''
            raw_data = response.read().decode('utf-8')

            flight_info = json.loads(raw_data)

            print("--- Pre-Departure Aircraft Information ---")

            for key, value in flight_info.items():
                print(f"{key}: {value}")
            
    except urllib.error.URLError as e:
        print("Connection Error: Could not reach the server.")
        print(f"Reason: {e.reason}")
    
    except json.JSONDecodeError:
        print("Data Error: Connected to the server, but the data received was not valid JSON.")

    except Exception as e:
        print(f"An unexcpected error as occured: {e}")


if __name__ == '__main__':
    fetch_flight_data()