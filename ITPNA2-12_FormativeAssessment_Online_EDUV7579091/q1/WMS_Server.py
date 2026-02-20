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
in_stock = False


while True:
    try:
        client, client_addr = server.accept()
        
        client_req = client.recv(1024).decode()

        print(f"Searching for {client_req}")
        client.send(f"\nChecking for product . . .".encode())
        
        for item in items:
            if client_req in items and items[client_req] > 0:
                in_stock = True
            else:
                in_stock = False
        
        if in_stock == True:
            client.send(f"{client_req}: {items[client_req]}".encode())
            
        elif client_req.lower() == "exit":
            print(f"Exiting program . . .")
            client.send(f"Exiting program . . .".encode())

        else:
            client.send(f"{client_req} is not available".encode())

        time.sleep(1)
        break


    except Exception as e:
        print(f"Error:  {e}")
        break

    #except KeyboardInterrupt:
    #    print("Keyboard Interrupt")
    #    server.close()
server.close()
