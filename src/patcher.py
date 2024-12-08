# simple patcher, expects:
# 1) all following translation files to exists:
# - translations/scenario.yaml
#
# 2) following variable to exists (points to disc data files):
# - meta._DT0
#
# and yaml fields to be used:
# block_XXX:
#   offsets:
#     end: c0bc3f
#     start: c0bc1a
#   portrait: 0f0a
#   text:
#     original: ちょっと待ちな#0A#聞き捨てならないぜ！
#     translated: Hold on.#0A#What do you mean ?!
import os
import shutil

import resource
import yaml
from mmap import mmap

import meta

try:
    PAGESIZE = resource.getpagesize()
except NameError:
    print("page size issue?")
    exit(1)


def overwrite(fileobj, start, end, newbytes):
    startoffset, startremainder = divmod(start, PAGESIZE)
    offset = startoffset * PAGESIZE
    endoffset, endremainder = divmod(end, PAGESIZE)
    length = (endoffset + 1) * PAGESIZE - offset
    data = mmap.mmap(fileobj.fileno(), offset=offset, length=length,
                     access=mmap.ACCESS_WRITE)
    data[startremainder:startremainder + end - start] = newbytes


# copy iso locally, then edit bytes

OUTPUT_DIR = "./"
PATCHED_DT0 = os.path.join(OUTPUT_DIR, os.path.basename(meta.DT0))

print("copying DTO")
shutil.copy2(meta.DT0, PATCHED_DT0)

print("patching DT0")
with open(PATCHED_DT0, 'wb') as out:
    with open("../translations/scenario.yaml", 'rb') as scen:
        scenario_data = yaml.safe_load(scen)
        print(scenario_data)
        for block in scenario_data:
            print(str(scenario_data[block]["offsets"]["start"]))
            if scenario_data[block]["text"]["translated"] is not None:
                overwrite(
                    out,
                    scenario_data[block]["offsets"]["start"],
                    scenario_data[block]["offsets"]["end"],
                    scenario_data[block]["text"]["translated"]
                )
