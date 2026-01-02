# Tutorial data follows the same bytes and pointers patterns than the help script.
# We will reuse the same functions
#
# file : CULDCEPT.DT0
import os

import extraction
import meta

_TABLE_START = "B609B8"
_TABLE_END = "B609F6"
_TUTORIAL_SCRIPT_END = "B61EA4"

#todo: second table here ?
# 11930102 [B609F6h]
# 11930154 [B60A2Ah]

####################################################################12

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
os.makedirs("../translations/tutorial", exist_ok=True)

extraction.generate_yaml_per_block(
    data,
    sorted_offsets,
    _TUTORIAL_SCRIPT_END,
    "../translations/tutorial/tutorial"
)
