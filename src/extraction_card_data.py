# Card data is organised as follows:
#
# Some card
#                           ST    HP     G  R XX XX 00 XX XX 00              |square                            |=> variable # bytes until next card
# Card 75    00 00 00 00 00 00 00 3C 00 46 00 0D 1A 00 02 52 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 00 00 00 00 00 00 00 00
# Card 79    00 00 00 00 00 00 00 3C 00 5A 02 14 BE 00 13 52 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 29 00 5C 00 00 00 00 00 00 00
# Card 93    00 00 00 00 00 0A 00 32 00 50 01 09 A9 00 02 42 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 4D 00 78 00 12 00 00 00 00 00
# Card 94    00 00 00 00 00 0A 00 28 00 4B 02 13 BE 00 12 12 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 32 00 60 00 26 00 66 00 00 00
# Card 145   00 00 00 00 00 01 00 28 00 3C 02 09 A9 00 06 54 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 00 00 1E 00 00 00 02 00 5C 00 00
# Card 128   00 00 00 00 00 14 00 28 00 3C 02 0F A8 00 04 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 26 00 78 00 00 00 00 00 00 00
# Card 63    00 00 00 00 00 50 00 50 00 64 03 0A 00 00 04 51 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0B 00 60 00 1D 00 00 00 00 00
# Card 101   00 00 00 00 00 0A 00 14 00 19 02 13 A8 00 00 12 00 00 01 00 00 01 00 00 00 00 00 00 00 00 00 00 00 40 00 6C 00 00 00 00 00 00 00
# Card 149   00 00 00 00 00 32 00 32 00 69 01 03 BA 00 08 24 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# Card 105   00 00 00 00 00 14 00 32 00 3C 01 09 A3 00 1A 22 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 00 00 02 00 70 00 00 00
# Card 103   00 00 00 00 00 32 00 32 00 5A 01 03 28 00 1B 22 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# Card 123   00 00 00 00 00 00 00 3C 00 46 00 0D 1A 00 10 53 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 00 00 00 00 00 00 00 00 00
# Card 126   00 00 00 00 00 3C 00 50 00 B4 02 15 A9 00 10 53 00 00 00 02 00 01 00 00 00 00 00 00 00 00 00 00 00 41 00 80 00 43 00 88 00 14
#                                                                         |cost: 風 (wind)
#                                                                      |cost: 森 (forest)
#                                                                   |cost: 水 (water)
#                                                                |cost: 火 (fire)

# Zoom on XX columns, those are boolean for card status or 4bit integers for element and types :
#                                                                                                |bool for limits          0000=無 0   neutral
#                                                                                                |風                        0100=風 4   wind
#                                                                                                  |森                      0011=森 3   forest
#                                                                                                   |水                     0001=火 1   fire
#                                                                                                    |火        |element    0010=水 2   water
#                          ST    HP     G  R XX XX == XX XX ==                                        |無
# Card 75   00 00 00 00 00 00 00 3C 00 46 00 0D 1A 00 02 52 00  0000 1101 0001 1010 0000 0000 0000 0010 0101 0010
# Card 79   00 00 00 00 00 00 00 3C 00 5A 02 14 BE 00 13 52 00  0001 0100 1011 1110 0000 0000 0001 0011 0101 0010
# Card 93   00 00 00 00 00 0A 00 32 00 50 01 09 A9 00 02 42 00  0000 1001 1010 1001 0000 0000 0000 0010 0100 0010
# Card 94   00 00 00 00 00 0A 00 28 00 4B 02 13 BE 00 12 12 00  0001 0011 1011 1110 0000 0000 0001 0010 0001 0010
# Card 145  00 00 00 00 00 01 00 28 00 3C 02 09 A9 00 06 54 00  0000 1001 1010 1001 0000 0000 0000 0110 0101 0100
# Card 128  00 00 00 00 00 14 00 28 00 3C 02 0F A8 00 04 13 00  0000 1111 1010 1000 0000 0000 0000 0100 0001 0011
# Card 63   00 00 00 00 00 50 00 50 00 64 03 0A 00 00 04 51 00  0000 1010 0000 0000 0000 0000 0000 0100 0101 0001
# Card 19   00 00 00 00 00 32 00 3C 00 78 01 03 28 00 00 30 00  0000 0011 0010 1000 0000 0000 0000 0000 0011 0000
# Card 101  00 00 00 00 00 0A 00 14 00 19 02 13 A8 00 00 12 00  0001 0011 1010 1000 0000 0000 0000 0000 0001 0010
# Card 149  00 00 00 00 00 32 00 32 00 69 01 03 BA 00 08 24 00  0000 0011 1011 1010 0000 0000 0000 1000 0010 0100
# Card 105  00 00 00 00 00 14 00 32 00 3C 01 09 A3 00 1A 22 00  0000 1001 1010 0011 0000 0000 0001 1010 0010 0010
# Card 103  00 00 00 00 00 32 00 32 00 5A 01 03 28 00 1B 22 00  0000 0011 0010 1000 0000 0000 0001 1011 0010 0010
# Card 123  00 00 00 00 00 00 00 3C 00 46 00 0D 1A 00 10 53 00  0000 1101 0001 1010 0000 0000 0001 0000 0101 0011
# Card 126  00 00 00 00 00 3C 00 50 00 B4 02 15 A9 00 10 53 00  0001 0101 1010 1001 0000 0000 0001 0000 0101 0011
# Card 95   00 00 00 00 00 14 00 28 00 2D 01 03 28 00 00 32 00  0000 0011 0010 1000 0000 0000 0000 0000 0011 0010
#                                                                                                          |type 0101=不死  5
#                                                                                                                0010=獣    2
#                                                                                                                0001=人    1
#                                                                                                                0100=植物  4
#                                                                                                                0011=竜    3

