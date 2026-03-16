import socket
import ssl

SERVER = '127.0.0.1'
PORT = 8443
CERT_FILE = 'server-cert.pem'
KEY_FILE = 'server-key.pem'

def create_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    try:
        context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    except:
        print("[ERROR] Certificate files not found")
        print("Run generate_certificates.sh first")
        exit(1)

    context.minimum_version = ssl.TLSVersion.TLSv1_2

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((SERVER, PORT))

    server_socket.listen(5)

    server_socket.settimeout(1.0)

    return server_socket, context


def handle_client(client_socket, client_address):
    print(f"\nConnection from {client_address[0]}:{client_address[1]}")

    cipher = client_socket.cipher()
    if cipher:
        print(f"\tCipher: {cipher[0]}")
        print(f"\tTLS Version {cipher[1]}")
    
    try:
        data = client_socket.recv(4096)

        if data:
            message = data.decode('utf-8')
            print(f"Received Message: {message}")

            response = f"Server Received: {message}"
            client_socket.sendall(response.encode('utf-8'))
            print(f"\tSent Response")

    except Exception as e:
        print(f"[ERROR] Client Handle Error: {e}")

    finally:
        client_socket.close()
        print(f"\tClient {client_address[0]} closed")


def start_server():
    print("=" * 60)
    print(f"TLS/SSL Server")
    print("=" * 60)
    print(f"Starting TLS/SSL Server on {SERVER}:{PORT}")
    print(f"Certificate: {CERT_FILE}")
    print(f"Private Key: {KEY_FILE}")

    server, context= create_server()

    try:
        while True:
            try:
                raw_client_socket, client_address = server.accept()
                secure_client_socket = context.wrap_socket(raw_client_socket, server_side=True)
                handle_client(secure_client_socket, client_address)
                raw_client_socket.close()

            except socket.timeout:
                continue

    except ssl.SSLError as e:
        print(f"[SECURITY ALERT] Handshake failed for {client_address[0]}")
        print(f"Clear failure message: Unauthorized or bad certificate. Details: {e}")
        #raw_client_socket.close()

    except Exception as e:
        print(f"[ERROR] SERVER ERROR: {e}")

    except KeyboardInterrupt:
        print("\n\nServer Stopped by user")

    finally:
        raw_client_socket.close()
        server.close()
        print("Server Socket Closed")


if __name__ == "__main__":
    start_server()