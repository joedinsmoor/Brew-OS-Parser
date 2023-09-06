# Brew OS Parser
Parse BREW (Binary Runtime Environment for Wireless) Platform OS mobile phone image dumps using known hex signatures in Python. In particular, parses *SMS* (message) data *Contact* data from a given mobile BREW image.

# Requires
1. Binary memory image file of a BREW OS phone (extracted using forensics techniques, e.g. chip-off)
2. Python 3 (and a pip installation of [bitstring](https://pypi.org/project/bitstring/) lib module--just run `pip3 install bitstring` first)
# Features
* Incrementally searches memory file for possible contacts and SMS headers
* Shows start memory address for each contact entry or SMS entry found
* Displays each name & phone number for any contact entries
* Displays message data content & associated phone number for any SMS entries
* Writes found contact output to CSV file (shown below)
<img width="552" alt="Screen Shot 2023-08-28 at 11 40 16 AM" src="https://github.com/phoenixrising1800/BrewOSHexParse/assets/44660515/df2607fd-4228-42f6-ae6f-a21245e68417">
* Write found SMS data output to CSV file 

# To-Dos
* Optimize code


