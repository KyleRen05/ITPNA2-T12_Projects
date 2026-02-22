""" CLIENT SIDE """
import socket
import time

""" NETWORKING """

CLIENT_IP = '127.0.0.1'
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

""" CLIENT REQUEST """
#print(f"What item are you looking for? ('exit' to end program)")
#req_item = input()

try:
    client.connect((CLIENT_IP, PORT))
    while True:     
        print(f"What item are you looking for? ('exit' to end program)")
        req_item = input()
        client.send(req_item.encode())

        data = client.recv(1024)
        print(f"{data.decode()}")

        data = client.recv(1024)
        print(f"{data.decode()}")
        
        if req_item.lower() == "exit":
            time.sleep(1)
            break
        
except:
    print(f"Error: Connection to server failed")

client.close()
