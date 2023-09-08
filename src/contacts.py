import os
import csv
from bitstring import ConstBitStream

def getContacts(file):
    ## Headers to look for (formatting is intentional)
    contactHeader = b'\x01\x06\x00\x05\x08\x08\x00'
    afterContactNameHeader = '0601'
    areaCodeInd = '0f'
    noAreaCodeInd = '0c'
    phoneNumberHeader = '0000ff000000'


    file_size_bytes = os.path.getsize(file)
    print(f'File size: {file_size_bytes} bytes') # Print file size

    #### EXTRACT CONTACT DATA
    ## Open phone memory dump image file
    data = open(file, 'rb')

    ## Load file into a bit data stream 
    s = ConstBitStream(filename=file)
    occurances = s.findall(contactHeader, bytealigned=True)
    occurances = list(occurances)
    foundOccurances = len(occurances)
    print("Found " + str(foundOccurances) + " memory addresses matching contact header " + str(contactHeader) + "\n")

    totalEntries = 0
    foundContactEntries = [["Entry #", "Contact Name", "Associated Phone Number", "Memory Address Offset"]]
## Read list of total occurances found
    for i in range(0, foundOccurances):
        ## Find each offset, then read
        occuranceOffset = hex(int(occurances[i]/8))

        ## Set bit stream position to individual offset
        s.bitpos = occurances[i]

        ## Record ~valid~ contact entry data
        # READ THE FIRST 8 BYTES (64 bits) -- a.k.a. the contactHeader (01 06 00 05 08 08 00)
        headerData = s.read('hex:64') 
        # SKIP THE NEXT 6 BYTES (48 bits)
        skipData = s.read('pad:48')
        # READ THE NEXT 3 BYTES (24 bits) -- bytes leading up to important data (00 04 00)
        leadingData = s.read('hex:24')
        # READ THE NEXT 1 BYTE (8 bits) -- a.k.a. the length of the following name entry
        contactNameLength = s.read('intle:8')
        # SKIP THE NEXT 1 BYTE (8 bits)
        skipData = s.read('pad:8')
        # READ THE NEXT n BYTES (8bit*n-bytes)-- a.k.a. the next number of bytes found from contactNameLength*8
        try: # skip entry if error is thrown
            CONTACT_NAME = s.read(8*contactNameLength).tobytes().decode()
        except UnicodeDecodeError:
            continue
        # READ THE NEXT 2 BYTES (16 bits) -- should be SAME for all entries (0x0601), else skip this occurance
        skipData = s.read('hex:16')
        if str(skipData) != afterContactNameHeader:
            continue
        # READ THE NEXT 1 BYTE (8 bits) -- either 0x0F or 0x0C (AREA CODE or NO AREA CODE included, meaning number is either 10d or 7d long)
        areaCodeData = s.read('hex:8')
        if str(areaCodeData) == areaCodeInd: # number will be 10d long (includes 3d area code)
            phoneNumberLength = 10
        elif str(areaCodeData) == noAreaCodeInd: # number will be 7d long (does not include area code)
            phoneNumberLength = 7
        else: # invalid/broken entry, so move on
            continue
        # READ THE NEXT 6 BYTES (48 bits) -- should be same for all valid entries, else skip bad entry
        skipData = s.read('hex:48')
        if str(skipData) != phoneNumberHeader:
            continue
        # READ THE NEXT n BYTES (8bit*n-bytes) -- a.k.a. the contact's phone number found from phoneNumberLength*8
        # Then format phone number
        tempPhone = s.read(8*phoneNumberLength).tobytes().decode()
        CONTACT_PHONE_NUMBER = ''
        is_10d_flag = False
        if len(tempPhone) == 10:
            is_10d_flag = True
        if is_10d_flag: 
            for i in range(0, len(tempPhone)):
                if i == 3 or i == 6:
                    CONTACT_PHONE_NUMBER = CONTACT_PHONE_NUMBER + '-' + tempPhone[i]
                else:
                    CONTACT_PHONE_NUMBER = CONTACT_PHONE_NUMBER + tempPhone[i]
        else:
            for i in range(0, len(tempPhone)):
                if i == 3:
                    CONTACT_PHONE_NUMBER = CONTACT_PHONE_NUMBER + '-' + tempPhone[i]
                else:
                    CONTACT_PHONE_NUMBER = CONTACT_PHONE_NUMBER + tempPhone[i]

            
        ## Increment found entry with each successful contact parsed 
        totalEntries += 1
        
        ## PRINT all important entry information
        print("Contact at address: " + str(occuranceOffset) + ", Entry #: " + str(totalEntries))
        print("\tName: " + str(CONTACT_NAME))
        print("\tNumber: " + str(CONTACT_PHONE_NUMBER))

        foundContactEntries.append([str(totalEntries), CONTACT_NAME, CONTACT_PHONE_NUMBER, str(occuranceOffset)])
    data.close()

    ## Write output to csv file
    with open('foundContacts.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, dialect=csv.excel)
        for entry in foundContactEntries:
            writer.writerow(entry)
    return totalEntries