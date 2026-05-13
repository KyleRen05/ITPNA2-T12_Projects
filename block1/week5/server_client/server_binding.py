"""
Server Binding with getaddrinfo()
----------------------------------
Demonstrates how to properly bind a server to a port
using getaddrinfo() which works with both IPv4 and IPv6.
"""

import socket

def create_server_socket(port, host=None):
    """
    Create and bind a server socket using getaddrinfo().
    
    Parameters:
        port: Port number to bind to
        host: IP address or hostname (None = all interfaces)
    """
    print("=" * 70)
    print(f"Creating server socket on port {port}")
    print("=" * 70)
    
    try:
        # Get address info for server binding
        # Use AI_PASSIVE flag - returns address suitable for bind()
        # If host is None, returns wildcard address (0.0.0.0 for IPv4)
        results = socket.getaddrinfo(
            host,                    # None = all interfaces
            port,                    # Port to bind
            socket.AF_INET,          # IPv4
            socket.SOCK_STREAM,      # TCP
            socket.IPPROTO_TCP,      # TCP protocol
            socket.AI_PASSIVE        # For server binding
        )
        
        # Get first result
        family, socktype, proto, canonname, sockaddr = results[0]
        
        print(f"\nSocket Configuration:")
        print(f"  Family: {'IPv4' if family == socket.AF_INET else 'IPv6'}")
        print(f"  Type: {'TCP' if socktype == socket.SOCK_STREAM else 'UDP'}")
        print(f"  Bind Address: {sockaddr[0]}")
        print(f"  Bind Port: {sockaddr[1]}")
        
        # Create socket
        server_socket = socket.socket(family, socktype, proto)
        
        # Set socket option to reuse address (helpful during development)
        # Allows restarting server without "Address already in use" error
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind to the address
        server_socket.bind(sockaddr)
        
        # Listen for connections (backlog of 5)
        server_socket.listen(5)
        
        print(f"\nServer successfully bound and listening on {sockaddr[0]}:{sockaddr[1]}")
        
        return server_socket
        
    except PermissionError:
        print(f"\nPermission denied - port {port} may require admin privileges")
        print("Try using a port above 1024")
        return None
        
    except OSError as e:
        print(f"\nOS Error: {e}")
        print("Port may already be in use")
        return None
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return None


def run_simple_server(port):
    """
    Run a simple echo server that accepts one connection.
    """
    # Create and bind server socket
    server = create_server_socket(port)
    
    if server is None:
        return
    
    print("\nWaiting for client connection...")
    print("(Run client_connection.py in another terminal)")
    
    try:
        # Accept a connection
        client_socket, client_address = server.accept()
        
        print(f"\nClient connected from {client_address[0]}:{client_address[1]}")
        
        # Receive data
        data = client_socket.recv(1024)
        message = data.decode('utf-8')
        
        print(f"Received: {message}")
        
        # Send response
        response = f"Echo: {message}"
        client_socket.sendall(response.encode('utf-8'))
        
        print(f"Sent: {response}")
        
        # Close client connection
        client_socket.close()
        print("\nClient connection closed")
        
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        
    finally:
        # Always close server socket
        server.close()
        print("Server socket closed")


# Main execution
if __name__ == "__main__":
    # Example: Create server on port 5000
    run_simple_server(5000)