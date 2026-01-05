# Tutorial data follows the same bytes and pointers patterns than the help script.
# We will reuse the same functions.
#
# Tutorial text shows only one specificity. Some pointers goes to this kind of short block without text :
# 0400 ff61 00
#     |XXXX| <= offset
# No text, but following the offset (here negative) we go back to another pointer of text block.
# They have in common to start with 0400. We keep these pointers untouched.
# (a warning is raised in the log)
#
# file : CULDCEPT.DT0
# Note : There are 6 copies of this text in DT0 file, located at  :
# B609B8
# B69810
# B71F18h
# B7A8B4h
# B82EC8h
# B8B89Ch
# Table AND text (including pointers in text) are identical.
# Translating one of them and injecting into the 6 positions should be enough.
# Below we use location of the 1st copy.

import os

import extraction
import meta

_TABLE_START = "B609B8"
_TABLE_END = "B609F5"
_TUTORIAL_SCRIPT_END = "B61EA4"

#note: there is a strange value 001A in the middle of the table, but it points to the table itself, not a text.
#It's like if the table was split in two by this value, then we need to explore 2 tables.

_TABLE_START_1 = "B609F8"
_TABLE_END_1 = "B60A29"


####################################################################12

# open saturn file
with open(meta.DT0, 'rb') as f:
    data = f.read()

counter = 0
output_yaml = ""

#get all offsets from table
table_offsets = extraction.extract_blocks_from_offset_table(data, _TABLE_START, _TABLE_END)
table_offsets.update(extraction.extract_blocks_from_offset_table(data, _TABLE_START_1, _TABLE_END_1))

#get more offsets from pointers
new_offsets = extraction.extract_blocks_from_pointers(data, table_offsets, _TABLE_START)

print("# text blocks found: "+str(len(table_offsets.keys())))
print("# supplementary blocks after pointer extraction: "+str(len(new_offsets.keys())))

# generate yaml using sorted offsets
table_offsets.update(new_offsets)
sorted_offsets = dict(sorted(new_offsets.items()))

os.makedirs("../translations", exist_ok=True)
os.makedirs("../translations/tutorial", exist_ok=True)

extraction.generate_yaml_per_block(
    data,
    sorted_offsets,
    _TUTORIAL_SCRIPT_END,
    "../translations/tutorial/tutorial"
)
