# QUESTION 2
from operator import itemgetter
client_data = []
FIXED_PRICE = 20

def handle_input():
    print("Client Name:")
    c_name = input()

    print("\nDestinaion:")
    destination = input()

    print("\nNumber of Passengers:")
    passengers = input()

    write_ln = f"{c_name} | {destination} | {passengers}\n"

    return write_ln

def handle_file(write_ln):
    with open("client_info.txt", "a+") as file:
        file.write(write_ln)

def order_data():
    with open("client_info.txt", "r") as file:
        for line in file:
            data = line.strip().split('|')
            if data:
                client_data.append(data)

    for clients in client_data:
        total_price = clients[2]
        total_price = total_price.lstrip()
        total_price = int(total_price)
        
        total_price = total_price * FIXED_PRICE
        clients.append(total_price)
    
    client_data.sort(key=itemgetter(3), reverse=True)

    print(f"=" * 70)
    print(f"{' NAME':<20} {'DESTINATION':<20} {'PASSENGERS':<20} PRICE")
    print("=" * 70)
    for client in client_data:
        output = f" {client[0]:<20} {client[1]:<24} {client[2]:<15} ${client[3]}\n"
        print(output)
    


def start_booking():
    
    while True:
        print(f"What would you like to do?")
        print("(A) Create a booking\n(B) View Current Bookings\n(C) Exit Application\n")
        selection = input().upper()

        if selection == 'A':
            write_ln = handle_input()
            handle_file(write_ln)
            print("Client Added Successfully\n")
        elif selection == 'B':
            order_data()
        elif selection == 'C':
            break
        else:
            print("Please Enter a Valid Option\n")


if __name__ == "__main__":
    start_booking()
    print("Closing Application")