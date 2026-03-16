"""
TLS/SSL Client Example
----------------------
Connects to TLS server and sends encrypted messages.
Demonstrates certificate validation and secure communication.
"""

import socket
import ssl

# Configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8443

def create_tls_client():
    """
    Create a TLS client and connect to server.
    Returns the TLS-wrapped socket.
    """
    # Step 1: Create SSL context for client
    # This creates a context with secure defaults
    context = ssl.create_default_context()
    
    # Step 2: For self-signed certificates (TESTING ONLY!)
    # In production, you would NOT do this - it defeats the purpose of TLS!
    # This tells the client to skip certificate verification
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    # WARNING: The above lines make the connection insecure
    # Remove them when using real certificates from a trusted CA
    
    # Step 3: Create regular TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Step 4: Wrap socket with TLS and connect
    # server_hostname is important for proper certificate validation
    tls_socket = context.wrap_socket(client_socket, 
                                     server_hostname=SERVER_HOST)
    
    # Step 5: Connect to server
    print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}...")
    tls_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected successfully!")
    
    return tls_socket

def main():
    """
    Main client logic.
    Connect to server, send message, receive response.
    """
    print("=" * 60)
    print("TLS/SSL Client")
    print("=" * 60)
    
    try:
        # Create TLS connection
        tls_socket = create_tls_client()
        
        # Display connection information
        cipher = tls_socket.cipher()
        if cipher:
            print(f"\nTLS Connection established:")
            print(f"  Cipher: {cipher[0]}")
            print(f"  Protocol: {cipher[1]}")
            print(f"  Key bits: {cipher[2]}")
        
        # Send message to server
        message = "Hello from secure client!"
        print(f"\nSending: {message}")
        tls_socket.sendall(message.encode('utf-8'))
        
        # Receive response
        response = tls_socket.recv(4096)
        print(f"Received: {response.decode('utf-8')}")
        
        # Close connection
        tls_socket.close()
        print("\nConnection closed successfully")
        
    except ConnectionRefusedError:
        print("\nERROR: Could not connect to server")
        print("Make sure the TLS server is running")
    
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == '__main__':
    main()