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

import re
import meta
import yaml

_TABLE_START = "C11C50"
_TABLE_END = "C11C83"

# look for this dialog pattern
dialog_sequence_pattern = re.compile(
    b'(?P<portrait>(\\x0F[\\x00-\\xFF])|(\\x0D[\\x00-\\xFF]))(?P<text>(?P<line>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+[\\x07|\\x0A]*)+)+'
)

# look for this pointer pattern
pointer_pattern = re.compile(
    b'(?P<pointer>(\\x10[\\xF0-\\xF9]\\x02)[\\x00]+(?P<index>[\\x00-\\xFF])(?P<offset>([\\x00-\\FF][\\x00-\\xFF])))'
)
