import socket
import threading
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001
FILE_STORE = "files"

connected_clients = []
client_names = {}

if not os.path.exists(FILE_STORE):
    os.makedirs(FILE_STORE)
    print(f"[CREATED] Directory: {FILE_STORE}")

def handle_client(client_socket, client_address):
    # handles connecting clients
    print(f"[NEW CONNECTION] {client_address} connected")

    try:
        client_name = client_socket.recv(1024).decode('utf-8').strip()
        client_names[client_socket] = client_name

        while True:
            selection = client_socket.recv(1024).decode('utf-8').strip()
            if selection.strip() == '1':
                print(f"[RECIEVE] {client_name} is sending a file\n")
                file_name = client_socket.recv(1024).decode('utf-8')
                rec_files(file_name, client_socket, client_address, client_name)
            elif selection.strip() == '2':
                print(f"[SEND] {client_name} wants to receive a file\n")
            elif selection.strip() == '3':
                print(f"[CLIENT DISCONNECT] {client_name} ({client_address[0]}) disconnected from the server")
                break
            else:
                print("Invalid Option")
                break

    except Exception as e:
        print(f"[ERROR] {e}")

def send_files():
    return

def rec_files(file_name, client_socket, client_address, client_name):
    try:

        print(f"[RECEIVING...] {file_name} from {client_name}")
        print(f"\t({client_address[0]}:{client_address[1]})")

        file_size = int(client_socket.recv(1024).decode('utf-8'))
        print(f"\tSize: {file_size:,} bytes ({file_size/1024:.2f} KB)")

        file_path = os.path.join(FILE_STORE, file_name)

        bytes_received = 0

        with open(file_path, 'wb') as file:
            print(f"   Receiving data...", end='', flush=True)

            while bytes_received < file_size:
                bytes_to_read = min(4096, file_size - bytes_received)
                chunk = client_socket.recv(bytes_to_read)

                if not chunk:
                    print("\nNOT CHUNK")
                    break
                
                file.write(chunk)
                bytes_received += len(chunk)
                if bytes_received % 102400 == 0:
                    progress = (bytes_received / file_size) * 100
                    print(f"\r   Progress: {progress:.1f}%", end='', flush=True)
            
        print(f"\r   Progress: 100.0%")

        if bytes_received == file_size:
            print(f"[SAVED] {file_path}")
            print(f"[COMPLETE] {bytes_received:,} bytes\n")
        else:
            print(f"[INCOMPLETE] File Transfer Incomplete {bytes_received}/{file_size}")
    except Exception as e:
        print(f"[ERROR] Files not Recieved\n{e}")



def start_server():
    # Handles server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)

    server_socket.settimeout(1.0)

    print("=" * 60)
    print("Multi-Client File Transfer Server Started")
    print("=" * 60)
    print(f"List6ting on {SERVER_IP}:{SERVER_PORT}")
    print(f"Waiting for Client Connections...\n")

    try:
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                connected_clients.append(client_socket)

                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

                # Show Active Connections
                print(f"[ACTIVE CONNECTIONS] {len(connected_clients)} client(s) connected\n")
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("\n\n Server Shutting Down")
    finally:
        for clients in connected_clients:
            clients.close()
        server_socket.close()
        print(" Server Stopped")
    

if __name__ == "__main__":
    start_server()