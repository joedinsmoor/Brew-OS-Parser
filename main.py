import os
import re
from bitstring import ConstBitStream

def main():
    ## Headers to look for
    contactHeader = b'\x01\x06\x00\x05\x08\x08\x00'

    ## Prompt user to specify file from path
#    file = input("Enter filename of binary to decode: ")
    file = '/Users/cersinterns2/Downloads/23-9726.bin' # Using a static filepath for now (testing-delete later)

    ## Initialize filesize (given a starting and ending offset)
    file_size_bytes = os.path.getsize(file)
    print(f'File size in bytes: {file_size_bytes} bytes') # Print file size

    ## Open and read file contents
    with open(file, mode="rb") as f:
        contents = f.read()
        try:
            offset = hex(contents.index(contactHeader))
            formatted_offset = '0x' + offset[2:].zfill(8) # format 0xXXXXXX -> 0x00XXXXXX leading zeroes
            print(formatted_offset)
        except ValueError:
            print('Invalid file')
#            
#        if b'\x01\x06\x00\x05\x08\x08\x00' in f.read():
#            print('Contains Contact data!')
#            offset = hex(f.tell())
#            print(offset)


if __name__ == '__main__':
    main()