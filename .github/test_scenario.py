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
    byte_length = val['offsets']['byte_length']
    print(byte_length)
    print(val['text']['original'])
    print(val['text']['translated'])
    bytes_original = str(val['text']['original']).encode('shift_jisx0213')
    bytes_original = bytes_original.replace('#0A#'.encode('shift_jisx0213'), b'\x0A')
    print("to "+str(bytes_original))
    print(len(bytes_original))



exit(0)
