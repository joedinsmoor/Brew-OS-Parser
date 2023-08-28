# BrewOSHexParse
Parse BREW OS phone image dump using known hex signatures in Python
# Requires
1. Binary memory image file of a BREW OS phone (extracted using forensics techniques, e.g. chip-off)
2. Python 3 (and a pip installation of [bitstring](https://pypi.org/project/bitstring/) lib module--just run `pip3 install bitstring` first)
# Features
* Incrementally searches memory file for possible contact headers
* Shows start memory address for each contact entry found
* Displays each name & phone number for any contact entries
* Writes found contact output to CSV file (shown below)
<img width="552" alt="Screen Shot 2023-08-28 at 11 40 16 AM" src="https://github.com/phoenixrising1800/BrewOSHexParse/assets/44660515/df2607fd-4228-42f6-ae6f-a21245e68417">

# To-Dos
* Optimize code
* (Maybe) Parse data for text messages

