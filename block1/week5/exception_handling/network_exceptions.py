"""
Network Exception Handling
---------------------------
Demonstrates proper exception handling for network operations
with retry logic and detailed error reporting.
"""

import socket
import time
import sys


def connect_with_retry(hostname, port, max_retries=3, timeout=5):
    """
    Connect to server with retry logic and proper exception handling.
    """
    print("=" * 70)
    print(f"Connecting to {hostname}:{port} with retry logic")
    print(f"Max retries: {max_retries}, Timeout: {timeout}s")
    print("=" * 70)
    
    for attempt in range(max_retries):
        print(f"\nAttempt {attempt + 1} of {max_retries}...")
        
        try:
            # Get address info
            results = socket.getaddrinfo(hostname, port, socket.AF_INET, 
                                        socket.SOCK_STREAM)
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            # Try to connect
            sockaddr = results[0][4]
            sock.connect(sockaddr)
            
            print(f"SUCCESS: Connected to {sockaddr[0]}:{sockaddr[1]}")
            return sock
            
        except socket.gaierror as e:
            print(f"DNS resolution failed: {e}")
            print("  Possible causes:")
            print("    - Hostname does not exist")
            print("    - DNS server unreachable")
            print("    - No internet connection")
            
            # DNS errors usually don't benefit from retry
            print("\nNo point retrying DNS errors - aborting")
            return None
            
        except socket.timeout:
            print(f"Connection timed out after {timeout} seconds")
            print("  Possible causes:")
            print("    - Server is slow to respond")
            print("    - Network congestion")
            print("    - Firewall blocking connection")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1, 2, 4 seconds
                print(f"  Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            
        except ConnectionRefusedError:
            print("Connection refused by server")
            print("  Possible causes:")
            print("    - Server is not running")
            print("    - Wrong port number")
            print("    - Firewall blocking connection")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"  Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            
        except OSError as e:
            print(f"OS error: {e}")
            print("  This could be:")
            print("    - Network unreachable")
            print("    - Host unreachable")
            print("    - Connection reset")
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"  Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(f"  Error type: {type(e).__name__}")
            return None
    
    print(f"\nFailed to connect after {max_retries} attempts")
    return None


def safe_send_receive(sock, message, buffer_size=1024):
    """
    Safely send and receive data with exception handling.
    """
    print("\n" + "=" * 70)
    print("Sending and Receiving Data")
    print("=" * 70)
    
    try:
        # Send data
        print(f"\nSending: {message}")
        data = message.encode('utf-8')
        sock.sendall(data)
        print("Data sent successfully")
        
        # Receive response
        print(f"\nWaiting for response (max {buffer_size} bytes)...")
        response = sock.recv(buffer_size)
        
        if not response:
            print("Server closed connection (received 0 bytes)")
            return None
        
        # Decode response
        decoded = response.decode('utf-8')
        print(f"Received: {decoded}")
        return decoded
        
    except socket.timeout:
        print("Timeout while waiting for data")
        return None
        
    except ConnectionResetError:
        print("Connection was reset by peer")
        print("  Server may have crashed or been restarted")
        return None
        
    except BrokenPipeError:
        print("Broken pipe - tried to write to closed socket")
        print("  Server closed connection unexpectedly")
        return None
        
    except UnicodeDecodeError as e:
        print(f"Could not decode response as UTF-8: {e}")
        print("  Server may be sending binary data")
        print(f"  Raw bytes: {response}")
        return None
        
    except Exception as e:
        print(f"Error during communication: {e}")
        return None


def demonstrate_all_exceptions():
    """
    Demonstrate handling of various network exceptions.
    """
    print("\n" + "=" * 70)
    print("Network Exception Handling Examples")
    print("=" * 70)
    
    test_cases = [
        ("localhost", 9999, "Non-existent server"),
        ("invalid-hostname-12345.local", 80, "Invalid hostname"),
        ("google.com", 12345, "Valid host, wrong port"),
        ("10.255.255.1", 80, "Unreachable IP"),
    ]
    
    for hostname, port, description in test_cases:
        print(f"\n{'='*70}")
        print(f"Test: {description}")
        print(f"Target: {hostname}:{port}")
        print('='*70)
        
        sock = connect_with_retry(hostname, port, max_retries=2, timeout=2)
        
        if sock:
            sock.close()
            print("Connection successful and closed")


def create_robust_client(hostname, port, message):
    """
    Complete example of a robust client with all error handling.
    """
    print("\n" + "=" * 70)
    print("Robust Client Example")
    print("=" * 70)
    
    sock = None
    
    try:
        # Connect with retry
        sock = connect_with_retry(hostname, port)
        
        if sock is None:
            print("\nCould not establish connection")
            return False
        
        # Send and receive
        response = safe_send_receive(sock, message)
        
        if response is None:
            print("\nCommunication failed")
            return False
        
        print("\nCommunication successful!")
        return True
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return False
        
    finally:
        # Always close socket
        if sock:
            try:
                sock.close()
                print("\nSocket closed safely")
            except Exception as e:
                print(f"\nError closing socket: {e}")


# Main execution
if __name__ == "__main__":
    # Demonstrate various exception scenarios
    demonstrate_all_exceptions()
    
    # Example of robust client
    print("\n\n" + "=" * 70)
    print("Testing Robust Client Implementation")
    print("=" * 70)
    
    # This will likely fail unless you have a server running
    create_robust_client("localhost", 5000, "Hello, Server!")