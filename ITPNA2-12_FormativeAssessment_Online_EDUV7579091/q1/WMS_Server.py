""" SERVER SIDE """
import socket
import time
import threading

SERVER_IP = '127.0.0.1'
PORT = 5500

def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")

    while True:
        try:
             data = client_socket.recv(1024).decode('utf-8')
             print(f"Client {client_address} connected successfully!")

             # Client Exit Code
             if data == "exit":
                 break
        except:
            print("Error")


def start_server():
    """Start TCP Server"""

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((SERVER_IP, PORT))

    server_socket.listen()

    print(f'=' * 20)
    print(" TCP Chat Server Started")
    print("=" * 20)
    print(f" Listening on {SERVER_IP}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()


    except KeyboardInterrupt:
        print(f"\n\n Server interrupted by keyboard input")

    finally:
        client_socket.closee()
        server_socket.close()