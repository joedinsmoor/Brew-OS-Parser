import os
import csv
from bitstring import ConstBitStream
from src.sms import *
from src.contacts import *

def input_file():
    filename = input("Path to binary BREW OS memory image file: ")
    return filename

def main():
    ## Headers to look for (formatting is intentional)
    contactHeader = b'\x01\x06\x00\x05\x08\x08\x00'
    smsHeader = b'\x02\x15\x00\x00\x01\x16\x01\x04\x06'
    afterContactNameHeader = '0601'
    msgNumberHeader = '7f80'
    areaCodeInd = '0f'
    noAreaCodeInd = '0c'
    phoneNumberHeader = '0000ff000000'

    ## Prompt user to specify file from path (DOES NOT HANDLE ERRORS PROPERLY)
    file = input_file()
#    file = '/Users/cersinterns2/Downloads/23-9726.bin' #Static filepath for testing
    while file == "":
        print("Enter valid path to file")
        file = input_file()

    contactEntries = getContacts(file)
    
    print("\nTotal contact entries found: " + str(contactEntries))

    #*****************************************************************
    smsEntries = getSMS(file)
    print("\nTotal SMS data entries found: " + str(smsEntries))
    
if __name__ == '__main__':
    main()