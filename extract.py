import fileinput
import json
sv_dict = { "1011": "reset", "0101": "off", "1110": "on", "0100": "reset", "1010": "off", "0001": "on", "1100": "new adr"}

for line in fileinput.input():
    if "payload" in line:
        js = json.loads(line)
        pl = js["payload"]
        sv = pl[12:16]
        print("Addr: {} SwitchVals: {} Seq: {} ({})".format(pl[0:12], sv, pl[16:24], sv_dict.get(sv, "unk")), flush=True)

