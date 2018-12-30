import fileinput
import json
import string
import re
from itertools import combinations
from collections import namedtuple
digs = string.digits + string.ascii_letters

def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

'Adr: 000000000110 SwitchVals: 1100 Seq: 01011010 (new adr)\n'
Entry=namedtuple("Entry", ["Adr", "Switch", "Seq", "Cmd"])
def parse(val):
    cmd = val[50::]
    cmd = cmd.replace("\n", "")
    cmd = cmd.replace(")", "")
    return Entry(val[5:17], val[30:35], val[40:49], cmd)

for a, b in combinations(fileinput.input(), 2):
    a=parse(a)
    b=parse(b)
    a_int = int(a.Adr, 2)
    b_int = int(b.Adr, 2)
    diff = a_int ^ b_int
    diff_str = int2base(diff, 2)
    if(a.Adr[11] == b.Adr[11]):
        if(diff_str.count("1") == 2 and re.match(r"10001", diff_str)):
            diff_bits_a = int2base(diff & a_int, 2)
            diff_bits_b = int2base(diff & b_int, 2)
            if(diff_bits_a.count("1") == 1 and diff_bits_b.count("1") == 1): # display only 10000 => 00001 not 00000 10001
                if a.Seq == b.Seq:
                    print("Equal:", a, b)
                else:

