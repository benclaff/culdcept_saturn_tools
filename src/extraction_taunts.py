# Taunts are NPC-specific dialogs throwed depending on game events. script data is organised as follows
# Text extraction works similarly to extraction_help_script.py, see corresponding code for more explanations
#
#
# file : CULDCEPT.DT0
#
# Taunts are spread into 12 bytes ranges. Below are the corresponding offset tables.
# There seems to be some placeholder, as some offset tables entry are shifted by 1byte and point only to x00


import os
import re
from typing import Dict

import meta
import ruamel.yaml
from extraction import pointer_offsets_extraction, sequence_to_yaml_text

## below taunt number matched the older DS translation
##
tables = list()
#taunt 00
_TAUNT00_TABLE_START = "B06C58"
_TAUNT00_TABLE_END = "B06CD1"
tables.append([_TAUNT00_TABLE_START, _TAUNT00_TABLE_END])

#taunt 01
_TAUNT01_TABLE_START = "B0F5BC"
_TAUNT01_TABLE_END = "B0F635"
tables.append([_TAUNT01_TABLE_START, _TAUNT01_TABLE_END])

#taunt 02
_TAUNT02_TABLE_START = "B18E00"
_TAUNT02_TABLE_END = "B18E79"
tables.append([_TAUNT02_TABLE_START, _TAUNT02_TABLE_END])

#taunt 03
_TAUNT03_TABLE_START = "B21B18"
_TAUNT03_TABLE_END = "B21B91"
tables.append([_TAUNT03_TABLE_START, _TAUNT03_TABLE_END])

#taunt 04
_TAUNT04_TABLE_START = "B2B07C"
_TAUNT04_TABLE_END = "B2B0F5"
tables.append([_TAUNT04_TABLE_START, _TAUNT04_TABLE_END])

#taunt 05
_TAUNT05_TABLE_START = "B33BCC"
_TAUNT05_TABLE_END = "B33C45"
tables.append([_TAUNT05_TABLE_START, _TAUNT05_TABLE_END])

#taunt 06
_TAUNT06_TABLE_START = "B3D60C"
_TAUNT06_TABLE_END = "B3D685"
tables.append([_TAUNT06_TABLE_START, _TAUNT06_TABLE_END])

#taunt 07
_TAUNT07_TABLE_START = "B46264"
_TAUNT07_TABLE_END = "B462DD"
tables.append([_TAUNT07_TABLE_START, _TAUNT07_TABLE_END])

#taunt 08
_TAUNT08_TABLE_START = "B46264"
_TAUNT08_TABLE_END = "B462DD"
tables.append([_TAUNT08_TABLE_START, _TAUNT08_TABLE_END])

#taunt 09
_TAUNT09_TABLE_START = "B4FA9C"
_TAUNT09_TABLE_END = "B4FB15"
tables.append([_TAUNT09_TABLE_START, _TAUNT09_TABLE_END])

#taunt 10
_TAUNT10_TABLE_START = "B58B04"
_TAUNT10_TABLE_END = "B58B7D"
tables.append([_TAUNT10_TABLE_START, _TAUNT10_TABLE_END])


####################################################################


# open saturn file
with open(meta.DT0, 'rb') as f:
    data = f.read()

output_yaml = ""

for counter,offsets in enumerate(tables):
    print("searching in : "+str(offsets))


    table_bytes= data[int(offsets[0], 16):(int(offsets[1], 16) + 1)]

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
    s = int(offsets[0], 16)
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

            offset_yaml_str = "\ntaunt"+str(counter)+"_block_"+str(i)+":"
            offset_yaml_str += "\n  offsets:"
            offset_yaml_str += "\n    byte_length: "+str(len(text_block))
            offset_yaml_str += "\n    start: "+hex(start)
            offset_yaml_str += "\n    end: "+hex(end)
            offset_yaml_str += "\n  sequences: "
            print("data:\t\t\t"+text_block.hex())
            offset_yaml_str += sequence_to_yaml_text(text_block)
            print(offset_yaml_str)
            os.makedirs("./translations", exist_ok=True)
            os.makedirs("./translations/taunts", exist_ok=True)
            with open('./translations/taunts/taunts'+str(counter)+'_block' + str(i) + '.yaml', 'w') as file:
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
    # _HELP_SCRIPT_END = "C13583"
    #
    # start = prev_offset
    # end = int(_HELP_SCRIPT_END,16)
    # print("file relative:\t"+hex(start)+":"+hex(end))
    # text_block=data[start:end]
    # offset_yaml_str = "\nhelpscript_block_"+str(i)+":"
    # offset_yaml_str += "\n  offsets:"
    # offset_yaml_str += "\n    byte_length: "+str(len(text_block))
    # offset_yaml_str += "\n    start: "+hex(start)
    # offset_yaml_str += "\n    end: "+hex(end)
    # offset_yaml_str += "\n  sequences: "
    # print("data:\t\t\t"+text_block.hex())
    # offset_yaml_str += bytes_to_yaml_text(text_block)
    # print(offset_yaml_str)


    # write yaml output
    #data_yaml = yaml.safe_load(offset_yaml_str)
    # with open('translations/helpscript/helpscript_block'+str(i)+'.yaml', 'w') as file:
    #     #yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
    #     yaml = ruamel.yaml.YAML()
    #     yaml.preserve_quotes = True
    #     reload = yaml.load(offset_yaml_str)
    #     yaml.dump(reload, file)
    # yaml_str += offset_yaml_str