"""
Test Client for Server Comparison
----------------------------------
Sends requests to servers to demonstrate the difference between
single-threaded and threaded servers.
"""

import socket
import threading
import time

def send_request(server_host, server_port, client_id, delay=0):
    """
    Send a request to the server.
    
    Args:
        server_host: Server IP address
        server_port: Server port
        client_id: Identifier for this client
        delay: How long to wait before connecting (seconds)
    """
    # Wait before connecting (to stagger connections)
    if delay > 0:
        time.sleep(delay)
    
    try:
        # Connect to server
        start_time = time.time()
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_host, server_port))
        
        print(f"[Client {client_id}] Connected at {time.time() - start_time:.2f}s")
        
        # Send message
        message = f"Hello from client {client_id}"
        client.sendall(message.encode('utf-8'))
        
        # Receive response
        response = client.recv(1024)
        elapsed = time.time() - start_time
        
        print(f"[Client {client_id}] Response received at {elapsed:.2f}s: {response.decode('utf-8')}")
        
        # Close
        client.close()
        
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")

def test_server(server_host, server_port, num_clients=3):
    """
    Test server by sending multiple simultaneous requests.
    
    Args:
        server_host: Server IP address
        server_port: Server port
        num_clients: Number of simultaneous clients to create
    """
    print("=" * 60)
    print(f"Testing server at {server_host}:{server_port}")
    print(f"Sending {num_clients} simultaneous requests...")
    print("=" * 60)
    
    threads = []
    
    # Create multiple client threads
    for i in range(1, num_clients + 1):
        # Each client connects with slight delay (0.1 seconds apart)
        thread = threading.Thread(
            target=send_request,
            args=(server_host, server_port, i, i * 0.1)
        )
        threads.append(thread)
    
    # Start all threads
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    total_time = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"All {num_clients} clients completed in {total_time:.2f} seconds")
    print(f"{'=' * 60}\n")

if __name__ == '__main__':
    print("\nServer Comparison Test")
    print("=" * 60)
    print("This script tests both single-threaded and threaded servers")
    print("\nTest 1: Single-threaded server (port 9000)")
    print("  Expected: ~6 seconds (3 clients x 2 seconds each)")
    print("\nTest 2: Threaded server (port 9001)")
    print("  Expected: ~2 seconds (all clients handled simultaneously)")
    print("=" * 60)
    
    input("\nMake sure single_threaded_server.py is running, then press Enter...")
    test_server('127.0.0.1', 9000, num_clients=3)
    
    input("\nMake sure threaded_server.py is running, then press Enter...")
    test_server('127.0.0.1', 9001, num_clients=3)