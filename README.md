# BrewOSHexParse
Parse BREW OS phone image dump using hex in Python
# Requires
1. Binary memory image file of a BREW OS phone (extracted using forensics techniques, e.g. chip-off)
2. Python 3 (and a pip installation of [bitstring](https://pypi.org/project/bitstring/) lib module--just run `pip3 install bitstring` first)
# Features
* Incrementally searches memory file for possible contact headers
* Shows start memory address for each contact entry found
* Displays each name & phone number for any contact entries 
