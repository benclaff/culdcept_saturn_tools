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

os.makedirs("./translations", exist_ok=True)
os.makedirs("./translations/helpscript", exist_ok=True)

extraction.generate_yaml_per_block(
    data,
    sorted_offsets,
    _HELP_SCRIPT_END,
    "./translations/helpscript/helpscript"
)

