from bitstring import ConstBitStream
from src.sms import *
from src.contacts import *

def input_file():
    filename = input("Path to binary BREW OS memory image file: ")
    return filename

def main():
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