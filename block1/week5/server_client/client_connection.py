"""
Client Connection with getaddrinfo()
------------------------------------
Demonstrates how to properly connect to a server
using getaddrinfo() with retry logic for multiple addresses.
"""

import socket

def connect_to_server(hostname, port):
    """
    Connect to a server using getaddrinfo().
    Tries all available addresses until one succeeds.
    """
    print("=" * 70)
    print(f"Connecting to {hostname}:{port}")
    print("=" * 70)
    
    try:
        # Get address information for connection
        results = socket.getaddrinfo(
            hostname,
            port,
            socket.AF_UNSPEC,      # Accept both IPv4 and IPv6
            socket.SOCK_STREAM     # TCP
        )
        
        print(f"\nFound {len(results)} address(es) to try\n")
        
        # Try each address until one works
        for i, result in enumerate(results, 1):
            family, socktype, proto, canonname, sockaddr = result
            
            family_name = "IPv4" if family == socket.AF_INET else "IPv6"
            ip_address = sockaddr[0]
            
            print(f"Attempt {i}: Trying {family_name} address {ip_address}...")
            
            try:
                # Create socket
                client_socket = socket.socket(family, socktype, proto)
                
                # Set timeout to avoid hanging
                client_socket.settimeout(5)
                
                # Try to connect
                client_socket.connect(sockaddr)
                
                print(f"Successfully connected to {ip_address}:{port}\n")
                
                return client_socket
                
            except socket.timeout:
                print(f"  Connection timed out")
                client_socket.close()
                continue
                
            except ConnectionRefusedError:
                print(f"  Connection refused (server not running?)")
                client_socket.close()
                continue
                
            except OSError as e:
                print(f"  Connection failed: {e}")
                client_socket.close()
                continue
        
        # If we get here, all attempts failed
        print("\nAll connection attempts failed")
        return None
        
    except socket.gaierror as e:
        print(f"\nDNS resolution failed: {e}")
        return None


def communicate_with_server(hostname, port, message):
    """
    Connect to server, send message, receive response.
    """
    # Connect to server
    client = connect_to_server(hostname, port)
    
    if client is None:
        print("\nCould not connect to server")
        return
    
    try:
        # Send message
        print(f"Sending: {message}")
        client.sendall(message.encode('utf-8'))
        
        # Receive response
        response = client.recv(1024)
        message_received = response.decode('utf-8')
        
        print(f"Received: {message_received}\n")
        
    except socket.timeout:
        print("\nTimeout while communicating with server")
        
    except Exception as e:
        print(f"\nError during communication: {e}")
        
    finally:
        # Always close socket
        client.close()
        print("Connection closed")


# Main execution
if __name__ == "__main__":
    # Example: Connect to local server
    communicate_with_server("localhost", 5000, "Hello, Server!")
    
    # You can also try connecting to a real web server
    print("\n" + "=" * 70)
    print("Connecting to real web server (example.com):")
    print("=" * 70)
    
    client = connect_to_server("example.com", 80)
    if client:
        print("Connection successful - closing")
        client.close()