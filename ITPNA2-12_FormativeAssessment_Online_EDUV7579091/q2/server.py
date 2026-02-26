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

    client_data[0] = c_name
    client_data[1] = destination
    client_data[2] = str(passengers)

    write_ln = "|".join(client_data) + "\n"

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
        



if __name__ == "__main__":