import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import sqlite3

PORT = 8000

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

        # Q1.4
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

        elif parsed_path == '/events':
            try:
                content_length = int(self.headers['Content-Length'])        

                post_data = self.rfile.read(content_length)

                data = json.loads(post_data)

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