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

def read_input():
    return [input for input in fileinput.input()]

def print_tuple(t):
    print(",".join(list(t)))

def get_adr_dict(input):
    return {i.Adr:i for i in input}

def main():
    input = read_input() 
    adr_dict = get_adr_dict(input)

    for i in range(0,4095):
        i = int2base(i, 2)
        if adr_dict.has_key(i):
            print_tuple(adr_dict[i])
        else:
            print(i)
