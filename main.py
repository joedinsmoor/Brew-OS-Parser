import os
import re
from io import TextIOWrapper
from bitstring import ConstBitStream

def main():
    ## Headers to look for
    contactHeader = b'\x01\x06\x00\x05\x08\x08\x00'
    afterContactNameHeader = '0601'
    areaCodeInd = '0f'
    noAreaCodeInd = '0c'
    phoneNumberHeader = '0000ff000000'

    ## Prompt user to specify file from path
#    file = input("Enter filename of binary to decode: ")
    #file = '/Users/cersinterns2/Downloads/23-9726.bin' # Using a static filepath for now (testing-delete later)
    file = '/Users/nixycamacho/Downloads/23-9726.bin' # Using a static filepath for now (testing-delete later)

    ## Initialize filesize (given a starting and ending offset)
    file_size_bytes = os.path.getsize(file)
    print(f'File size in bytes: {file_size_bytes} bytes') # Print file size

    header_occurances = [] # List to hold first occurances of all header data

    data = open(file, 'rb')

    s = ConstBitStream(filename=file)
    occurances = s.findall(contactHeader, bytealigned=True)
    occurances = list(occurances)
    totalOccurances = len(occurances)
    print("Total occurances of contacts found: " + str(totalOccurances))
    byteOffset = 0

## Read list of total occurances found
    for i in range(0, totalOccurances):
        ## Find each offset, then read
        occuranceOffset = hex(int(occurances[i]/8))

        ## Set bit stream position to individual offset
        s.bitpos = occurances[i]

        ## READ THE NEXT 8 BYTES (64 bits) -- a.k.a. the contactHeader 
        headerData = s.read('hex:64') 
        ## SKIP THE NEXT 6 BYTES (48 bits) 
        skipData = s.read('pad:48')
        ## READ THE NEXT 3 BYTES (24 bits) -- bytes leading up to important data 
        leadingBytes = s.read('hex:24')
        ## READ THE NEXT 1 BYTE (8 bits) -- a.k.a. the length of the following name entry
        contactNameLength = s.read('intle:8')
        ## SKIP THE NEXT 1 BYTE (8 bits)
        skipData = s.read('pad:8')
        ## READ THE NEXT n BYTES (8bit*n-bytes)-- a.k.a. the next number of bytes found from contactNameLength*8
        try: # skip if error is thrown
            CONTACT_NAME = s.read(8*contactNameLength).tobytes().decode()
        except UnicodeDecodeError:
            CONTACT_NAME = 'Null/Bad Entry'
        ## READ THE NEXT 2 BYTES (16 bits) -- should be SAME for all entries (0x0601), else skip this occurance
        skipData = s.read('hex:16')
        if str(skipData) != afterContactNameHeader:
            continue
        ## READ THE NEXT 1 BYTE (8 bits) -- either 0x0F or 0x0C (AREA CODE or NO AREA CODE included, meaning number is either 10d or 7d long)
        areaCodeData = s.read('hex:8')
        if str(areaCodeData) == areaCodeInd: # number will be 10d long (includes 3d area code)
            phoneNumberLength = 10
        elif str(areaCodeData) == noAreaCodeInd: # number will be 7d long (does not include area code)
            phoneNumberLength = 7
        else: # invalid/broken entry, so move on
            continue
        ## READ THE NEXT 6 BYTES (48 bits) -- should be same for all valid entries, else skip bad entry
        skipData = s.read('hex:48')
        if str(skipData) != phoneNumberHeader:
            continue
        ## READ THE NEXT n BYTES (8bit*n-bytes) -- a.k.a. the contact's phone number found from phoneNumberLength*8
        CONTACT_PHONE_NUMBER = s.read(8*phoneNumberLength).tobytes().decode()
        

        
        ## PRINT all important entry information
        #print("Address " + str(i) + ": "+ str(occuranceOffset) + ", Header: " + str(headerData))
        print("Contact at address: " + str(occuranceOffset))
#        print("\tSkipped: " + str(skipData))
#        print("\tLeading: " + str(leadingBytes))
#        print("\tLength: " + str(contactNameLength))
#        print("\tSkip: " + str(skipData))
        print("\tName: " + str(CONTACT_NAME))
#        print("\tNext: " + str(skipData))
#        print("\tNext: " + str(areaCodeData))
#        print("\tNext: " + str(skipData))
        print("\tNumber: " + str(CONTACT_PHONE_NUMBER))

    data.close()


###### OLD CODE (delete later)
#    ## Open and read file contents
#    with open(file, mode="rb") as f:
#        contents = f.read()
#        try:
#            offset = contents.index(contactHeader)
#
#            formatted_offset = hex(offset)
#            formatted_offset = '0x' + formatted_offset[2:].zfill(8) # format 0xXXXXXX -> 0x00XXXXXX leading zeroes
#            header_occurances.append(offset)
#            print(formatted_offset)
#
#            offset = int(offset)
#            print("Offset: " + str(offset))
#
#            n = f.seek(offset)
#            print("n: " + str(n))
            
            # move 64 ascii characters/bytes with f.seek() TO THE NEXT ENTRY

#            list = re.findall(contactHeader, contents)
#            regex = re.compile(contactHeader)
#            for match_obj in regex.finditer(contents):
#                offset = match_obj.start()
#                print ("decimal: ")

#            print(list)

#        except ValueError:
#            print('Invalid file')

if __name__ == '__main__':
    main()