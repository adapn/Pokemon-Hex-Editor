import sys
import struct
import os
import hexdump
import csv

# Function to load and process the save file data
def import_data(file_path):
    try:
        if not os.path.exists(file_path):
            print("Error: No file selected or file does not exist.")
            return

        # Open the save file in binary mode and read its content
        with open(file_path, "rb") as file:
            data = file.read()

        # Use hexdump to return the file's hex data in string format
        data_16 = hexdump.hexdump(data, result='return')

    except Exception as e:
        print(f"Error: {e}")
        return None

    # Split the data into lines for display
    lines = data_16.splitlines()

    offset = []
    byte_data = []
    decoded_text = []

    # Parse the hex dump into offset, byte data, and decoded text
    for x in range(len(lines)):
        offset.append(str(lines[x])[:10])
        byte_data.append(str(lines[x])[10:58])
        decoded_text.append(str(lines[x])[58:])

    for x in range(len(decoded_text)):
        decoded_text[x] = decode(byte_data[x])
        
    # Display the parsed hex data in the console
    for x in range(len(lines)):
        print(f"List index: {x} | Offset: {offset[x]} | Data: {byte_data[x]} | Decoded Text: {decoded_text[x]}")

    return offset, byte_data, decoded_text # return the lists 


def decode(assembly):
    #turn the string into an array after each space, so
    #80 80 80 80 80 80 80 50 
    #=[80][80[80]....

    #Turns the assembly string into a list
    assembly_list = assembly.split()

    hex_to_char = {
        '80': 'A', '81': 'B', '82': 'C', '83': 'D', '84': 'E', '85': 'F',
        '86': 'G', '87': 'H', '88': 'I', '89': 'J', '8A': 'K', '8B': 'L',
        '8C': 'M', '8D': 'N', '8E': 'O', '8F': 'P', '90': 'Q', '91': 'R',
        '92': 'S', '93': 'T', '94': 'U', '95': 'V', '96': 'W', '97': 'X',
        '98': 'Y', '99': 'Z', '50': ' ','7F': ' ','F1': '×','9A': '(','9B': ')','9C': ':','9D': ';','9E': '[','9F': ']',
        'E3': '-','E6': '?','E7': '!','F2': '.','F4': ',','00': ' ',
         
         
          # Adding a space character for A0
        # Add other mappings as needed...
        }
    #name is 7 chars long 
    translated_name = ''.join(hex_to_char.get(byte, '?') for byte in assembly_list)
    GREY_BACKGROUND = "\033[48;5;237m"  # Grey background
    RESET = "\033[0m"  # Reset to default
    print(f"{GREY_BACKGROUND}{translated_name}{RESET}")
    return translated_name

def trainer_name(offset, byte_data):
    #trainer name is located at 00002598
    #lets output where this line is located in the list

    for x in range(len(offset)):
        if offset[x] == "00002590: ":
            trainer_offset = x

    assembly_name = byte_data[trainer_offset][25:]
    print(assembly_name)
    decode(assembly_name)


def rival_name(offset, byte_data):
    #trainer name is located at 00002598
    #lets output where this line is located in the list

    for x in range(len(offset)):
        if offset[x] == "000025F0: ":
            trainer_offset = x

    assembly_name = byte_data[trainer_offset][17:43]
    #print(assembly_name)
    print(assembly_name)
    decode(assembly_name)

def change_trainer_name(new_name, file_path):
    if len(new_name) > 7:
        print("New Trainer Name too Long")
        return
    
    #Now we encode the char.
    
    hex_to_char = {
        'A': '80', 'B': '81', 'C': '82', 'D': '83', 'E': '84', 'F': '85',
        'G': '86', 'H': '87', 'I': '88', 'J': '89', 'K': '8A', 'L': '8B',
        'M': '8C', 'N': '8D', 'O': '8E', 'P': '8F', 'Q': '90', 'R': '91',
        'S': '92', 'T': '93', 'U': '94', 'V': '95', 'W': '96', 'X': '97',
        'Y': '98', 'Z': '99', ' ': '50'  # Map space character
    }

    hex_new_name = []
    #Crazy you can do this in python
    for char in new_name:
         hex_value = hex_to_char.get(char.upper(), '00') ##Convert hex to char 
         hex_new_name.append(hex_value) ##Appedns it
    hex_new_name.append("50")

    #FIll the remainding chars with 00
    for x in range(7 - len(new_name)):
        hex_new_name.append("00")


    # Convert hex string list to actual bytes...goes fomr [90,90,80,80] to  b'\x80\x81\x82'.
    name_bytes = bytes(int(x, 16) for x in hex_new_name)


    #The trainer offset, The `trainer_offset` is defined as `0x2598`, which specifies the location in the save 
    # file where the trainer's name is stored. We use hexadecimal to represent this offset because it is more compact 
    # and easier to read than binary. When we open the file in binary mode (`"rb"`), we can seek to this offset and read the 
    # raw bytes that correspond to the trainer's name. This approach allows us to accurately access and modify the specific data 
    # stored in the save file.
    trainer_offset = 0x2598
    with open(file_path, "r+b") as file:
        file.seek(trainer_offset)
        file.write(name_bytes)

    print(f"The new trainer name of {new_name} has been applied")



