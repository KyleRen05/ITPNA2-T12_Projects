import socket
import threading
import os

SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001

connected_clients = []
client_names = {}


def handle_client(client_socket, client_address):
    # handles connecting clients
    print(f"[NEW CONNECTION] {client_address} connected")

    try:
        client_name = client_socket.recv(1024).decode('utf-8').strip()
        client_names[client_socket] = client_name

        while True:
            selection = client_socket.recv(1024).decode('utf-8').strip()
            if selection == '1':
                print(f"[RECIEVE] {client_name} is sending a file\n")
                rec_files()
            elif selection == '2':
                print(f"[SEND] {client_name} wants to receive a file\n")
            elif selection == '3':
                print(f"[CLIENT DISCONNECT] {client_name} ({client_address[0]}) disconnected from the server")
                break
            else:
                print("Invalid Option")

    except Exception as e:
        print(f"[ERROR] {e}")

def send_files():
    return

def rec_files():
    return

def start_server():
    # Handles server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)

    server_socket.settimeout(1.0)

    print("=" * 30)
    print("Multi6Client File Transfer Server Started")
    print("=" * 30)
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