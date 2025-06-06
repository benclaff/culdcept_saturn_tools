# Scenario data is organised as follows
#
# file : CULDCEPT.DT0
# text start offset: C0BAB0
# text end offset: C11C4D
#
# There are 2 offset tables, offsets are relative to C0B9C0
# 1. starts at : C0B9C0
# 2. starts at : C0BA38
#
# Text sequence is as follows:
# 1. 0FXX - 0DXX : defines character portrait
# 2. shift-JIS : text
#       13XX : replaced by player name or other names
#       07: new line in same window
#       A0: new window
#       00: ends a dialog sequence, e.g. after the dialog, something is loaded / an event happens.
#
# example:
# [...] 82B5 82E5 82A4 00        | 18 01 83 | 0F0A       89B4 82CC 96BC 82CD [...]
#       end of text sequence A   | unknown  | portrait   start of text sequence B
#
# Sometimes a few bytes are splitting dialog sequences, exact function is unknown for now.
# but they appear more or less when there is a transition between 2 scenario texts, like moving from the
# world map to entering the battlefield.
# They start with x18, followed by a variable number of bytes, some examples:
# 18 00 00 00 00
# 18 01 11
# 18 00 01 0D
# 18 00 01 10
# I let them untouched at same position, in case the last 2 bytes are pointer offsets
import os
import re
from base64 import decode
from typing import Dict, Any

import meta
import yaml
import ruamel.yaml

_TABLE_START = "C0B9C0"
_TABLE_END = "C0BAAF"

# look for this dialog pattern
dialog_sequence_pattern = re.compile(
    b'''
    (?P<head>
        (?P<head_preportrait>\\x18[^\\x0F]+)*
        (?P<portrait>(\\x0F[\\x00-\\xFF])|(\\x0D[\\x00-\\xFF]))
        (?P<head_postportrait>\\x18[^\\x0F-\\xFF]+)*
    )
    (?P<text>
        (?P<line>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+
        [\\x07|\\x0A]*)+
    )+
    (?P<tail>\\x18[^\\x0F]+)*
    ''',
    flags=re.VERBOSE
)

def bytes_to_yaml_text(text_block) -> str:
    yaml_str = ""
    matched = False
    for i,m in enumerate(re.finditer(dialog_sequence_pattern, text_block)):
        matched = True
        match_dic = m.groupdict()
        yaml_str += "\n    sequence_" + str(i) + ":"
        yaml_str += "\n      start_relative_to_block: " + str(m.start())
        yaml_str += "\n      end_relative_to_block: " + str(m.end())
        if match_dic["head"] is not None:
            yaml_str += "\n      head_hexa: \'" + match_dic["head"].hex()+"\'"
        if match_dic["head_preportrait"] is not None:
            yaml_str += "\n      head_preportrait_hexa: \'" + match_dic["head_preportrait"].hex() + "\'"
        if match_dic["head_postportrait"] is not None:
            yaml_str += "\n      head_postportrait_hexa: \'" + match_dic["head_postportrait"].hex() + "\'"
        if match_dic["tail"] is not None:
            yaml_str += "\n      tail_hexa: \'" + match_dic["tail"].hex()+"\'"
        yaml_str += "\n      portrait: \'" + match_dic["portrait"].hex()+"\'"
        dec = match_dic["text"]
        if len(dec)<1:
            print("unexpected text block length <1")
            exit(1)
        dec = dec.replace(b'\x13\x07', "\\p".encode('shift_jisx0213'))
        dec = dec.replace(b'\x0A', '\\n'.encode('shift_jisx0213'))
        dec = dec.replace(b'\x07', '\\w'.encode('shift_jisx0213'))
        # value = value.replace(b'\x00', '[00]'.encode('shift_jisx0213'))
        try:
            dec = dec.decode('shift_jisx0213', errors='strict')
            yaml_str += ("\n      original_txt: >-\n"
                         "        ") + dec
            yaml_str += ("\n      ruler_helper: >-\n"
                         "        -----------------------|-----------------------|-----------------------|")
            yaml_str += ("\n      translat_txt: >-\n"
                         "        null")
        except UnicodeError as ex:
            print(ex)
            exit(1)
    if not matched:
        print("Did not match scenario regexp:")
        print(text_block.hex())
        exit(1)
    return yaml_str

def data_to_yaml(data,i,start,end) -> str:
    text_block = data[start:end]
    offset_yaml_str = "\nscenario_block_" + str(i) + ":"
    offset_yaml_str += "\n  offsets:"
    offset_yaml_str += "\n    byte_length: " + str(len(text_block))
    offset_yaml_str += "\n    start: " + hex(start)
    offset_yaml_str += "\n    end: " + hex(end)
    offset_yaml_str += "\n  sequences: "
    print("data:\t\t\t" + text_block.hex())
    offset_yaml_str += bytes_to_yaml_text(text_block)
    print(offset_yaml_str)
    # write yaml output
    #data_yaml = yaml.safe_load(offset_yaml_str)
    os.makedirs("../translations", exist_ok=True)
    os.makedirs("../translations/scenario", exist_ok=True)
    with open('../translations/scenario/scenario_block' + str(i) + '.yaml', 'w') as file:
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        reload = yaml.load(offset_yaml_str)
        yaml.dump(reload, file)
        # yaml.dump(
        #     data_yaml, file,
        #     default_flow_style=False,
        #     allow_unicode=True,
        #     sort_keys=False
        # )
    return offset_yaml_str

####################################################################


# open saturn file
with open(meta.DT0, 'rb') as f:
    data = f.read()

counter = 0
output_yaml = ""

table_bytes= data[int(_TABLE_START, 16):(int(_TABLE_END, 16) + 1)]

#get all offsets from table
table_offsets = dict()
for i in range(0, len(table_bytes)):
    if i%2==0:
        table_offsets[int(table_bytes[i:i+2].hex(),16)] = table_bytes[i:i+2].hex()
table_offsets = dict(sorted(table_offsets.items()))
print("# text blocks found: "+str(len(table_offsets.keys())))

# get text blocks per offset, convert them to a yaml
prev_offset=0
prev_offset_str="0000"
s = int(_TABLE_START,16)
yaml_str: str = ""
i=0
for offset_int,offset_str in table_offsets.items():
    print("########" + str(i))
    if i>0:
        print("table relative:\t"+prev_offset_str+":"+offset_str)
        start = s + prev_offset
        end = s + offset_int
        print("file relative:\t" + hex(start) + ":" + hex(end))
        yaml_str += data_to_yaml(data,i,start,end)
    prev_offset=offset_int
    prev_offset_str=offset_str
    i+=1

#last block
_SCENARIO_END = "C11C4D"
start = s + prev_offset
end = int(_SCENARIO_END,16)
print("table relative:\t" + prev_offset_str + ":" + offset_str)
print("file relative:\t" + hex(start) + ":" + hex(end))
yaml_str += data_to_yaml(data, i, start, end)


# write yaml output
# data_yaml = yaml.safe_load(yaml_str)
# with open('translations/scenario.yaml', 'w') as file:
#     yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
