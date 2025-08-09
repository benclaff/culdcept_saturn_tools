# Shrine effects messages are displayed when passing on the shrine icon (the start of the board game)
# It is located from BB21C8 to BB355C
#
# There is a pointer table:
#   start: BB1C9D
#   end: BB21C7
#   It is structured as 2 offsets, followed by some values, then offset to some control code (for applying an effect ?)
#      05 28 05 2D   05 00 00 00 01 02 00 00 00 17   05 6C   00 00 00 00
#      05 5E 05 65   05 00 00 00 01 02 00 00 00 1F   00 00   00 00 00 00   <== indeed not followed by bytes tail
#      05 98 05 9F   05 00 00 00 01 02 00 00 00 0F   05 D0   00 00 00 00
#      [...]
#      12 D8 12 DD   00 00 00 00 01 01 00 00 00 02   12 FC   00 00 00 00
#      12 F0 12 FF   06 00 00 00 01 07 00 00 00 0E   13 16   00 00 00 00
#      13 0A 13 15   06 00 00 00 01 07 00 00 00 2D   13 3A   00 00 00 00
#      |_offsets 1,2 and 3 are relative to this pos, e.g. each table entry (not 1st position of table)
#      |offset 1 (effect name)
#            |offeset 2 (descirption)
#                                                    |offset 3 (see below)
#
#   For each pointer table entry, the 1st and 2nd pointers go to some effect name, then effect description.
#   The 3rd points to a tail of bytes, until the end of the effect block, which is x0000.
#
#   Text may contain control codes related to icons insertions, as in cards.
#   see exemple of effect "eruption", below :
#
#   95 AC 89 CE 00 <= name
#   82 A0 82 E9 83 47 83 8A 83 41 82 CC |0E 04 81 0E 01| 8C EC 95 84 82 CC 89 BF 92 6C 82 AA 82 50 82 4F 81 93 8F E3 82 AA 82 E9 00
#                                        L> replaced by an icon, as in cards, we find the pattern 0E04[byte]+0E01
#   example above translates into :
#   あるエリアの[icon]護符の価値が１０％上がる
#   The value of [icon] protection in an area is increased by 10%.
#
#   A rapid parsing shows that values possible for icons are those, and should match creature types:
#   0E 04 80 0E 01
#   0E 04 81 0E 01
#   0E 04 82 0E 01
#   0E 04 83 0E 01
#   0E 04 84 0E 01
#
#   Name ends with x00 and description with x00x09, then a tail of variable # of bytes follows.
#   This tail do not seem to match any pointer... can they be shifted  with text if necessary ??
#   Are they even used ? because all table entries are 20 bytes long, part may be zero fillers ?

#   Finally, this tail ends with x00x00 and the next block of effects starts.
#   3rd pointer points to this tail, just after the x00x0X ending the description
#   ex:
#   82E9   00 09   02 00 20 04 01 6E                                                                  00 00 91E4                                                                                                        |letter of next effect name
#   82E9   00 09   01 02 04 0C 40 30 80 00 00 05 00 00 00 08 00 00                                    00 00 8FE1
#   82A4   00 01   64 01 01                                                                           00 00 8AE8
#   82E9   00 02   00 20 00 01 08 04 14 80 00 00 00 00 00 40 05 80 00 00 14 00 00 00 08 00 0F 00 00   00 00 90C2
#   |last kanji of description
#                                                                                                           |kanji of name (next entry)
#
#   Note: 3rd pointer can be null as value x0000 when corresponding effect block do not show a tail !!!

import os
import re
from typing import List, Tuple

import meta

_TABLE_START = "BB1C9D"
_TABLE_END = "BB21C7"
_SHRINE_EFFET_END = "BB3567"

