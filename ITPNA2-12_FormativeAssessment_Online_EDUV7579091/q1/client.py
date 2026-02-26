""" CLIENT SIDE """
import socket

SERVER_IP = '127.0.0.1'
PORT = 5500

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("=" * 40)
    print("WMS Client")
    print("=" * 40)

    try:
        print(f"Connecting to {SERVER_IP}:{PORT}...")
        client_socket.connect((SERVER_IP, PORT))
        print("Connected to server\n")

        while True:
            print(f"What item are you looking for? ('exit' to quit)")
            message = input()

            if message.strip().lower() == "exit":
                print("Disconencting from server")
                client_socket.sendall("Exit".encode('utf-8'))
                break

            if message:
                client_socket.sendall(message.encode('utf-8'))

                reply = client_socket.recv(1024).decode('utf-8')
                print(reply, end='')

    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {SERVER_IP}:{PORT}")
    
    except Exception as e:
        print(f" Error: {e}")
    
    finally:
        # Close connection
        client_socket.close()
        print("[DISCONNECT] Successful\n")

if __name__ == "__main__":
    start_client()