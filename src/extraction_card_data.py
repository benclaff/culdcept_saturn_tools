# Card data is organised as follows:
#
# Some card
#                           ST    HP     G  R XX XX 00 XX XX 00              |square                            |=> vbytes of unkown function, followed by card name and description
# Card 75    00 00 00 00 00 00 00 3C 00 46 00 0D 1A 00 02 52 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 00 00 00 00 00 00 00 00 00
# Card 79    00 00 00 00 00 00 00 3C 00 5A 02 14 BE 00 13 52 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 29 00 5C 00 00 00 00 00 00 00 00
# Card 93    00 00 00 00 00 0A 00 32 00 50 01 09 A9 00 02 42 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 4D 00 78 00 12 00 00 00 00 00 00
# Card 94    00 00 00 00 00 0A 00 28 00 4B 02 13 BE 00 12 12 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 32 00 60 00 26 00 66 00 00 00 00
# Card 145   00 00 00 00 00 01 00 28 00 3C 02 09 A9 00 06 54 00 00 00 00 02 01 00 00 00 00 00 00 00 00 00 00 00 1E 00 00 00 02 00 5C 00 00 00 00
# Card 128   00 00 00 00 00 14 00 28 00 3C 02 0F A8 00 04 13 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 26 00 78 00 00 00 00 00 00 00 00
# Card 63    00 00 00 00 00 50 00 50 00 64 03 0A 00 00 04 51 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0B 00 60 00 1D 00 00 00 00 00 00
# Card 101   00 00 00 00 00 0A 00 14 00 19 02 13 A8 00 00 12 00 00 01 00 00 01 00 00 00 00 00 00 00 00 00 00 00 40 00 6C 00 00 00 00 00 00 00 00
# Card 149   00 00 00 00 00 32 00 32 00 69 01 03 BA 00 08 24 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# Card 105   00 00 00 00 00 14 00 32 00 3C 01 09 A3 00 1A 22 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 00 00 02 00 70 00 00 00 00
# Card 103   00 00 00 00 00 32 00 32 00 5A 01 03 28 00 1B 22 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# Card 123   00 00 00 00 00 00 00 3C 00 46 00 0D 1A 00 10 53 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 12 00 00 00 00 00 00 00 00 00 00
# Card 126   00 00 00 00 00 3C 00 50 00 B4 02 15 A9 00 10 53 00 00 00 02 00 01 00 00 00 00 00 00 00 00 00 00 00 41 00 80 00 43 00 88 00 14 00 00
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



card_name_pattern = re.compile(b"\\x83\\x8F\\x83\\x43\\x83\\x8B"+
                               b"\\x83\\x68\\x83\\x4F\\x83\\x8D\\x81\\x5B\\x83\\x58")
for m in re.finditer(card_name_pattern, data):
    print('x%02x-x%02x: %s' % (m.start(), m.end(), m.group(0).decode('shift_jisx0213')))


