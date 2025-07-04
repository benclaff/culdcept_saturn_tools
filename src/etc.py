from ast import Bytes


def shift_jis2unicode(charcode):
    """
    decode jis to unicode
    ex: print("U+%04X" % shift_jis2unicode(0x8144))
        print("U+%04X" % shift_jis2unicode(0x51))
    :param charcode:
    :return:
    """
    if charcode <= 0xFF:
        shift_jis_string = chr(charcode)
    else:
        shift_jis_string = chr(charcode >> 8) + chr(charcode & 0xFF)

    unicode_string = shift_jis_string.decode('shift-jis')

    assert len(unicode_string) == 1
    return ord(unicode_string)

def is_bit_set(bytes, n):
    """
    test if nth bit is set
    :param num:
    :param pos:
    :return:
    """
    mask = 1 << n
    return (int.from_bytes(bytes) & mask) != 0
