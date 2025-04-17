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
import shutil

import resource
import yaml
import mmap

import meta

try:
    PAGESIZE = resource.getpagesize()
    print("page size is: "+str(PAGESIZE))
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

def reverse_control_codes(value):
    value = value.replace('\\p'.encode('shift_jisx0213'), b'\x13\x07')
    value = value.replace('\\n'.encode('shift_jisx0213'), b'\x0A')
    value = value.replace('\\w'.encode('shift_jisx0213'), b'\x07')
    return value

def patch_from_yaml(yaml_file, DT0:mmap):
    with open(yaml_file, 'rb') as ya:
        yaml_data = yaml.safe_load(ya)
        for block in yaml_data:
            print("======== BLOCK: " + block + "\n")
            # start = int(yaml_data[block]["offsets"]["start"], 16)
            start = yaml_data[block]["offsets"]["start"]
            # end = int(yaml_data[block]["offsets"]["end"], 16)
            end = yaml_data[block]["offsets"]["end"]
            max_size = yaml_data[block]["offsets"]["byte_length"]
            data = b''
            for sequence in yaml_data[block]["sequences"]:
                # optional head and tails of bytes (function unknown)
                if "head_hexa" in yaml_data[block]["sequences"][sequence]:
                    head = bytes.fromhex(yaml_data[block]["sequences"][sequence]["head_hexa"])
                    data += head
                # sequence itself
                data += bytes.fromhex(yaml_data[block]["sequences"][sequence]["portrait"])
                txt = yaml_data[block]["sequences"][sequence]["translat_txt"]
                if txt is None:  # not translated yet
                    txt = yaml_data[block]["sequences"][sequence]["original_txt"]
                txt = txt.encode('shift_jisx0213')
                txt = reverse_control_codes(txt)
                data += txt
                # tail
                if "tail_hexa" in yaml_data[block]["sequences"][sequence]:
                    tail = bytes.fromhex(yaml_data[block]["sequences"][sequence]["tail_hexa"])
                    data += tail
            if end - start <= max_size:
                print("len(data): " + str(len(data)))
                print("len(original): " + str(end - start))
                print("filler? : " + str((end - start) - len(data)))
                DT0[start: start + len(txt)] = txt
            else:
                print("block " + block + " : text size > max_size")
            DT0.flush()

###################################################################################
# Script
###################################################################################

# copy iso locally, then edit bytes

OUTPUT_DIR = "./"
PATCHED_DT0 = os.path.join(OUTPUT_DIR, os.path.basename(meta.DT0))

print("copying from " + meta.DT0 + " to " + PATCHED_DT0)
if not os.path.exists(meta.DT0):
    print("expected file not found: "+meta.DT0)
    exit(1)
try:
    shutil.copy2(meta.DT0, PATCHED_DT0)
except IOError as err:
    print("DTO file copy failed: "+PATCHED_DT0)
    exit(1)

print("patching DT0")
with open(PATCHED_DT0, mode="r+") as file_obj:
    DT0 = mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE)
    # scenario script
    block_files = glob.glob('**/../translations/scenario/scenario_block*.yaml')
    for f in block_files:
        patch_from_yaml(f, DT0)
    # help script
    # block_files = glob.glob("**/../translations/helpscript/helpscript_block*.yaml")
