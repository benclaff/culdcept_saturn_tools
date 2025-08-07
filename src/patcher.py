# simple patcher, expects:
# 1) all following files to exists (path relative to GIT directories):
# - translations/scenario_block[x].yaml, with x an integer
# - helpscript/helpscript_block[x].yaml, with x an integer
# 2) following variable to exists (which disc file to patch):
# - meta._DT0
#
# and currently those yaml fields will be used:
# scenario_block_XXX:
#   offsets:
#     end: c0bc3f
#     start: c0bc1a
#   sequence_0:
#     start_relative_to_block: 0
#     end_relative_to_block: 126
#     head_hexa: 180181
#     portrait: 0f3e
#     original_txt: \pよ\nわが
#     translat_txt: It's \p\nMy

import glob
import os
import re
import shutil

import resource

import ruamel.yaml
import yaml
import mmap

from ruamel.yaml import YAML

import meta

try:
    PAGESIZE = resource.getpagesize()
    print("page size is: " + str(PAGESIZE))
except NameError:
    print("page size issue?")
    exit(1)


def overwrite(fileobj, start: int, end: int, newbytes: bytes):
    startoffset, startremainder = divmod(start, PAGESIZE)
    offset = startoffset * PAGESIZE
    endoffset, endremainder = divmod(end, PAGESIZE)
    length = (endoffset + 1) * PAGESIZE - offset
    data = mmap(fileobj.fileno(), offset=offset, length=length)
    data[startremainder:startremainder + end - start] = newbytes


pattern_icon = re.compile(b'x\\[([^\]]+)\\]')

def reverse_control_codes(value):
    value = value.replace('\\p'.encode('shift_jisx0213'), b'\x13\x07')
    #as with use yaml 's ">-" block adds spaces after \n and \w, we ned to remove it
    #before reencoding
    value = value.replace('\\n'.encode('shift_jisx0213'), b'\x0A')
    value = value.replace('\\w'.encode('shift_jisx0213'), b'\x07')
    v = b''
    for m in re.finditer(pattern_icon, value): #retrive icon pointer value(s)
        hex_str = str(m.group(1))[2:-1]  #this line is a bit hacky, may be a better way ?
        v = bytes.fromhex(hex_str)
    if len(v)>0:  # icon pointers present in byte string
        pre = b'\x0e\x04'
        post = b'\x0e\x01'
        new = pre + v + post
        value = re.sub(pattern_icon, new, value)
    return value


def patch_from_yaml_scenario(yaml_file, DT0: mmap):
    with open(yaml_file, 'rb') as ya:
        yaml_data = yaml.safe_load(ya)
        for block in yaml_data:
            print("======== BLOCK: " + block + "\n")
            start = yaml_data[block]["offsets"]["start"]
            end = yaml_data[block]["offsets"]["end"]
            max_size = yaml_data[block]["offsets"]["byte_length"]
            block_data = b''
            for sequence in yaml_data[block]["sequences"]:
                txt = yaml_data[block]["sequences"][sequence]["translat_txt"]
                if (txt is None) or (txt == "null"):  # not translated yet
                    print("Not translated yet !")
                    continue
                # optional head and tails of bytes (function unknown)
                if "head_preportrait_hexa" in yaml_data[block]["sequences"][sequence]:
                    head = bytes.fromhex(yaml_data[block]["sequences"][sequence]["head_preportrait_hexa"])
                    block_data += head
                # portrait
                block_data += bytes.fromhex(yaml_data[block]["sequences"][sequence]["portrait"])
                # optional head and tails of bytes (function unknown)
                if "head_postportrait_hexa" in yaml_data[block]["sequences"][sequence]:
                    head = bytes.fromhex(yaml_data[block]["sequences"][sequence]["head_postportrait_hexa"])
                    block_data += head
                # text itself
                txt = yaml_data[block]["sequences"][sequence]["translat_txt"]
                if (txt is None) or (txt == "null"):  # not translated yet
                    txt = yaml_data[block]["sequences"][sequence]["original_txt"]
                txt = txt.encode('shift_jisx0213')
                txt = reverse_control_codes(txt)
                block_data += txt
                # tail
                if "tail_hexa" in yaml_data[block]["sequences"][sequence]:
                    tail = bytes.fromhex(yaml_data[block]["sequences"][sequence]["tail_hexa"])
                    block_data += tail
            # fill with 0s, for now
            # todo: need to improve with recomputed offset table
            if end - start <= max_size:
                print("len(data): " + str(len(block_data)))
                print("len(original): " + str(end - start))
                print("filler? : " + str((end - start) - len(block_data)))
                DT0[start: start + len(block_data)] = block_data
                ender = b''
                for i in range(start + len(block_data), end):
                    DT0[i:i + 1] = b'\x00'
            else:
                print("block " + block + " : text size > max_size")
            DT0.flush()


