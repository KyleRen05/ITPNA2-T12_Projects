import socket
import os


SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001


def send_files(file_path, client_socket):
    try:
        if not os.path.exists(file_path):
            print(f"[ERROR] File not found: {file_path}")
            return
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        print(f"[SENDING...] {file_name} to {SERVER_IP}")
        client_socket.sendall(file_name.encode('utf-8'))

        print(f"[SENDING...] {file_size} bytes to {SERVER_IP}")
        client_socket.sendall(str(file_size).encode('utf-8'))

        bytes_sent = 0
        with open(file_path, 'rb') as file:
            while bytes_sent < file_size:
                chunk = file.read(4096)
                if not chunk:
                    break

                client_socket.sendall(chunk)
                bytes_sent += len(chunk)
                progress = (bytes_sent / file_size) * 100
                print(f"\rProgress: {progress:.1f}%", end='', flush=True)

            print(f"\rProgress: 100.0%")
            print(f" Sent {bytes_sent:,} bytes\n")
    except Exception as e:
        print(f"[ERROR] Send file: {e}")


def req_files(file_name, client_socket):
    print(f"[REQUEST] {file_name} from {SERVER_IP}")
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

        print(f"Please Enter your Name:\n")
        name = input()
        client_socket.sendall(name.encode('utf-8'))

        while True:
            print("Would you like to send or request a file?")
            print(" (1) SEND FILE\n (2) REQUEST FILE\n (3) EXIT PROGRAM\n")
            selection = input()
            client_socket.sendall(selection.encode('utf-8'))

            if selection.strip() == '1':
                print("Please enter file path of the file you want to send:")
                file_path = input()
                send_files(file_path, client_socket)
            elif selection.strip() == '2':
                print("Please enter reuqested file name:")
                file_name = input()
                req_files(file_name, client_socket)
            elif selection.strip() == '3':
                print("[EXIT] Exit Condition Met\nClosing Client Connection")
                break


    except ConnectionRefusedError:
        print(f"[ERROR] Could not connect to server at {SERVER_IP}:{SERVER_PORT}")
    
    except Exception as e:
        print(f" Error: {e}")
    
    finally:
        # Close connection
        client_socket.close()
        print("[DISCONNECT] Successful\n")
            

if __name__ == "__main__":
    start_client()