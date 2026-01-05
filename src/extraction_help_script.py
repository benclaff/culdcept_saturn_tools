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
#
# There is some pointers inside the text blocks.
# Each of these pointers has this structure:
#     10 FX 02 [variable number of 00] [1-byte index] [2-bytes offset]
# ex: 10 F1 02  00 00 00 00 00 00       02             FA 5F
#
# Below are the pointers including in the "Top" text block,
# reached from offset x06f1 in the Help Script offset table.
#
# This top block contains lots of text AND
# includes many pointers that target subblocks of texts.
# if following them, there are even some loops.
# this seems to correspond to menu text behaviours.
#
# Not that the example offset is FA5F, this is actually a negative offset: FA5F-FFFF = -5A0
# Relatively to the position of FA, indeed this points to the start of a text block.
# (-1 shift, compared to FA position)
#
#                              |XX XX| <<= offset to sub-block
# 10 F1 02 00 00 00          02 01 D3
# 10 F1 02 00 00 00 00 00 00 01 02 83
# 10 F1 02 00 00 00 00 00 00 03 02 F9
# 10 F1 02 00 00 00 00 00 00 04 02 ED
# 10 F1 02 00 00 00 00 00 00 05 03 1A
# 10 F1 02 00 00 00 00 00 00 08 05 4B
# 10 F1 02 00 00 00 00 00 00 06 03 E3
# 10 F1 02 00 00 00 00 00 00 07 04 EF
# [next, isolated between texts]
# 10 F0 02 00 00 00 00 00 00 01 03 E3 *B
# 10 F0 02 00 00 00 00       01 03 27
# 10 F0 02 00 00 00          01 03 03
# 10 F0 02 00 00 00 00       01 01 8B
# 10 F0 02 00 00 00 00 00    01 00 73
# 10 F0 02 00 00 00          01 00 2F
# 10 F0 02 00 00 00 00       01 00 03  *C
# 10 F1 02 00 00 00 00 00 00 00 F8 91 <<= F891-FFFF=-76E or  FFFF xor F891 => start of 1st big block at -1
# 10 F1 02 00 00 00 00 00 00 02 FA 5F <<= FA5F-FFFF=-5AO => start of some text at -1, after *B
# 10 F0 02 00 00 00 00 00    01 FD BF <<= FDBF-FFFF=-240 => start of some text at -1, after *C
# [big block again]
# 10 F1 02 00 00 00 00 00 00 01 00 A5
# 10 F1 02 00 00 00 00 00 00 03 00 DF
# 10 F1 02 00 00 00 00 00 00 04 00 D3
# 10 F1 02 00 00 00 00 00 00 05 00 81
# 10 F1 02 00 00 00 00 00 00 08 00 75
# 10 F1 02 00 00 00 00 00 00 06 00 69
# 10 F1 02 00 00 00 00 00 00 07 00 5D
# [last one isolated]
# 10 F0 02 00 00 00 00 00 00 01 FC 17 <<= FC17-FFFF=-3E8 => start of some text at -1, after *C
#
# Extracting all text block is as a consequence a matter of
# 1) parsing the offset table to reach each top text block
# 2) then extract all pointers from each top block, to reach more text sub-blocks.
#
# To do so, we get a list of table offset, then parse each top block to seek
# more sublock using pointers. We obtain a list of start / stop of all text blocks.
#
# Note : There are sometimes tail bytes after the text of the text block.
# Does this trigger something ? See at C12AA4 ==> (need to be confirmed in-game)


import os
import extraction
import meta

_TABLE_START = "C11C50"
_TABLE_END = "C11C83"
_HELP_SCRIPT_END = "C13583"

####################################################################

# open saturn file
with open(meta.DT0, 'rb') as f:
    data = f.read()

counter = 0
output_yaml = ""

#get all offsets from table
table_offsets = extraction.extract_blocks_from_offset_table(data, _TABLE_START, _TABLE_END)

#get more offsets from pointers
new_offsets = extraction.extract_blocks_from_pointers(data, table_offsets, _TABLE_START)

print("# text blocks found: "+str(len(table_offsets.keys())))
print("# supplementary blocks after pointer extraction: "+str(len(new_offsets.keys())))

# generate yaml using sorted offsets
table_offsets.update(new_offsets)
sorted_offsets = dict(sorted(new_offsets.items()))

os.makedirs("../translations", exist_ok=True)
os.makedirs("../translations/helpscript", exist_ok=True)

extraction.generate_yaml_per_block(
    data,
    sorted_offsets,
    _HELP_SCRIPT_END,
    "../translations/helpscript/helpscript"
)

