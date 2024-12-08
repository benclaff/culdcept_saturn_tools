# Scenario data is organised as follows
#
# file : CULDCEPT.DT0
# start offset: C0BAB0
# end offset: C11C4D
#
# table probably starts at : C0B9C1
#
# Text structure is as follows:
# 1. 0FXX - 0DXX : defines character portrait
# 2. shift-JIS : text
#       A0: 13XX : replace by player name or other variable names
#       07: new line in same window
#       A0: new window
#       00: ends a dialog sequence, e.g. after the dialog, something is loaded / an event happens.
#
# sometimes a few bytes saparated dialog sequences, functions is unknow for now.
# example:
# [...] 82B5 82E5 82A4 00 | 18 01 83 | 0F0A     89B4 82CC 96BC 82CD [...]
#       text sequence A   | unknown  | portrait text sequence B
#
import json
import re

import yaml

import meta
from etc import pretty_dict_siftJIS

_OFFSET_START = "C0BAB0"
_OFFSET_END = "C11C4D"
_NEXTLINE = "07"
_NEXTWINDOW = "A0"

# open file
with open(meta._DT0, 'rb') as f:
    data = f.read()

dialog_sequence_pattern = re.compile(
    b'(?P<portrait>\\x0F[\\x00-\\xFF])(?P<block>(?P<line>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+[\\x07|\\x0A]*)+)+'
)
for m in re.finditer(dialog_sequence_pattern, data):
    if int(_OFFSET_START, 16) <= m.start() < int(_OFFSET_END, 16):
        print('x%02x-x%02x: ' % (m.start(), m.end()), bytes.hex(m.group(0), " ", 1))
        print(pretty_dict_siftJIS(m.groupdict(), indent=1))
        # for i in m.groups():
        #     if i == _NEXTLINE or i == _NEXTWINDOW:
        #         print(i.decode('shift_jisx0213'), end='')
        #     else:
        #         print(i.decode('shift_jisx0213'), end='')
