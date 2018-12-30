import fileinput
import json
cmd_dict = { "1011": "reset", "0101": "off", "1110": "on", "0100": "reset", "1010": "off", "0001": "on", "1100": "new adr", "0011": "new adr"}

seq_dict = {
    "0001": [13, 5, 1, 9, 7, 15, 3, 11, 12, 4, 0, 8, 10, 2, 6, 14], #off 0-end
    "0101": [13, 5, 1, 9, 7, 15, 3, 11, 12, 4, 0, 8, 10, 2, 6, 14], #off 1-end
    "1010": [14, 6, 2, 10, 8, 0, 4, 12, 11, 3, 15, 7, 9, 1, 5, 13], #on 0-end
    "1110": [14, 6, 2, 10, 8, 0, 4, 12, 11, 3, 15, 7, 9, 1, 5, 13], #on 1-end
    "1011": [None, None, None, None, None, None, None, None, None, None, 0, None, None, None, None, None], #reset 1-end
    "0100": [None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None], #reset 0-end
    "0011": [None, None, None, None, None, None, None, None, None, None, 0, None, None, None, None, None], #new 1-end
    "1100": [None, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None], #new 0-end
}

def lookup_decimal_sequence(command, seq):
    if command in seq_dict:
        slist = seq_dict[command]
        return slist[int(seq, 2)]
    else:
        return None

for line in fileinput.input():
    if "payload" in line:
        js = json.loads(line)
        pl = js["payload"]
        command = pl[12:16]
        seq = pl[16:20]
        chksum = pl[20:24]
        seqd = str(lookup_decimal_sequence(command, seq)).zfill(4)
        print("{} Adr: {} Cmd: {} Seq: {} ({}) Sum: {} ({})".format(seqd, pl[0:12], command, seq, seqd, chksum, cmd_dict.get(command, "unk")), flush=True)
