import socket
import os


SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001


def send_files():
    return

def req_files():
    return

def start_client():
    #Start client side
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("=" * 60)
    print("Multi-Client File Transfer Server Started")
    print("=" * 60)

    try:
        print(f"Connecting to {SERVER_IP}:{SERVER_PORT}")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to Server\n")

        while True:
            

if __name__ == "__main__":
    start_client()