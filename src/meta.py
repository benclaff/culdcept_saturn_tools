# YAML config
#################################

import os, yaml
from pathlib import Path

_YAML_PADDING = 4


# saturn specifics
#################################

_MAX_CHAR_PER_DIALOG_LINE = 22
_LINE_RETURN = '\x0A'
_WAIT_INPUT = '\x07'
_END_OF_DIALOG = '\x00'

# extracted iso files
_BIN = ""
DT0 = os.path.join(str(Path.home()), "Dropbox/GAMES/SATURN_CULDCEPT/Culdcept_Extracted/CULDCEPT.DT0")
_DT1 = ""

# shift-JIS
# main intervals
# ASCII        20-7E
# symbols      8140-81AC
# roman-large  824F-829A
# kan1         829F-8396
# euromix      839E-8491
# kan2         889F-9FFC
# kan3         E040-EAA2

# Shift-JIS Encoding
# https://docs.teradata.com/r/Enterprise_IntelliFlex_VMware/International-Character-Set-Support/Japanese-Encodings-and-Mapping-Standards/Shift-JIS-DOS-Kanji-Encoding/Selected-Characters-for-Shift-JIS-Kanji
# Hex Representation of Shift-JIS	Shift-JIS Implementation
# 0x00-0x7E, 0xA1-0xDF	JIS X 0201
# 0x81-0x9F, 0xE0-0xFC	First byte of double-byte representation. Its mapping is as follows:
# 1. 0x81-0x9F--Contains rows 1 to 62 from JIS X 0208.
#
# 2. 0xE0-0xEF--Contains rows 63 to 94 from JIS X 0208.
#
# 3. 0xF0-0xF9--Contains 1,880 Gaiji characters.
#
# 4. 0xFA-0xFC--Contains IBM-defined characters.
#
# 0x40-0x7E, 0x80-0xFC	Second byte of double-byte representation.


_SHIFTJIS_ROMAN_START = "x20"
_SHIFTJIS_ROMAN_END = "x7E"
_SHIFTJIS_KAN_LOW_START = "x8140"
_SHIFTJIS_KAN_LOW_END = "x9FFC"