# first card blocks extracted from table
# stats:      ST   HP    G  R
# bools:                     XX XX00 XXXX
# costs:                                  00XX XXXX XXXX
# spacer:                                 0000 0000 0000 0000 0000 0000 0000 0000 00 => 11 times
# unkown functions:                                                                 XX 00XX 00XX 00XX 00XX 00XX
# card text:                                                                                                    XXXXXXXXXXXXXX 00  XXXXXXXXXXXXXXXXXXXXX 00
# unknown function:                                                                                                                                          (tail of bytes)
# 0000 0000 003c 0046 00fa 030d a800 0050 0000 0000 0000 0000 0000 0000 0000 0000 0027 0068 0028 0000 0000 0000 836f 8393 8368 838b 834d 8341 0083 5883 4e83 8d81 5b83 8b96 b38c f889 bb81 460a 8358 8379 838b 8d55 8c82 82cc 91ce 8fdb 82c9 82c8 82e7 82c8 82a2 0000 01ff 0164 0000 ffff
# 0000 0000 0014 0014 001e 0213 a900 0010 0000 0000 0000 0000 0000 0000 0000 0000 0026 005c 0000 0000 0000 0000 8341 8393 8356 815b 8393 008d 558c 8282 f096 b38c f889 bb0a 8169 8358 834e 838d 815b 838b 8d55 8c82 8f9c 82ad 816a 0000 01ff 0164 0000 ffff
# 0000 0000 0000 0028 0032 020d a300 0040 0000 0000 0000 0000 0000 0000 0000 0000 0011 0064 0000 0000 0000 0000 8341 8393 836f 815b 8382 8358 0090 ed93 ac92 8681 4183 6583 4283 8983 6d83 5483 4583 8b83 5882 a982 6681 4583 8983 6283 6782 c995 cf90 6700 0164 041e 4007 8000 0001 0000 001b 001e 8000 000e 0000 0000 8000 0013 0000 0000 0000 0101 0000 0100
# 0000 0000 001e 0028 0037 0213 be00 0010 0000 0000 0000 0000 0000 0000 0000 0000 0029 0064 0000 0000 0000 0000 8343 8354 815b 834e 8343 815b 8393 0090 ed93 ac92 8681 4182 6782 6f82 cd91 8a8e e882 cc8e 9d82 c291 5397 cc92 6e82 cc90 9481 7e82 5400 0000 0101 040c 4032 8000 0005 0000 0009 0000 0000 0000
# 0000 0000 0014 0028 0019 0003 ba00 0020 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 8345 838b 8374 0000
# 0000 0000 000a 001e 0041 010e be00 0010 0000 0000 0000 0000 0000 0000 0000 0000 0002 0064 0013 006c 0000 0000 834e 838c 838a 8362 834e 0089 878c ec81 460a 0e04 8c0e 0183 4e83 8a81 5b83 6083 8381 5b82 f091 a68e 800a 8169 8255 824f 8193 816a 0000 0000 013c 0200 0200 0000 01ff 0000
# 0000 0000 0014 001e 000a 000e a800 0010 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 8353 8375 838a 8393 0000 0000
# 0000 0000 0032 0032 0055 000e a800 0010 0000 0000 0000 0000 0000 0000 0000 0000 001e 0000 0000 0000 0000 0000 8354 8343 834e 838d 8376 8358 008c e38e e881 698f ed82 c98c e38d 5582 c982 c882 e981 6a00
# 0000 0000 0032 001e 005a 0100 a800 0010 0000 0000 0000 0000 0000 0000 0000 0000 0002 004c 0000 0000 0000 0000 8354 8380 8389 8343 000e 0488 0e01 82f0 91a6 8e80 8169 8252 824f 8193 816a 0000 011e 0120 0000 2000
# 0000 0000 0014 0028 002d 0006 a800 0010 0000 0000 0000 0000 0000 0000 0000 0000 0009 0000 0000 0000 0000 0000 8356 815b 8374 0083 4183 4383 6583 8082 f08e 6782 c182 c482 a282 c80a 82a9 82c1 82bd 8fea 8d87 8141 91ce 90ed 918a 8ee8 0a82 cc83 4183 4383 6583 8082 f092 4482 a400 0000
# 0000 0000 0028 0014 0028 0104 a900 0050 0000 0000 0000 0000 0000 0000 0000 0000 0022 0060 001d 0000 0000 0000 8356 8346 8343 8368 0090 e690 a781 460a 918a 8ee8 82cc 8272 8273 82f0 8250 815e 8251 82c9 0a82 b782 e981 6989 698b 7681 6a00 0000 0132 0100 0000 0000
# 0000 0000 001e 0028 0032 0014 a300 0020 0000 0000 0000 0000 0000 0000 0000 0000 0002 0054 0000 0000 0000 0000 8266 8145 834e 838d 815b 8389 815b 000e 048b 0e01 82f0 91a6 8e80 8169 8255 824f 8193 816a 0000 0000 0132 0200 0100 0000
# 0000 0000 001e 0014 0014 0003 ba00 0020 0000 0000 0000 0000 0000 0000 0000 0000 0019 0050 0000 0000 0000 0000 8266 8145 8358 836c 815b 834e 000e 0488 898a 0e01 82c9 93c5 82f0 975e 82a6 82e9 0000 0000 0200 00e0 0000 0000
# 0000 0000 000a 001e 0019 0003 a300 0020 0000 0000 0000 0000 0000 0000 0000 0000 0023 0048 0000 0000 0000 0000 8266 8145 8358 8370 8343 835f 815b 000e 0488 890e 0182 f083 7d83 7100 0164 0160 0000 2000
# 0000 0000 0014 000a 0005 0003 a300 0020 0000 0000 0000 0000 0000 0000 0000 0000 001d 0000 0000 0000 0000 0000 8266 8145 8389 8362 8367 0090 e690 a700

