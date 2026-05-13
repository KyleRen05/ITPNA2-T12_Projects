"""
TLS/SSL Server Example
----------------------
A simple HTTPS-like server that accepts encrypted connections.
Demonstrates basic TLS server implementation.

Requirements:
- server-cert.pem (certificate file)
- server-key.pem (private key file)
Generate these using the generate_certificates.sh script
"""

import socket
import ssl

# Configuration
HOST = '127.0.0.1'
PORT = 8443  # Standard HTTPS port is 443, we use 8443 for testing
CERT_FILE = 'server-cert.pem'
KEY_FILE = 'server-key.pem'

def create_tls_server():
    """
    Create and configure a TLS server socket.
    Returns the configured TLS socket.
    """
    # Step 1: Create SSL context for server
    # Purpose.CLIENT_AUTH means this context is for server-side TLS
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Step 2: Load the server certificate and private key
    # These files prove the server's identity to clients
    try:
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    except FileNotFoundError:
        print("ERROR: Certificate files not found!")
        print("Please run generate_certificates.sh first")
        exit(1)
    
    # Step 3: Configure TLS settings
    # Set minimum TLS version to 1.2 (secure)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    # Step 4: Create regular TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reusing the address (useful during development)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Step 5: Bind to address and port
    server_socket.bind((HOST, PORT))
    
    # Step 6: Listen for connections (queue up to 5 connections)
    server_socket.listen(5)
    
    # Step 7: Wrap socket with TLS
    # server_side=True indicates this is a server socket
    tls_socket = context.wrap_socket(server_socket, server_side=True)
    
    return tls_socket

def handle_client(client_socket, client_address):
    """
    Handle a client connection.
    Receives data, sends response, closes connection.
    """
    print(f"\nConnection from {client_address[0]}:{client_address[1]}")
    
    # Display TLS connection information
    cipher = client_socket.cipher()
    if cipher:
        print(f"  Cipher: {cipher[0]}")
        print(f"  TLS Version: {cipher[1]}")
    
    try:
        # Receive data from client (max 4096 bytes)
        data = client_socket.recv(4096)
        
        if data:
            message = data.decode('utf-8')
            print(f"  Received: {message}")
            
            # Prepare response
            response = f"Server received: {message}"
            
            # Send response back to client
            client_socket.sendall(response.encode('utf-8'))
            print(f"  Sent response")
        
    except Exception as e:
        print(f"  Error handling client: {e}")
    
    finally:
        # Always close the client connection
        client_socket.close()
        print(f"  Connection closed")

def main():
    """
    Main server loop.
    Accepts connections and handles them one at a time.
    """
    print("=" * 60)
    print("TLS/SSL Server")
    print("=" * 60)
    print(f"Starting TLS server on {HOST}:{PORT}")
    print(f"Certificate: {CERT_FILE}")
    print(f"Private Key: {KEY_FILE}")
    print("\nWaiting for connections...")
    print("Press Ctrl+C to stop the server\n")
    
    # Create TLS server socket
    server = create_tls_server()
    
    try:
        # Main server loop
        while True:
            # Accept incoming connection
            # This returns a TLS-wrapped socket
            client_socket, client_address = server.accept()
            
            # Handle the client
            handle_client(client_socket, client_address)
    
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    
    finally:
        server.close()
        print("Server socket closed")

if __name__ == '__main__':
    main()