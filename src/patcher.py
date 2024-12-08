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

import nmap


try:
    PAGESIZE = mmap.PAGESIZE
except NameError:
    PAGESIZE = mmap.ALLOCATION_GRANULARITY

def overwrite(fileobj, start, end, newbytes):
    startoffset, startremainder = divmod(start, PAGESIZE)
    offset = startoffset * PAGESIZE
    endoffset, endremainder = divmod(end, PAGESIZE)
    length = (endoffset + 1) * PAGESIZE - offset
    map = mmap.mmap(fileobj.fileno(), offset=offset, length=length,
                    access=mmap.ACCESS_WRITE)
    map[startremainder:startremainder+end-start] = newbytes