#                           header
#                                     1:ST
#                                                        2:HP
#                                                                            3:G
#                                                                                            4:R
#                                                                                                          5:bools0 : ?
#                                                                                                                         6:bools1 : ?
#                                                                                                                                             7:bools2 : limits
#                                                                                                                                                            8:bools3 : types+elements
#                                                                                                                                                                                 9:cost:fire
#                                                                                                                                                                                                10:cost:water
#                                                                                                                                                                                                               11:cost:forest
#                                                                                                                                                                                                                              12:cost:wind
#                                                                                                                                                                                                                                            13:squares
#                                                                                                                                                                                                                                                                      14:unknown0
#                                                                                                                                                                                                                                                                                          15:unknown1
#                                                                                                                                                                                                                                                                                                              16:unknown2
#                                                                                                                                                                                                                                                                                                                                  17:unknown3
#                                                                                                                                                                                                                                                                                                                                                      18:unknown4
#                                                                                                                                                                                                                                                                                                                                                                          19:unknown5
#                                                                                                                                                                                                                                                                                                                                                                                        20:card_name
#                                                                                                                                                                                                                                                                                                                                                                                                           21:card_descirption, it may contain icon injection control code: 0e04 8X0e 01
card_pattern = re.compile(b'\\x00{5}([\\x00-\\xFF])\\x00([\\x00-\\xFF])\\x00([\\x01-\\xFF])([\\x00-\\x03])([\\x00-\\xFF])([\\x00-\\xFF])\\x00([\\x00-\\xFF])([\\x00-\\xFF])\\x00([\\x00-\\xFF])([\\x00-\\xFF])([\\x00-\\xFF])([\\x00-\\xFF])([\\x00-\\xFF])[\\x00]{11}([\\x00-\\xFF])\\x00([\\x00-\\xFF])\\x00([\\x00-\\xFF])\\x00([\\x00-\\xFF])\\x00([\\x00-\\xFF])\\x00([\\x00-\\xFF])(?P<card_name>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+[\\x07|\\x0A]*)+\\x00(?P<card_description>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+[\\x07|\\x0A]*)*\\x00') #.+(?P<card_name>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+)\\x00')

## search all cards from using offset table
block_offsets = extract_blocks_from_offset_table(data, _TABLE_START, _TABLE_END);

print("Card blocks found from offset table: "+ str(len(block_offsets.keys())))

c=0
prev_offset=-1
for i,item in enumerate(block_offsets.items()):
    offset = item[0]
    end = int(_TABLE_START, 16) + offset
    if i>0:
        subdata = data[prev_offset:end]
        print(subdata.hex(' ', 2))
        found=False
        for m in re.finditer(card_pattern, subdata):
            # print('x%02x-x%02x: %s' % (
            #     m.start(), m.end(),
            #     m.group(0).hex(' ',2),
            #     )
            # )
            found=True
            c+=1
        if not found:
            print("CARD PATTERN DID NOT MATCH ! start:"+str(prev_offset)+" end:"+str(end))
    prev_offset=end
#last elt
subdata=data[prev_offset:int(_OFFSET_END,16)]
# TODO


print("Card data pattern found using regexp: " + str(c))


exit()

c=0
for i in range(len(block_offsets.keys())+1):
    if i>0:
        for m in re.finditer(card_pattern, data):
            if m.start() >= int(_OFFSET_START,16) and m.end() <= int(_OFFSET_END,16):
                print('name: %s\n  ST:%d HP:%d G:%d R:%d\n  bools0:%02x bools1:%02x bools2:%02x bools3:%02x\n  cost(fire):%d cost(water):%d cost(forest):%d cost(wind):%d squares:%d' % (

                    m.groupdict()["card_name"].decode('shift_jisx0213'), # card name
                    #m.group(15), #.decode('shift_jisx0213'),  # card description
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



