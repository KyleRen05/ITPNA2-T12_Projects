import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

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

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"404 Not Found: The requested endpoint does not exist.")

if __name__ == '__main__':
    server_address = ('localhost', 8000)

    httpd = HTTPServer(server_address, FlightHandler)

    print(f"Server is waiting to start on port {server_address[1]} ...")
    print(f"Waiting for clients to request data from {server_address}")

    httpd.serve_forever()