"""
Single-Threaded Server
----------------------
Handles one client at a time. Next client must wait.
Good for: Simple applications, low traffic, learning.
Bad for: Multiple concurrent clients, slow clients.
"""

import socket
import time

HOST = '127.0.0.1'
PORT = 9000

def handle_request(client_socket, client_address):
    """
    Handle a single client request.
    Simulates slow processing (2 seconds).
    """
    print(f"\nHandling client: {client_address[0]}:{client_address[1]}")
    
    # Receive data from client
    data = client_socket.recv(1024)
    message = data.decode('utf-8')
    print(f"  Received: {message}")
    
    # Simulate slow processing (database query, file I/O, etc.)
    print(f"  Processing (this takes 2 seconds)...")
    time.sleep(2)
    
    # Send response
    response = f"Processed: {message}"
    client_socket.sendall(response.encode('utf-8'))
    print(f"  Response sent")
    
    # Close connection
    client_socket.close()

def main():
    """
    Single-threaded server main loop.
    Accepts connections one at a time.
    """
    print("=" * 60)
    print("Single-Threaded Server")
    print("=" * 60)
    print(f"Listening on {HOST}:{PORT}")
    print("Press Ctrl+C to stop\n")
    
    # Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    
    client_count = 0
    
    try:
        while True:
            # Accept connection (blocks until client connects)
            client_socket, client_address = server.accept()
            client_count += 1
            
            print(f"\n[Client #{client_count}] Connected")
            
            # Handle the client
            # NOTE: This blocks! No other clients can connect
            # until this client is completely handled
            handle_request(client_socket, client_address)
            
            print(f"[Client #{client_count}] Finished")
    
    except KeyboardInterrupt:
        print("\n\nServer stopped")
    
    finally:
        server.close()

if __name__ == '__main__':
    main()