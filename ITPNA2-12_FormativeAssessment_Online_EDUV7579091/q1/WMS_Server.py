""" SERVER SIDE """
import socket
import time

""" NETWORKING PORTION """

SERVER_IP = '127.0.0.1'
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, PORT))

server.listen()

""" WAREHOUSE PORTION"""

items = {
    "Screws": 10,
    "Nails": 50,
    "2x4 Plank": 25,
    "Sheet Metal": 400,
    "Toolkit": 72,
    "Sandpaper": 0
}
in_stock = 1


try:
    
    client, client_addr = server.accept()
    print(f"Connecting to client {client_addr[0]}:{PORT}")

    while True:
        client_req = client.recv(1024).decode()

        print(f"Searching for {client_req}")
        client.send(f"\nChecking for product . . .".encode())
        
        for item in items:
            if client_req in items and items[client_req] > 0:
                in_stock = 1
                break
            else:
                in_stock = 0
        
        
        if client_req.lower() == "exit":
            print(f"Exiting program . . .")
            client.send(f"Exiting program . . .".encode())
            time.sleep(1)
            break

        if in_stock == 1:
            client.send(f"{client_req}: {items[client_req]}".encode())
            print(f"{client_req}: {items[client_req]}")
            
        else:
            client.send(f"{client_req} is not available\n".encode())
            print(f"{client_req} not found")


except:
    print(f"Connection Failed")

    #except KeyboardInterrupt:
    #    print("Keyboard Interrupt")
    #    server.close()
server.close()
