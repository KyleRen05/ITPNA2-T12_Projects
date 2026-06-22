import json
from urllib import request, error

def update_flight_data():
    url = 'http://localhost:8000/flight'

    update_info = {
        "aircraft_status": "Boarding",
        "passenger_boarding_number": 130,
        "fueling": "Complete",
        "door_state": "Open",
        "push_back_time": "13:45"
    }

    print(f"Preparing to send updated data to {url}")

    try:
        json_data = json.dumps(update_info)
        byte_data = json_data.encode('utf-8')

        req = request.Request(
            url=url,
            data=byte_data,
            headers={'Content-type': 'application/json'},
            method='POST'
        )

        with request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            server_reply = json.loads(response_body)

            print("--- Server Response ---")
            print(f"Status Code: {response.getcode()}")
            print(f"Message: {server_reply.get('message', 'Update successful')}")

    except error.URLError as e:
        print("Connection Error: Could not reach the server.")
        print(f"Reason: {e.reason}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 


if __name__ == '__main__':
    update_flight_data()