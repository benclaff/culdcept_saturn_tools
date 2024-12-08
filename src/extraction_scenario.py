# Scenario data is organised as follows
#
# file : CULDCEPT.DT0
# start offset: C0BAB0
# end offset: C11C4D
#
# table probably starts at : C0B9C1
#
# Text sequence is as follows:
# 1. 0FXX - 0DXX : defines character portrait
# 2. shift-JIS : text
#       13XX : replaced by player name or other variable names
#       07: new line in same window
#       A0: new window
#       00: ends a dialog sequence, e.g. after the dialog, something is loaded / an event happens.
#
# sometimes a few bytes are splitting dialog sequences, function is unknown for now.
# for now they should remain untouched.
# example:
# [...] 82B5 82E5 82A4 00        | 18 01 83 | 0F0A       89B4 82CC 96BC 82CD [...]
#       end of text sequence A   | unknown  | portrait   start of text sequence B
#
import re
import meta
import yaml

_OFFSET_START = "C0BAB0"
_OFFSET_END = "C11C4D"


def pretty_block_siftJIS(idx, groupdict, start, end, indent=0, shift=0):
    """

    :param idx: match index
    :param groupdict: match group dictionnary
    :param start: offset
    :param end:  offset
    :param indent: yaml indent
    :return: yaml-formatted
    """
    block_yaml = ""
    block_yaml += "index: " + str(idx) + '\n'
    block_yaml += "offsets:\n" + \
                  ' ' * indent + "start: " + f'{start:x}' + '\n' + \
                  ' ' * indent + "end: " + f'{end:x}' + '\n' + \
                  ' ' * indent + "byte_length: " + str(end - start - 2) + \
                  '\n'
    for key, value in groupdict.items():
        if key == "line":
            continue
        if isinstance(value, (bytes, bytearray)):
            if key == "portrait":
                value = value.hex(" ", 2)
            elif key == "text":

                value = value.replace(b'\x13\x07', "#PN#".encode('shift_jisx0213'))
                value = value.replace(b'\x0A', '#0A#'.encode('shift_jisx0213'))
                value = value.replace(b'\x07', '#07#'.encode('shift_jisx0213'))
                # value = value.replace(b'\x00', '[00]'.encode('shift_jisx0213'))
                try:
                    value = value.decode('shift_jisx0213', errors='strict')
                except UnicodeError as ex:
                    print(ex.with_traceback(ex))
                    exit(1)
        if key == "text":
            block_yaml += str(key) + ":\n"
            block_yaml += ' ' * indent + "windows: " + str(value.count("#0A#") + 1) + '\n'
            block_yaml += ' ' * indent + "original: " + str(value) + '\n'
            block_yaml += ' ' * indent + "translated: " + str(value) + '\n'
        else:
            block_yaml += str(key) + ": "
            block_yaml += str(value) + '\n'

    leftshift = ' ' * shift * indent
    shifted_block = ""
    for line in block_yaml.split('\n'):
        shifted_block += leftshift + line + '\n'

    return shifted_block


# open saturn file
with open(meta._DT0, 'rb') as f:
    data = f.read()

# look for this dialog pattern
dialog_sequence_pattern = re.compile(
    b'(?P<portrait>\\x0F[\\x00-\\xFF])(?P<text>(?P<line>([\\x81-\\x9F\\x13][\\x40-\\xFC\\x07])+[\\x07|\\x0A]*)+)+'
)

counter = 0
output_yaml = ""
for m in re.finditer(dialog_sequence_pattern, data):
    if int(_OFFSET_START, 16) <= m.start() < int(_OFFSET_END, 16):
        # print('%02x-%02x: ' % (m.start(), m.end()), bytes.hex(m.group(0), " ", 1))
        output_yaml += "block_" + str(counter) + ":\n"
        res = pretty_block_siftJIS(counter, m.groupdict(), m.start(), m.end(), indent=2, shift=1)
        output_yaml += res
        print(output_yaml)
        counter += 1
        # for i in m.groups():
        #     if i == _NEXTLINE or i == _NEXTWINDOW:
        #         print(i.decode('shift_jisx0213'), end='')
        #     else:
        #         print(i.decode('shift_jisx0213'), end='')

# write yaml output
data = yaml.safe_load(output_yaml)
with open('translations/scenario.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
