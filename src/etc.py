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

def pretty_dict_siftJIS(d, indent=0):
    """

    :param d:
    :param indent:
    :return:
    """
    for key, value in d.items():
        if isinstance(value, (bytes, bytearray)):
            if key=="portrait":
                value = value.hex(" ", 2)
            else:
                value = value.replace(b'\x13\x07', "[PN]".encode('shift_jisx0213'))
                value = value.replace(b'\x07', '[07]\n'.encode('shift_jisx0213'))
                value = value.replace(b'\x0A', '[0A]\n'.encode('shift_jisx0213'))
                try:
                    value = value.decode('shift_jisx0213', errors='strict')
                except UnicodeError:
                    value = value.hex(" ", 2)
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty_dict_siftJIS(value, indent+1)
        else:
            print('\t' * (indent+1) + str(value))