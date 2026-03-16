import socket
import ssl

SERVER_IP = 'localhost'
PORT = 8443
SERVER_CERT = 'server-cert.pem'

def create_tls_client():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

    # Prevent SSL error without disabling the security checks
    context.load_verify_locations(SERVER_CERT)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tls_socket = context.wrap_socket(client_socket, server_hostname=SERVER_IP)

    print(f"[CONNECTING] Connecting to {SERVER_IP}:{PORT}")
    tls_socket.connect((SERVER_IP, PORT))
    print("[SUCCESS] Connected Successfully")

    return tls_socket


def start_client():
    print("=" * 60)
    print("TLS/SSL Client")
    print("=" * 60)

    try:
        tls_socket = create_tls_client()

        cipher = tls_socket.cipher()
        if cipher:
            print("[SUCCESS] TLS Connection Established:")
            print(f"\tCipher {cipher[0]}\n\tProtocol: {cipher[1]}\n\tKey Bits: {cipher[2]}")

            message = "Hello from Secure Client ^^"
            print(f"\n[SENDING...] '{message}'")
            tls_socket.sendall(message.encode('utf-8'))

            response = tls_socket.recv(4096)
            print(f"[RECEIVED] Response from Server: '{response.decode('utf-8')}'")

            tls_socket.close()
            print(f"[CLOSED] TLS Socket Closeed Successfully!")

    except Exception as e:
        print(f"[ERROR] Could not close Connection\n{e}")
        print("[TIP] Make sure TLS Server is running")

if __name__ == "__main__":
    start_client()