import os
import re
from typing import *

import ruamel.yaml

# look for this dialog pattern
dialog_sequence_pattern = re.compile(
    b'(?P<portrait>(\\x0F[\\x00-\\xFF])|(\\x0D[\\x00-\\xFF]))(?P<text>(?P<line>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+[\\x07|\\x0A]*)+)+'
)

# look for this pointer pattern
pointer_pattern = re.compile(
    b'(?P<pointer>(\\x10[\\xF0-\\xF9]\\x02)([\\x00]{1,6})(?P<index>[\\x00-\\xFF]{1})(?P<offset>([\\x00-\\xFF]{2})))'
)

def pointer_offsets_extraction(block_start_offset: int, data) -> Dict[int,str]:
    """
    given bytes of a text block, seek for all pointers
    :param block_start_offset:
    :param data:
    :return:
    """
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

def extract_blocks_from_pointers(data:bytes, table_offsets:Dict[int,str], _TABLE_START:str):
    """
    search in each text block defined by offset table for pointers linking to more blocks
    :param data:
    :param table_offsets: block offsets extract from offset table
    :param _TABLE_START: hexa str of 1st position of offest table
    :return:
    """
    prev_offset = 0
    prev_offset_str = "0000"
    s = int(_TABLE_START, 16)
    new_offsets = dict()
    for i, (offset_int, offset_str) in enumerate(table_offsets.items()):
        print("########" + str(i))
        if i > 0:
            print("table relative:\t" + prev_offset_str + ":" + offset_str)
            start = s + prev_offset
            end = s + offset_int
            print("file relative:\t" + hex(start) + ":" + hex(end))
            block = data[start:end]
            new_offsets[start] = hex(start).lstrip("x0")
            # extract pointers from each block
            more_offsets = pointer_offsets_extraction(start, block)
            new_offsets.update(more_offsets)
        prev_offset = offset_int
        prev_offset_str = offset_str
    return  new_offsets


def sequence_to_yaml_text(text_block) -> str:
    """
    given bytes of a text block, return a yaml of all sequences in the block
    """
    if text_block == '\x00':  # it happens that some are empty
        return ""

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
            yaml_str += (("\n      original_txt: >-\n"
                         "        ") +
                         dec.replace("\\n",'\\n\n        ')).replace("\\w",'\\w\n        ')
            #space in preceeding lines are nessary as yaml indentation
            yaml_str += ("\n      ruler_helper: >-\n"
                         "        -----------------------|-----------------------|-----------------------|")
            yaml_str += ("\n      translat_txt: >-\n"
                         "        null")
        except UnicodeError as ex:
            print(ex.with_traceback(ex))
            exit(1)
    return yaml_str

def get_uniq_offsets_from_table(table_bytes:bytes) -> Dict[int,str]:
    """
    using bytes from on offset table, set a dict of all uniq offset, dict[int_offset]=str_hexa_offset
    :param data:
    :return:
    """
    #get all offsets from table
    table_offsets = dict()
    for i in range(0, len(table_bytes)):
        if i%2==0:
            table_offsets[int(table_bytes[i:i+2].hex(),16)] = table_bytes[i:i+2].hex()
    table_offsets = dict(sorted(table_offsets.items()))
    return table_offsets

def extract_blocks_from_offset_table(data:bytes, table_start_offset_hexa_str:str, table_end_offset_hexa_str:str) -> Dict[int,str]:
    """
    given data and start/end offsets of an offset table, get a dict of all offsets
    :param data:
    :param table_start_offset_hexa_str:
    :param table_end_offset_hexa_str:
    :return:
    """
    table_bytes = data[int(table_start_offset_hexa_str, 16):(int(table_end_offset_hexa_str, 16) + 1)]
    return get_uniq_offsets_from_table(table_bytes)