# This is followed by 2 blocks of text, the card name and the card abilities.
# Both are tailed with byte x00 , which indicates the end of the text item.
# A card without ability description will show x0000
# then follows a variable length bytes run and the next card pattern starts

# also description may contain placeholders for icons
# ex from last card (last in pointer table)
# 83 8F 83 43 83 8B 83 68 83 4F 83 8D 81 5B 83 58 00 93 79 92 6E 82 F0 0E 04 83 0E 01 82 C9 95 CF 89 BB 82 B3 82 B9 82 E9 00
#                                                                     |icon placehold|
# Pattern is 0E 04 XX 0E 01, where XX in [80,84] (the 5 elements)


#!/usr/bin/env python3

# card data offsets
import re
import meta
from extraction import extract_blocks_from_offset_table

_TABLE_START = "BA2E5C"
_TABLE_END = "BA312D"

_OFFSET_START = "BA312E"
_OFFSET_END = "BAC823"

# open file
with open(meta.DT0, 'rb') as f:
    data = f.read()



card_pattern = re.compile(b'\x83\\x8F\\x83\\x43\\x83\\x8B\\x83\\x68\\x83\\x4F\\x83\\x8D\\x81\\x5B\\x83\\x58')
for m in re.finditer(card_pattern, data):
    print('x%02x-x%02x: %s' % (m.start(), m.end(), m.group(0).decode('shift_jisx0213')))

#                           header
#                                     1:ST
#                                                        2:HP
#                                                                            3:G
#                                                                                                4:R
#                                                                                                               5:bools0 : ?
#                                                                                                                              6:bools1 : ?
#                                                                                                                                                  7:bools2 : limits
#                                                                                                                                                                 8:bools3 : types+elements
#                                                                                                                                                                                      9:cost:fire
#                                                                                                                                                                                                     10:cost:water
#                                                                                                                                                                                                                    11:cost:forest
#                                                                                                                                                                                                                                   12:cost:wind
#                                                                                                                                                                                                                                                 13:squares
card_pattern = re.compile(b'\\x00{5}([\\x00-\\xFF])\\x00([\\x01-\\xFF])\\x00([\\x01-\\xFF])\\x00([\\x00-\\x03])([\\x00-\\xFF])([\\x00-\\xFF])\\x00([\\x00-\\xFF])([\\x00-\\xFF])\\x00([\\x00-\\xFF])([\\x00-\\xFF])([\\x00-\\xFF])([\\x00-\\xFF])([\\x00-\\xFF])\\x00{11}')

## search all cards from using offset table
block_offsets = extract_blocks_from_offset_table(data, _TABLE_START, _TABLE_END);

print("Card blocks found from offset table: "+ str(len(block_offsets.keys())))


c=0
for m in re.finditer(card_pattern, data):
    print('x%02x-x%02x: %s\nST:%d HP:%d G:%d R:%d bools0:%02x bools1:%02x bools2:%02x bools3:%02x cost(fire):%d cost(water):%d cost(forest):%d cost(wind):%d squares:%d' % (
            m.start(), m.end(),
            m.group(0), #.decode('shift_jisx0213')
            int.from_bytes(m.group(1), byteorder='little'), #ST
            int.from_bytes(m.group(2), byteorder='little'), #HP
            int.from_bytes(m.group(3), byteorder='little'), #G
            int.from_bytes(m.group(4), byteorder='little'), #R
            int.from_bytes(m.group(5), byteorder='little'), #bools0
            int.from_bytes(m.group(6), byteorder='little'),
            int.from_bytes(m.group(7), byteorder='little'),
            int.from_bytes(m.group(8), byteorder='little'),
            int.from_bytes(m.group(9), byteorder='little'), #cost: fire
            int.from_bytes(m.group(10), byteorder='little'), # water
            int.from_bytes(m.group(11), byteorder='little'), # forest
            int.from_bytes(m.group(12), byteorder='little'), # wind
            int.from_bytes(m.group(13), byteorder='little'), # squares
        )
    )
    c+=1

print("Card blocks found from offset table: "+ str(len(block_offsets.keys())))
print("Card data pattern found using regexp: "+str(c))



