# Help script data is organised as follows
#
# file : CULDCEPT.DT0
# text start offset: C11C84
# text end offset: C13583
#
# There is 1 offset tables, offsets are relative to C11C50
# 1. starts at : C11C50
# 2. starts at : C11C83
#
# Text sequence is as follows:
# 1. 0FXX - 0DXX : defines character portrait
# 2. shift-JIS : text
#       13XX : replaced by player name or other names
#       07: new line in same window
#       A0: new window
#       00: ends a dialog "sequence", e.g. next offset targeted by table will be after this 00
#
# example:
# [...] 82B5 82E5 82A4 00        | 18 01 83 | 0F0A       89B4 82CC 96BC 82CD [...] 00
#       end of text sequence A   | unknown  | portrait   start of text sequence B
#
# There is some pointers inside the text blocks.
# Offset x06F1 is the 1st of the offset table to point to a list of 1 to many consecutive pointers(?).
# Each of these putative pointers has this structure:
#     10 FX 02 [variable number of 00] [1-byte index] [2-bytes offset]
# ex: 10 F1 02  00 00 00 00 00 00       02             FA 5F
#
# Not that the example offset is FXXX, this is acutally a negative offset: FA5F-FFFF = -5A0
# Which relatively to the position preceeding FA, indeed points to the start of a text block.
# (-1 shift, compared to FA position)
#
# Accessing all text block is as a consequence a matter of 1) parsing the offset table, then all pointer with
# computation of the position to which they point to.
#
# There are 2 bytes of unknown function at bytes at C12AA4 ==> text? (need to be confirmed in-game)
import os
import re
from typing import Dict

import meta
import yaml
import ruamel.yaml


_TABLE_START = "C11C50"
_TABLE_END = "C11C83"

# look for this dialog pattern
dialog_sequence_pattern = re.compile(
    b'(?P<portrait>(\\x0F[\\x00-\\xFF])|(\\x0D[\\x00-\\xFF]))(?P<text>(?P<line>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+[\\x07|\\x0A]*)+)+'
)

# look for this pointer pattern
pointer_pattern = re.compile(
    b'(?P<pointer>(\\x10[\\xF0-\\xF9]\\x02)([\\x00]{1,6})(?P<index>[\\x00-\\xFF]{1})(?P<offset>([\\x00-\\xFF]{2})))'
)

def pointer_offsets_extraction(block_start_offset: int, data) -> Dict:
    d = dict()
    for i, m in enumerate(re.finditer(pointer_pattern, data)):
        match_dic = m.groupdict()
        #negative offset
        if match_dic["offset"] > b'\\x0F\\xFF':
            new_block_start_offset = int(match_dic["offset"].hex(),16) - int('FFFF',16) - 1
        #positive offset
        else:
            new_block_start_offset = int.from_bytes(match_dic["offset"])
        new_offset = block_start_offset + m.end() - 2 + new_block_start_offset
        if new_offset < 0 :
            print("offest computation error")
            exit(1)
        d[new_offset] = hex(new_offset).lstrip("0x")
    return d


def bytes_to_yaml_text(text_block) -> str:
    yaml_str = ""
    for i,m in enumerate(re.finditer(dialog_sequence_pattern, text_block)):
        match_dic = m.groupdict()
        yaml_str += "\n    sequence_" + str(i) + ":"
        yaml_str += "\n      start_relative_to_block: " + str(m.start())
        yaml_str += "\n      end_relative_to_block: " + str(m.end()+1)
        # if match_dic["head"] is not None:
        #     yaml_str += "\n      head_hexa: " + match_dic["head"].hex()
        # if match_dic["tail"] is not None:
        #     yaml_str += "\n      tail_hexa: " + match_dic["tail"].hex()
        yaml_str += "\n      portrait: " + match_dic["portrait"].hex()
        dec = match_dic["text"]
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
            print(ex.with_traceback(ex))
            exit(1)
    return yaml_str


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

#get more offsets from pointers
#search in each text block defined by pointer table for pointers
prev_offset=0
prev_offset_str="0000"
s = int(_TABLE_START,16)
yaml_str: str = ""
new_offsets = dict()
for i,(offset_int,offset_str) in enumerate(table_offsets.items()):
    print("########" + str(i))
    if i>0:
        print("table relative:\t"+prev_offset_str+":"+offset_str)
        start = s + prev_offset
        end = s + offset_int
        print("file relative:\t"+hex(start)+":"+hex(end))
        block=data[start:end]
        new_offsets[start] = hex(start).lstrip("x0")
        #extract pointers from each block
        more_offsets = pointer_offsets_extraction(start,block)
        new_offsets.update(more_offsets)
    prev_offset=offset_int
    prev_offset_str=offset_str

print("# text blocks found: "+str(len(table_offsets.keys())))
print("# supplementary blocks after pointer analysis: "+str(len(new_offsets.keys())))

# generate yaml using sorted offsets
sorted_offsets = dict(sorted(new_offsets.items()))
prev_offset=0
prev_offset_str="0000"
yaml_str: str = ""
i=0
for offset_int,offset_str in sorted_offsets.items():
    print("--------" + str(i))
    if i>0:
        start = prev_offset
        end = offset_int
        print("file relative:\t"+hex(start)+":"+hex(end))
        text_block=data[start:end]
        offset_yaml_str = "\nhelpscript_block_"+str(i)+":"
        offset_yaml_str += "\n  offsets:"
        offset_yaml_str += "\n    byte_length: "+str(len(text_block))
        offset_yaml_str += "\n    start: "+hex(start)
        offset_yaml_str += "\n    end: "+hex(end)
        offset_yaml_str += "\n  sequences: "
        print("data:\t\t\t"+text_block.hex())
        offset_yaml_str += bytes_to_yaml_text(text_block)
        print(offset_yaml_str)
        # write yaml output
        #data_yaml = yaml.safe_load(offset_yaml_str)
        #with open('translations/helpscript/helpscript_block'+str(i)+'.yaml', 'w') as file:
        #    yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        os.makedirs("./translations", exist_ok=True)
        os.makedirs("./translations/helpscript", exist_ok=True)
        with open('./translations/helpscript/helpscript_block' + str(i) + '.yaml', 'w') as file:
            # yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
            yaml = ruamel.yaml.YAML()
            yaml.preserve_quotes = True
            reload = yaml.load(offset_yaml_str)
            yaml.dump(reload, file)
        yaml_str += offset_yaml_str
    i+=1
    prev_offset=offset_int
    prev_offset_str=offset_str

#last block
_HELP_SCRIPT_END = "C13583"

start = prev_offset
end = int(_HELP_SCRIPT_END,16)
print("file relative:\t"+hex(start)+":"+hex(end))
text_block=data[start:end]
offset_yaml_str = "\nhelpscript_block_"+str(i)+":"
offset_yaml_str += "\n  offsets:"
offset_yaml_str += "\n    byte_length: "+str(len(text_block))
offset_yaml_str += "\n    start: "+hex(start)
offset_yaml_str += "\n    end: "+hex(end)
offset_yaml_str += "\n  sequences: "
print("data:\t\t\t"+text_block.hex())
offset_yaml_str += bytes_to_yaml_text(text_block)
print(offset_yaml_str)
# write yaml output
#data_yaml = yaml.safe_load(offset_yaml_str)
with open('translations/helpscript/helpscript_block'+str(i)+'.yaml', 'w') as file:
    #yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    reload = yaml.load(offset_yaml_str)
    yaml.dump(reload, file)
yaml_str += offset_yaml_str