#      05 28 05 2D   05 00 00 00 01 02 00 00 00 17   05 6C   00 00 00 00
#      05 98 05 9F   05 00 00 00 01 02 00 00 00 0F   05 D0   00 00 00 00
#      [...]
#      12 D8 12 DD   00 00 00 00 01 01 00 00 00 02   12 FC   00 00 00 00
#      13 0A 13 15   06 00 00 00 01 07 00 00 00 2D   13 3A   00 00 00 00
pattern_pointer_table = re.compile(b'([\x00-\xFF]{2})([\x00-\xFF]{2})[\x00-\xFF]\x00\x00\x00\x01[\x00-\xFF]\x00\x00\x00[\x00-\xFF]([\x00-\xFF]{2})\x00\x00\x00\x00')
pattern_name = re.compile(b'(?P<name>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+)\\x00')
pattern_desc = re.compile(b'(?P<d1>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])*)(?P<icon>(\\x0E\\x04.+\\x0E\\x01)*)(?P<d2>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+)(\\x0A)*\x00')


def extract_pointer_table_offsets(data: bytes) -> List[Tuple[int,int,int,int]]:
    """
    pointer table returned as a list of offsets tuples,
    tuple=(offset, shift_to_name, shift_to_desc, shift_to_tail]
    :param data:
    :return:
    """
    l = list()
    for m in re.finditer(pattern_pointer_table, data):
        l.append(
            [
                int(_TABLE_START,16)+m.start(1),
                int.from_bytes(m.group(1), byteorder='big', signed=False),
                int.from_bytes(m.group(2), byteorder='big', signed=False),
                int.from_bytes(m.group(3), byteorder='big', signed=False),
            ]
        )
    return l


def entry_to_yaml(data: bytes, offsets: Tuple[int,int,int,int]) -> str:
    """
    extract text from shrine effect entry
    :param data:
    :param offsets:
    :return:
    """
    output_yaml=""
    name = data[0:offsets[2]-offsets[1]-1].decode('shift_jisx0213') # -1 because ends with \x00
    output_yaml += "\n    name: "
    output_yaml += "\n      original_txt: >-\n        " + name
    output_yaml += "\n      ruler_helper: >-\n        ------------"  # todo: determine max char per name line
    output_yaml += "\n      translat_txt: >-\n        null"
    description = data[offsets[2]-offsets[1]:offsets[3]-offsets[1]]
    #description can end with x00 or x0009
    #we set a "spacer" field to differenciate them
    pattern_spacer = re.compile(b'(\x00[\x00-\xFF]*)$')
    spacer_pos=len(description)
    for m in re.finditer(pattern_spacer, description):
        spacer_pos=m.start(1)
    output_yaml += "\n    spacer: " + str(description[spacer_pos:])
    description_txt = (description[0:spacer_pos])
    #todo icon txt replacement via pattern_desc, like in cards
    description_txt = description_txt.decode('shift_jisx0213')
    output_yaml += "\n    description: "
    output_yaml += "\n      original_txt: >-\n        " + description_txt
    output_yaml += "\n      ruler_helper: >-\n        ------------"  # todo: determine max char per card line
    output_yaml += "\n      translat_txt: >-\n        null"
    tail = data[offsets[3]-offsets[1]:]
    output_yaml += "\n  tail: \"" + tail.hex() + "\""  # " to avoid to be parsed as int
    print(output_yaml)

    return output_yaml


os.makedirs("../translations", exist_ok=True)
os.makedirs("../translations/shrineeffect", exist_ok=True)

output_yaml = ""

# open file
with open(meta.DT0, 'rb') as f:
    data = f.read()

    #read pointer table
    pt_data = data[int(_TABLE_START,16):int(_TABLE_END,16)+1]
    l = extract_pointer_table_offsets(pt_data)
    print("\n".join([str(t) for t in l]))

    for i,offset_tuple in enumerate(l):
        # l[1] is offset start, next entry is l[1]+20 (all entries are 20 bytes long)
        start = offset_tuple[0]+offset_tuple[1] #start of name
        if i >= len(l)-1:
            end = int(_SHRINE_EFFET_END,16) +1
        else:
            end = l[i+1][0]+l[i+1][1]#start of next name
        print("shrineeffect_"+str(i))
        #yaml
        output_yaml += "\nshrineeffect_"+str(i)+":"
        output_yaml += "\n  offsets: "
        output_yaml += "\n    byte_length: " + str(end-start)
        output_yaml += "\n    start: " + hex(start)
        output_yaml += "\n    end: " + hex(end)
        subdata = data[start:end]
        output_yaml += entry_to_yaml(subdata,offset_tuple)

print(output_yaml)