def generate_yaml_per_block(data:bytes, sorted_block_offsets:Dict[int,str], end_offset_hexa:str, output_prefix:str)->bool:
    prev_offset = 0
    prev_offset_str = "0000"
    yaml_str: str = ""
    i = 0
    for offset_int, offset_str in sorted_block_offsets.items():
        print("--------" + str(i))
        if i > 0:
            start = prev_offset
            end = offset_int
            print("file relative:\t" + hex(start) + ":" + hex(end))
            text_block = data[start:end]
            offset_yaml_str = "\nblock_" + str(i) + ":"
            offset_yaml_str += "\n  offsets:"
            offset_yaml_str += "\n    byte_length: " + str(len(text_block))
            offset_yaml_str += "\n    start: " + hex(start)
            offset_yaml_str += "\n    end: " + hex(end)
            offset_yaml_str += "\n  sequences: "
            print("data:\t\t\t" + text_block.hex())
            block = sequence_to_yaml_text(text_block)
            if block == "":
                i += 1
                prev_offset = offset_int
                prev_offset_str = offset_str
                continue
            offset_yaml_str += sequence_to_yaml_text(text_block)
            print(offset_yaml_str)
            # write yaml output
            # data_yaml = yaml.safe_load(offset_yaml_str)
            # with open('translations/helpscript/helpscript_block'+str(i)+'.yaml', 'w') as file:
            #    yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
            with open(output_prefix+'_block' + str(i) + '.yaml', 'w') as file:
                # yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
                yaml = ruamel.yaml.YAML()
                yaml.preserve_quotes = True
                reload = yaml.load(offset_yaml_str)
                yaml.dump(reload, file)
            yaml_str += offset_yaml_str
        i += 1
        prev_offset = offset_int
        prev_offset_str = offset_str

    start = prev_offset
    end = int(end_offset_hexa, 16)
    print("file relative:\t" + hex(start) + ":" + hex(end))
    text_block = data[start:end]
    offset_yaml_str = "\nblock_" + str(i) + ":"
    offset_yaml_str += "\n  offsets:"
    offset_yaml_str += "\n    byte_length: " + str(len(text_block))
    offset_yaml_str += "\n    start: " + hex(start)
    offset_yaml_str += "\n    end: " + hex(end)
    offset_yaml_str += "\n  sequences: "
    print("data:\t\t\t" + text_block.hex())
    offset_yaml_str += sequence_to_yaml_text(text_block)
    print(offset_yaml_str)
    # write yaml output
    # data_yaml = yaml.safe_load(offset_yaml_str)
    with open(output_prefix+'_block' + str(i) + '.yaml', 'w') as file:
        # yaml.dump(data_yaml, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        reload = yaml.load(offset_yaml_str)
        yaml.dump(reload, file)
    yaml_str += offset_yaml_str
    return True



desc_pattern = re.compile(b'(?P<d1>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])*)(?P<icon>(\\x0E\\x04.+\\x0E\\x01)*)(?P<d2>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+)(\\x0A)*[\\x00]*')

def decode_icon_pointers(data: bytes) -> str:
    """
    decode text containing icon pointers (which are 0E04[.+]0E01 bytes)
    :param data:
    :return:
    """
    line_count = 0
    yaml_str = ""
    for m in re.finditer(desc_pattern, data):
        if (line_count > 0):
            yaml_str += '\\n'
        # print("d1:"+m.groupdict()["d1"].hex(' ',2))
        yaml_str += m.groupdict()["d1"].decode('shift_jisx0213')
        # print("d2:"+m.groupdict()["icon"].hex(' ',2))
        icon_bytes = m.groupdict()["icon"]
        if len(icon_bytes) > 0:
            yaml_str += 'x[' + icon_bytes[2:-2].hex() + ']'
        # print("d3:"+m.groupdict()["d2"].hex(' ',2))
        yaml_str += m.groupdict()["d2"].decode('shift_jisx0213')
        line_count = line_count + 1
    return yaml_str