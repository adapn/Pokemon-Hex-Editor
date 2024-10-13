import sys
import struct
import os
import hexdump

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

    for x in range(7 - len(new_name)):
        hex_new_name.append("00")

    # Convert hex list to byte array
    hex_bytes = bytes(int(h, 16) for h in hex_new_name)
   
    # Trainer name is located at offset 0x2590
    trainer_offset = 0x2590

    try:
        with open(file_path, "r+b") as file:
            file.seek(trainer_offset)
            file.write(hex_bytes)
            print(f"The trainer name has been changed to {new_name}")
            
    except Exeption as e:
        print(f"Error: {e}")

    print("sadasdasd")




def verify_trainer_name(file_path):
    trainer_offset = 0x2590
    with open(file_path, "rb") as file:
        file.seek(trainer_offset)
        data = file.read(8)  # Read 7 bytes + 1 for padding
        print(f"Written name hex: {data}")









# Main logic to run the program
def main():
    # Example file path, change it to the actual path or pass it as a command-line argument
    file_path = r"C:\Users\AdamA\Desktop\Future Goals\Pokemon\Pokemon Red.sav"

    # Load and display the hex data from the save file
    offset, byte_data, decoded_text = import_data(file_path)
    trainer_name(offset, byte_data)
    rival_name(offset, byte_data)

    new_name = "ADAMP"

    change_trainer_name(new_name, file_path)
    verify_trainer_name(file_path)
    #print(offset[90])
# Execute the main function
if __name__ == "__main__":
    main()
