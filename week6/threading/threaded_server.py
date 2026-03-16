"""
Threaded Server
---------------
Creates a new thread for each client connection.
Multiple clients can be handled simultaneously.
Good for: I/O-bound operations, moderate concurrency.
"""

import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 9001

def handle_request(client_socket, client_address, client_id):
    """
    Handle a single client request in its own thread.
    Each client runs independently.
    """
    thread_name = threading.current_thread().name
    print(f"\n[Client #{client_id}] Connected from {client_address[0]}:{client_address[1]}")
    print(f"  Thread: {thread_name}")
    
    try:
        # Receive data
        data = client_socket.recv(1024)
        message = data.decode('utf-8')
        print(f"  [Client #{client_id}] Received: {message}")
        
        # Simulate slow processing
        print(f"  [Client #{client_id}] Processing (2 seconds)...")
        time.sleep(2)
        
        # Send response
        response = f"Processed: {message}"
        client_socket.sendall(response.encode('utf-8'))
        print(f"  [Client #{client_id}] Response sent")
        
    except Exception as e:
        print(f"  [Client #{client_id}] Error: {e}")
    
    finally:
        client_socket.close()
        print(f"  [Client #{client_id}] Connection closed")

def main():
    """
    Threaded server main loop.
    Creates a new thread for each client.
    """
    print("=" * 60)
    print("Threaded Server")
    print("=" * 60)
    print(f"Listening on {HOST}:{PORT}")
    print("Each client gets its own thread")
    print("Press Ctrl+C to stop\n")
    
    # Create socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    
    client_count = 0
    active_threads = []
    
    try:
        while True:
            # Accept connection
            client_socket, client_address = server.accept()
            client_count += 1
            
            # Create a new thread for this client
            client_thread = threading.Thread(
                target=handle_request,
                args=(client_socket, client_address, client_count),
                name=f"ClientThread-{client_count}"
            )
            
            # Daemon threads exit when main program exits
            client_thread.daemon = True
            
            # Start the thread
            client_thread.start()
            active_threads.append(client_thread)
            
            print(f"\n[Main] Client #{client_count} accepted, started thread")
            print(f"[Main] Active threads: {threading.active_count()}")
    
    except KeyboardInterrupt:
        print("\n\nServer stopping...")
        print(f"Waiting for {len(active_threads)} active threads to complete...")
    
    finally:
        server.close()
        print("Server closed")

if __name__ == '__main__':
    main()