def change_rival_name(new_name, file_path):
    if len(new_name) > 7:
        print("New Rival Name too Long")
        return
    
    #Now we encode the char.
    
    hex_to_char = {
        'A': '80', 'B': '81', 'C': '82', 'D': '83', 'E': '84', 'F': '85',
        'G': '86', 'H': '87', 'I': '88', 'J': '89', 'K': '8A', 'L': '8B',
        'M': '8C', 'N': '8D', 'O': '8E', 'P': '8F', 'Q': '90', 'R': '91',
        'S': '92', 'T': '93', 'U': '94', 'V': '95', 'W': '96', 'X': '97',
        'Y': '98', 'Z': '99', ' ': '50'  # Map space character
    }

    hex_new_name = []
    #Crazy you can do this in python
    for char in new_name:
         hex_value = hex_to_char.get(char.upper(), '00') ##Convert hex to char 
         hex_new_name.append(hex_value) ##Appedns it
    hex_new_name.append("50")

    #FIll the remainding chars with 00
    for x in range(7 - len(new_name)):
        hex_new_name.append("00")


    # Convert hex string list to actual bytes...goes fomr [90,90,80,80] to  b'\x80\x81\x82'.
    name_bytes = bytes(int(x, 16) for x in hex_new_name)


    #The trainer offset, The `trainer_offset` is defined as `0x2598`, which specifies the location in the save 
    # file where the trainer's name is stored. We use hexadecimal to represent this offset because it is more compact 
    # and easier to read than binary. When we open the file in binary mode (`"rb"`), we can seek to this offset and read the 
    # raw bytes that correspond to the trainer's name. This approach allows us to accurately access and modify the specific data 
    # stored in the save file.
    trainer_offset = 0x25F6
    with open(file_path, "r+b") as file:
        file.seek(trainer_offset)
        file.write(name_bytes)

    print(f"The new rival name of {new_name} has been applied")


def set_money(amount, file_path):
    if amount > 999999:
        print("Too much Money! ")
        return
    
    with open(file_path, "r+b") as file:
        #User types lets say 999999
        #Convert it to, [99 99 99]
        #Find the hex value which corresponds to 99
        #Go to each correspoding byte and add the value
        # Split the amount into three parts
        part1 = (amount // 10000) % 100  # First two digits (e.g., for 999999 -> 99)
        part2 = (amount // 100) % 100     # Middle two digits (e.g., for 999999 -> 99)
        part3 = amount % 100              # Last two digits (e.g., for 999999 -> 99)

        file.seek(0x25F3)  # Offset for first part
        file.write(bytes([part1]))
        
        file.seek(0x25F4)  # Offset for second part
        file.write(bytes([part2]))
        
        file.seek(0x25F5)  # Offset for third part
        file.write(bytes([part3]))
  

def verify_trainer_name(file_path):
    trainer_offset = 0x2590
    with open(file_path, "rb") as file:
        file.seek(trainer_offset)
        data = file.read(8)  # Read 7 bytes + 1 for padding
        print(f"Written name hex: {data}")


def check_sum(file_path):
    with open(file_path, "r+b") as file:
        
        #pretend initialize the checksum to 255
        check_sum = 0xFF

        #For every byte between 0x2598 to 0x3522 inclusive. Subtract from check_sum
        file.seek(0x2598)
        data = file.read(0x3522 - 0x2598 + 1)  # +1 to include the end offset
       
         # Iterate over each byte in the data and update the checksum
        for byte in data:
            check_sum -= byte  # Subtract the value of each byte
            check_sum &= 0xFF  # Ensure check_sum is a valid byte

        file.seek(0x3523)
        file.write(bytes([check_sum]))
        print(f"Check Sum of : {bytes([check_sum])} added")
       # file.seek(0x3523)
       # written_value = file.read(1)
        #print(f"The value at 0x3523 is {written_value.hex()} ")
        

def encode(string):
    hex_to_char = {
        'A': '80', 'B': '81', 'C': '82', 'D': '83', 'E': '84', 'F': '85',
        'G': '86', 'H': '87', 'I': '88', 'J': '89', 'K': '8A', 'L': '8B',
        'M': '8C', 'N': '8D', 'O': '8E', 'P': '8F', 'Q': '90', 'R': '91',
        'S': '92', 'T': '93', 'U': '94', 'V': '95', 'W': '96', 'X': '97',
        'Y': '98', 'Z': '99', ' ': '50'  # Map space character
          }
    encoded_string = []
    for char in string:
        hex_value = hex_to_char.get(char.upper(), '00') ##Convert hex to char 
        encoded_string.append(hex_value) ##Appedns it

    print(f"{string} in hex is {encoded_string}")
 
def save_to_csv(offset, byte_data, decoded_text, output_path="output.csv"):
    with open(output_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Offset", "Data", "Decoded Text"])  # Write header
        for i in range(len(offset)):
            writer.writerow([offset[i], byte_data[i], decoded_text[i]])
    print(f"Data saved to {output_path}")

def save_to_txt(offset, byte_data, decoded_text, output_path="output.txt"):
    with open(output_path, "w") as txt_file:
        for i in range(len(offset)):
            txt_file.write(f"Offset: {offset[i]} | Data: {byte_data[i]} | Decoded Text: {decoded_text[i]}\n")
    print(f"Data saved to {output_path}")

# Main logic to run the program
def main():
    # Example file path, change it to the actual path or pass it as a command-line argument
    file_path = r"C:\Users\AdamA\Desktop\Future Goals\Pokemon\Pokemon Red.sav"
    
    #Load and display the hex data from the save file
    offset, byte_data, decoded_text = import_data(file_path)
    trainer_name(offset, byte_data)
    rival_name(offset, byte_data)

    #save_to_csv(offset, byte_data, decoded_text, output_path=".csv")
    #save_to_txt(offset, byte_data, decoded_text, "my_custom_output.txt")
    change_trainer_name("ADAM", file_path)
    change_rival_name("AYESHA", file_path)
    set_money(8760, file_path)

    encode("BADGES")
    check_sum(file_path)  

# Execute the main function
if __name__ == "__main__":
    main()
