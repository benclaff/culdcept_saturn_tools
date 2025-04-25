import yaml
from yaml.loader import SafeLoader

print("Testing scenario translation integrity")
data = dict()
with open("translations/scenario.yaml") as stream:
    try:
        data = yaml.load(stream, Loader=SafeLoader)
        print("Loaded #blocks: " + str(len(data.keys())))

    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

for block, val in data.items():
    byte_length_expected = val['offsets']['byte_length']
    bytes_original = str(val['text']['original']).encode('shift_jisx0213')
    bytes_original = bytes_original.replace("#PN#".encode('shift_jisx0213'), b'\x13\x07', )
    bytes_original = bytes_original.replace('#0A#'.encode('shift_jisx0213'), b'\x0A')
    bytes_original = bytes_original.replace('#07#'.encode('shift_jisx0213'), b'\x07')
    bytes_translated = str(val['text']['translated']).encode('shift_jisx0213')
    bytes_translated = bytes_translated.replace("#PN#".encode('shift_jisx0213'), b'\x13\x07', )
    bytes_translated = bytes_translated.replace('#0A#'.encode('shift_jisx0213'), b'\x0A')
    bytes_translated = bytes_translated.replace('#07#'.encode('shift_jisx0213'), b'\x07')
    if byte_length_expected < len(bytes_translated):
        print("##### Translation in block "+block+" does not respect max byte length condition.")
        print("Original           : "+str(bytes_original))
        print("Translation text   : "+str(bytes_translated))
        print("Translation bytes  : " + str([hex(i) for i in bytes_translated]).replace(" ",""))
        print("Maximum byte length: "+str(byte_length_expected))
        print("Current byte length: " + str(len(bytes_translated)))
        exit(1)

exit(0)
