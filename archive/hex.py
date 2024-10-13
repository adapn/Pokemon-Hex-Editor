import sys
import struct
import os


    

# Main logic to run the program
def main():
    # Example file path, change it to the actual path or pass it as a command-line argument
    file_path = r"C:\Users\AdamA\Desktop\Future Goals\Pokemon\AAAAAAA VS CCCCCCC.sav"

 # Open the save file in binary mode and read its content
    with open(file_path, "rb") as file:
      data = file.read()

    # Use hexdump to return the file's hex data in string format
    data_16 = pyhexdump.hexdump(data)

 
    #print(offset[90])
# Execute the main function
if __name__ == "__main__":
    main()
