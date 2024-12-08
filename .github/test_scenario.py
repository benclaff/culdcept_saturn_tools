import yaml
from yaml.loader import SafeLoader

print("Testing scenario translation integrity")
data = dict()
with open("translations/scenario.yaml") as stream:
    try:
        data = yaml.load(stream, Loader=SafeLoader)
        print("Blocks: " + str(len(data.keys())))

    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

for block, val in data.items():
    print(block)
    print(val['offsets'])
    byte_length_expected = val['offsets']['byte_length']
    print(val['text']['original'])
    print(val['text']['translated'])
    bytes_original = str(val['text']['original']).encode('shift_jisx0213')
    bytes_original = bytes_original.replace("#PN#".encode('shift_jisx0213'), b'\x13\x07', )
    bytes_original = bytes_original.replace('#0A#'.encode('shift_jisx0213'), b'\x0A')
    bytes_original = bytes_original.replace('#07#'.encode('shift_jisx0213'), b'\x07')
    bytes_translated = str(val['text']['translated']).encode('shift_jisx0213')
    bytes_translated = bytes_translated.replace("#PN#".encode('shift_jisx0213'), b'\x13\x07', )
    bytes_translated = bytes_translated.replace('#0A#'.encode('shift_jisx0213'), b'\x0A')
    bytes_translated = bytes_translated.replace('#07#'.encode('shift_jisx0213'), b'\x07')
    if byte_length_expected != bytes_original != bytes_translated:
        print("Translation in block "+block+" does not respect byte_length condition")
        exit(1)

exit(0)
