import socket
import os


SERVER_IP = '127.0.0.1'
SERVER_PORT = 5001


def send_files(file_path):
    print(f"[SENDING...] {file_path} to {SERVER_IP}")
    return

def req_files(file_name):
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

        while True:
            print("Would you like to send or request a file?")
            print(" (1) SEND FILE\n (2) REQUEST FILE\n (3) EXIT PROGRAM\n")
            selection = input()

            if selection == '1':
                client_socket.sendall(selection.encode('utf-8'))
                print("Please enter file path of the file you want to send:\n")
                file_path = input()
                send_files(file_path)
            elif selection == '2':
                client_socket.sendall(selection.encode('utf-8'))
                print("Please enter reuqested file name:\n")
                file_name = input()
                req_files(file_name)
            elif selection == '3':
                client_socket.sendall(selection.encode('utf-8'))
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