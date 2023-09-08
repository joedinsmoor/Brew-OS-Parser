import csv
from bitstring import ConstBitStream

#### EXTRACT SMS DATA
def getSMS(file):
    ## Headers to look for (formatting is intentional)
    smsHeader = b'\x02\x15\x00\x00\x01\x16\x01\x04\x06'
    msgNumberHeader = '7f80'

    ## Open phone memory dump image file
    data2 = open(file, 'rb')

    ## Load file into a bit data stream 
    s = ConstBitStream(filename=file)
    occurances = s.findall(smsHeader, bytealigned=True)
    occurances = list(occurances)
    foundOccurances = len(occurances)
    print("Found " + str(foundOccurances) + " memory addresses matching SMS header " + str(smsHeader) + "\n")

    totalEntries = 0
    foundSmsEntries = [["Entry #", "Message Content", "Associated Phone Number", "Memory Address Offset"]]
## Read list of total occurances found
    for i in range(0, foundOccurances):
        ## Find each offset, then read
        occuranceOffset = hex(int(occurances[i]/8))

        ## Set bit stream position to individual offset
        s.bitpos = occurances[i]

        ## Record ~valid~ contact entry data
        # READ THE FIRST 9 BYTES (72 bits) -- a.k.a. the smsHeader (02 15 00 00 01 16 01 04 06)
        headerData = s.read('hex:72') 
        # READ the NEXT 1 BYTE (8 bits) -- a.k.a. length of following message
        msgDataLength = s.read('intle:8')
        # SKIP the NEXT 1 BYTE (8 bits) -- should always be '00' for all valid entries
        skipData = s.read('hex:8')
        # READ the NEXT n BYTES (8bits*n-bytes)
        try: # skip entry if error is thrown
            MSG_DATA = s.read(8*msgDataLength).tobytes().decode()
        except UnicodeDecodeError:
            continue
        # SKIP the NEXT 17 BYTES (136 bits)
        skipData = s.read('hex:136')
        # READ the NEXT 2 BYTES (16 bits) -- a.k.a. the msgNumberHeader, if not valid, then skip
        skipData = s.read('hex:16')
        if str(skipData) != msgNumberHeader:
            continue
        # READ THE NEXT 10 BYTES (80 bits) -- a.k.a. the mobile phone number assoc. with SMS message 
        try: 
            MOBILE_SENDER = s.read(80).tobytes().decode()
            MOBILE_SENDER = int(MOBILE_SENDER) # test value for invalid data characters
        except UnicodeDecodeError:
            continue
        except ValueError:
            continue
        finally:
            MOBILE_SENDER = str(MOBILE_SENDER)

        ## Increment found entry with each successful contact parsed 
        totalEntries += 1
        ## PRINT all important SMS information
        print("SMS Message at address: " + str(occuranceOffset) + ", Entry #: " + str(totalEntries))
        print("\t\"" + str(MSG_DATA) + "\"")
        print("\tSender #: " + str(MOBILE_SENDER))

        foundSmsEntries.append([str(totalEntries), MSG_DATA, MOBILE_SENDER, str(occuranceOffset)])
    data2.close()

    ## Write output to csv file
    with open('foundSMSData.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile, dialect=csv.excel)
        for entry in foundSmsEntries:
            writer.writerow(entry)

    return totalEntries