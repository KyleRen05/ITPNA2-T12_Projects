""" SERVER SIDE """
import socket

SERVER_IP = '127.0.0.1'
PORT = 5500

server_running = True

items = {
    "Nails": 200,
    "Screws": 321,
    "Toolkit": 59,
    "Wood Planks": 97,
    "Sheet Metal": 153,
    "Lightbulb": 76,
}

def handle_client(client_socket, client_address):
    print(f"Connected to {client_address}")
    global server_running

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8').strip()
            print(f"Client {client_address} connected successfully!")

            # in case client presses enter
            if not data:
                continue

             # Client Exit Code
            if data == "exit":
                print(f" [DISCONNECT] {client_address} sent the exit code.")
                server_running = False
                break

            # search through dictionary to find item
            if data in items and items[data] > 0:
                message = f"[ITEM FOUND] {data} : {items[data]}"
            else:
                message = f"[ITEM NOT FOUND] {data} is not in stock"

            client_socket.sendall((message + "\n").encode('utf-8'))
                    
        except ConnectionResetError:
            print(f"Error: Client Closed Connection Upbruptly")
        except Exception as e:
            print(f"Error: {e}")
    client_socket.close()


def start_server():
    """Start TCP Server"""

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((SERVER_IP, PORT))

    server_socket.listen()
    global server_running

    # Allows for keyboard interrupt on server side every 1 second
    server_socket.settimeout(1.0)

    print(f'=' * 40)
    print(" TCP WMS Server Started")
    print("=" * 40)
    print(f" Listening on {SERVER_IP}:{PORT}")

    try:
        while server_running == True:

            try:

                client_socket, client_address = server_socket.accept()
                
                # When client connects, remove timeout
                client_socket.settimeout(None)

                handle_client(client_socket, client_address)

                if server_running == False: break

            except socket.timeout:
                continue
            
    except KeyboardInterrupt:
        print(f"\n\n Server interrupted by keyboard input")

    finally:
        if 'client_socket' in locals():
            client_socket.close()
        server_socket.close()

        print(f" Server Closed\n")

if __name__ == "__main__":
    start_server()