def patch_from_yaml_block_with_pointers(yaml_file, DT0: mmap):
    with open(yaml_file, 'rb') as ya:
        yaml_data = yaml.safe_load(ya)
        for block in yaml_data:
            print("======== BLOCK: " + block + "\n")
            start = yaml_data[block]["offsets"]["start"]
            end = yaml_data[block]["offsets"]["end"]
            max_size = yaml_data[block]["offsets"]["byte_length"]
            if yaml_data[block]["sequences"] is None:
                # cases where there is actually no data in block
                # this happens for instance in taunts where offset table point to empty blocks
                # (no text, but x00 to show end of text block)
                continue
            else:
                for sequence in yaml_data[block]["sequences"]:
                    block_data = b''
                    # for text block with pointers, yaml contains 2 fields to shift start/end accordingly
                    # start_relative_to_block ; end_relative_to_block
                    if "start_relative_to_block" in yaml_data[block]["sequences"][sequence]:
                        shifted_start = start + yaml_data[block]["sequences"][sequence]["start_relative_to_block"]
                    else:
                        shifted_start = start
                    if "end_relative_to_block" in yaml_data[block]["sequences"][sequence]:
                        shifted_end = start + yaml_data[block]["sequences"][sequence]["end_relative_to_block"]
                    else:
                        shifted_end = end
                    # optional head and tails of bytes (function unknown)
                    # if "head_preportrait_hexa" in yaml_data[block]["sequences"][sequence]:
                    #     head = bytes.fromhex(yaml_data[block]["sequences"][sequence]["head_preportrait_hexa"])
                    #     block_data += head
                    # portrait
                    block_data += bytes.fromhex(yaml_data[block]["sequences"][sequence]["portrait"])
                    # optional head and tails of bytes (function unknown)
                    # if "head_postportrait_hexa" in yaml_data[block]["sequences"][sequence]:
                    #     head = bytes.fromhex(yaml_data[block]["sequences"][sequence]["head_postportrait_hexa"])
                    #     block_data += head
                    # text itself
                    txt = yaml_data[block]["sequences"][sequence]["translat_txt"]
                    if (txt is None) or (txt == "null"):  # not translated yet
                        print("Not translated yet !")
                        continue
                    txt = txt.encode('shift_jisx0213')
                    txt = reverse_control_codes(txt)
                    block_data += txt
                    # tail
                    # if "tail_hexa" in yaml_data[block]["sequences"][sequence]:
                    #     tail = bytes.fromhex(yaml_data[block]["sequences"][sequence]["tail_hexa"])
                    #     block_data += tail
                    # fill with 0s, for now
                    # todo: need to improve with recomputed offset table
                    if end - start <= max_size:
                        print("len(data): " + str(len(block_data)))
                        print("len(original): " + str(shifted_end - shifted_start))
                        print("filler? : " + str((shifted_end - shifted_start) - len(block_data)))
                        DT0[shifted_start: shifted_start + len(block_data)] = block_data
                        for i in range(shifted_start + len(block_data), shifted_end - 1):
                            DT0[i:i + 1] = b'\x00'
                    else:
                        print("block " + block + " : text size > max_size")
                    DT0.flush()


def patch_from_yaml_cards(yaml_file, DT0: mmap):
    with open(yaml_file, 'rb') as ya:
        yamll = YAML(typ="safe", pure=True)
        yaml_data = yamll.load(ya)
        for block in yaml_data:
            print("======== CARD: " + block + "\n")
            start = yaml_data[block]["offsets"]["start"]
            end = yaml_data[block]["offsets"]["end"]
            max_size = yaml_data[block]["offsets"]["byte_length"]
            block_data = b''
            head = yaml_data[block]["head"]
            block_data += bytes.fromhex(head)
            name = yaml_data[block]["text"]["name"]["translat_txt"]
            if (name is None) or (name == "null"):  # not translated yet
                print("Not translated yet !")
                continue
            name = name.encode('shift_jisx0213')
            name = reverse_control_codes(name)
            block_data += name
            block_data += b'\x00'
            #todo description
            desc = yaml_data[block]["text"]["desc"]["translat_txt"]
            desc = re.sub(r'\\+', r'\\', desc) #avoids case where yaml parser replace \ with \\
            desc = desc.encode('shift_jisx0213')
            desc = reverse_control_codes(desc)
            block_data += desc
            block_data += b'\x00'
            tail = yaml_data[block]["tail"]
            #add tail
            block_data += bytes.fromhex(tail)
            # todo: need to improve with recomputed offset table
            #filler
            block_len = yaml_data[block]["offsets"]["byte_length"]
            text_len_diff = (block_len - len(tail)/2) - len(head)/2 - len(name) -1  - len(desc) -1 #head&tail are str
            if text_len_diff > 0:
                block_data += b'\x00' * int(text_len_diff)
            else:
                print("block " + block + " : text size > max_size")
                exit(1)
            DT0[start: start+len(block_data)] = block_data
            DT0.flush()


###################################################################################
# Script
###################################################################################

# copy iso locally, then edit bytes

OUTPUT_DIR = "../"
PATCHED_DT0 = os.path.join(OUTPUT_DIR, os.path.basename(meta.DT0 + "_patched"))

print("copying from " + meta.DT0 + " to " + PATCHED_DT0)
if not os.path.exists(meta.DT0):
    print("expected file not found: " + meta.DT0)
    exit(1)
try:
    shutil.copy2(meta.DT0, PATCHED_DT0)
except IOError as err:
    print("DTO file copy failed: " + PATCHED_DT0)
    exit(1)

print("patching DT0")
with open(PATCHED_DT0, mode="r+") as file_obj:
    DT0 = mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE)
    ##### scenario script
    block_files = glob.glob('../translations/scenario/scenario_block*.yaml')
    block_files.sort()
    for f in block_files:
        patch_from_yaml_scenario(f, DT0)
    ##### help script
    block_files = glob.glob("../translations/helpscript/helpscript_block*.yaml")
    block_files.sort()
    for f in block_files:
        patch_from_yaml_block_with_pointers(f, DT0)
    ##### taunts
    block_files = glob.glob("../translations/taunts/taunts*_block*.yaml")
    block_files.sort()
    for f in block_files:
        patch_from_yaml_block_with_pointers(f, DT0)
    #### cards
    file = "../translations/cards/cards.yaml"
    patch_from_yaml_cards(file, DT0)
