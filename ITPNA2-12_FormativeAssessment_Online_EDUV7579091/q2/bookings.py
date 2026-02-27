# QUESTION 2
client_data = []
FIXED_PRICE = 500

def handle_input():
    print("Client Name:\n")
    c_name = input

    print("Destinaion:\n")
    destination = input()

    print("Number of Passengers:\n")
    passengers = input()

    write_ln = f"{c_name} | {destination} | {passengers}\n"

    return write_ln

def handle_file(write_ln):
    with open("client_info.txt", "a+") as file:
        file.write(write_ln)

def order_data():
    with open("client_info.txt", "r") as file:
        for line in file:
            parts = line.strip().split("|")

            if len(parts) >= 3:
                client_data.append(parts)
        
        
def start_booking():
    
    while True:
        print(f"What would you like to do?")
        print("(A) Create a booking\n(B) View Current Bookings\n(C) Exit Application\n")
        selection = input()

        if selection == 'A':
            write_ln = handle_input()
            handle_file(write_ln)
        elif selection == 'B':
            order_data()
        elif selection == 'C':
            break
        else:
            print("Please Enter a Valid Option\n")





if __name__ == "__main__":
    start_booking()
    print("Closing Application")