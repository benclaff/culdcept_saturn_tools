# simple patcher, expects:
# 1) all following translation files to exists:
# - translations/scenario.yaml
#
# 2) following variable to exists (which disc file to patch):
# - meta._DT0
#
# and yaml fields to be used:
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
    with open("./translations/scenario_test.yaml", 'rb') as scen:
        scenario_data = yaml.safe_load(scen)
        for block in scenario_data:
            print(str(scenario_data[block]["offsets"]["start"]))
            start = int(scenario_data[block]["offsets"]["start"], 16)
            end = int(scenario_data[block]["offsets"]["end"], 16)
            max_size = int(scenario_data[block]["offsets"]["byte_length"])
            data = b''
            for sequence in block["sequences"]:
                head = bytes.fromhex(scenario_data[block]["sequences"][sequence]["head_hexa"])
                if head is not None:
                    data += head
                data += bytes.fromhex(scenario_data[block]["sequences"][sequence]["portrait"])
                txt = scenario_data[block]["sequences"][sequence]["translat_txt"]
                txt = txt.encode('shift_jisx0213')
                txt = reverse_control_codes(txt)
                data += txt

            if end-start <= max_size:
                DT0[start: start+len(txt)] = txt
            DT0.flush()
