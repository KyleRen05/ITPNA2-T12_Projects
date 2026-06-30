import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import sqlite3
import smtplib
from email.message import EmailMessage
from datetime import datetime

PORT = 8000

# --- QUESTION 1.4 ---

def init_db():
    conn = sqlite3.connect('aviation.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS in_flight_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            autopilot_status TEXT,
            cabin_pressure_psi REAL,
            wifi_usage_mb INTEGER
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM in_flight_events")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO in_flight_events (autopilot_status, cabin_pressure_psi, wifi_usage_mb)
            VALUES 
                ('Engaged', 11.80, 450),
                ('Engaged', 11.82, 512),
                ('Disengaged', 11.75, 530)
        ''')
        conn.commit()
        print(f"[SYSTEM] New Aviation Database Created with Dummy Data")
    
    else:
        print("[SYSTEM] Existing aviation.db found. Skipping build phase.")
    conn.close()



init_db()
print("SQLite Database verified/built successfully.")


# --- QUESTION 3 - EMAIL ALERT IMPLEMENTATION ---
def email_alerts(parameter, value, description):
    ''' SENDS A REAL SMTP EMAIL OVER LOCAL NETWORK FOR TESTING '''
    current_time = datetime.now().strftime("%H:%M:%S")

    msg = EmailMessage()
    msg['Subject'] = f"CRITICAL ALERT: {description}"
    msg['From'] = "system@aeroarilines.com"
    msg['To'] = "monitoring@aeroairlines.com"

    body = f"""AERO AIRLINES - AUTOMATED SAFETY ALERT
==================================================
ALERT: {description}
Parameter: {parameter}
Recorded Value: {value}
Time of Event: {current_time}
==================================================
Action: Immediate assessment required.
""" 

    msg.set_content(body)

    try:
        with smtplib.SMTP('localhost', 1025) as server:
            server.send_message(msg)
        print(f"[SYSTEM] Alert successfully transmitted for {parameter}.")
    except ConnectionRefusedError:
        print(f"[ERROR] Local SMTP server is not running. Alert Not Sent.")


class FlightHandler(BaseHTTPRequestHandler):

    # q1.1
    def do_GET(self):
        '''urlparse isolates only the /flight endpint so that there can be no lateral file discovery using injections'''
        parsed_path = urlparse(self.path).path

        if parsed_path == '/flight': #if the path is correct
            try:
                ''' open the json file in read mode '''
                with open('flight_data.json', 'r') as file:
                    flight_data = json.load(file)
                
                ''' sending network response '''
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
            
                ''' convert python dictionary back into json '''
                response_data = json.dumps(flight_data)
                ''' pipeline back to client '''
                self.wfile.write(response_data.encode('utf-8'))
            
            except FileNotFoundError:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"[SERVER ERROR] flight_data.json file not found.")

        # -- QUESTION 1.4 -- DB CONNECTION TO API
        elif parsed_path == '/events':
            try:
                conn = sqlite3.connect('aviation.db')

                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM in_flight_events")
                
                records = [dict(row) for row in cursor.fetchall()]

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                self.wfile.write(json.dumps(records, indent=4).encode('utf-8'))

                cursor.close()
                conn.close()

            except sqlite3.Error as err:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_msg = {"status": "error", "message": f"Database connection failed: {err}"}
                self.wfile.write(json.dumps(error_msg).encode('utf-8'))


        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"[ERROR 404] The Request to the Endpoint does not exist")
    
    # q1.3
    def do_POST(self):
        parsed_path = urlparse(self.path).path

        if parsed_path == "/flight":
            try:
                content_length = int(self.headers['Content-Length'])

                post_data = self.rfile.read(content_length)

                update_data = json.loads(post_data.decode('utf-8'))

                with open('flight_data.json', 'w') as file:
                    json.dump(update_data, file, indent=4)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                confirmation = {"status": "success", "message": "Aircraft data successfully updated."}
                self.wfile.write(json.dumps(confirmation).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_msg = {"status": "error", "message": f"Failed to update data: {str(e)}"}
                self.wfile.write(json.dumps(error_msg).encode('utf-8'))

        # -- Question 1.6 -- /events POST METHOD
        elif parsed_path == '/events':
            try:
                content_length = int(self.headers['Content-Length'])        

                post_data = self.rfile.read(content_length)

                data = json.loads(post_data)

                values = (
                    data.get('autopilot_status', 'Unknown'),
                    data.get('cabin_pressure_psi', 0.0),
                    data.get('wifi_usage_mb', 0.0)
                )

                # Question 3 - SENDING EMAIL ALERT
                # unpacking tuple variables
                autopilot = values[0]
                pressure = values[1]
                wifi = values[2]

                # Evaluate variables and thresholds
                if pressure < 11.0 or pressure > 13.0:
                    email_alerts("Cabin Pressure", f"{pressure} PSI", "Cabin Pressure Out of Range")
            
                if autopilot != "Engaged":
                    email_alerts("Autopilot Status", autopilot, "Autopilot disengaged")
                
                if wifi > 900:
                    email_alerts("WiFi Usage", f"{wifi} MB", "Abnormal Network Bandwidth")

                conn = sqlite3.connect('aviation.db')
                cursor = conn.cursor()

                sql = """
                    INSERT INTO in_flight_events
                    (autopilot_status, cabin_pressure_psi, wifi_usage_mb)
                    VALUES (?, ?, ?)
                """

                values = (
                    data.get('autopilot_status', 'Unknown'),
                    data.get('cabin_pressure_psi', 0.0),
                    data.get('wifi_usage_mb', 0.0)
                )


                cursor.execute(sql, values)

                conn.commit()

                cursor.close()
                conn.close()

                self.send_response(201) 
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Data saved"}).encode('utf-8'))

            except Exception as e:
                print(f"\n[CRASH REPORT] Server Failed: {e}")
                
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))



        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"404 Not Found: The requested endpoint does not exist.")

if __name__ == '__main__':
    server_address = ('localhost', PORT)

    httpd = HTTPServer(server_address, FlightHandler)

    print(f"Server is waiting to start on port {server_address[1]} ...")
    print(f"Waiting for clients to request data from {server_address}")

    httpd.serve_forever()