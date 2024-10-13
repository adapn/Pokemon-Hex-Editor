def rival_name(offset, byte_data):
    #trainer name is located at 00002598
    #lets output where this line is located in the list

    for x in range(len(offset)):
        if offset[x] == "00000014: ":
            trainer_offset = x

    assembly_name = byte_data[trainer_offset][25:]
    #print(assembly_name)
    decode(assembly_name)