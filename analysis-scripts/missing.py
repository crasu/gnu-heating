import string
import re
import fileinput
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

Entry=namedtuple("Entry", ["Adr", "Switch", "Seq", "Cmd"])
def parse(val):
    cmd = val[50::]
    cmd = cmd.replace("\n", "")
    cmd = cmd.replace(")", "")
    return Entry(val[5:17], val[30:34], val[40:48], cmd)

def read_input():
    return [parse(input) for input in fileinput.input()]

def print_tuple(t, ukb):
    line = ",".join(list(t)) + "," + ukb
    print(line)

def get_adr_dict(input):
    return {i.Adr:i for i in input}

def find_bitflip(cur_adr, prev_adr):
    cur_adr = int(cur_adr[8:12], 2)
    prev_adr = int(prev_adr[8:12], 2)
    for i in range(3, -1, -1):
        if (cur_adr ^ prev_adr) & 2**i == 2**i:
            break
    return i

def check_prev(cur, prev):
    # get last four bits of adr
    i = find_bitflip(cur.Adr, prev.Adr)
    # get part of the seq i cannot explain
    cur_seq = int(cur.Seq[4:8], 2)
    prev_seq = int(prev.Seq[4:8], 2)
    if cur_seq & 2**i != prev_seq & 2**i and (prev.Adr[8:12] != "1111" and cur.Adr[8:12] != "0000"):
        print("err change bit from adr not constant in seq bits")
    # all the bits above the constant bit in adr are negated
    low_mask = 2**(i+1)-1
    high_mask = 15 ^ low_mask
    if prev_seq & high_mask ^ cur_seq & high_mask != high_mask:
        print("err seq bits above constant seq bit not negated")

def get_unknown(cur):
    m=re.search(r"^[01]*?(0{1,4})$", cur.Adr)
    if m:
        return cur.Seq[len(cur.Seq)-len(m.group(1))::]
    else:
        return ""


def main():
    input = read_input() 
    adr_dict = get_adr_dict(input)

    prev = None
    for i in range(0,4095):
        i = int2base(i, 2).zfill(12)
        if i in adr_dict:
            if prev:
                check_prev(adr_dict[i], prev)
            ukb = get_unknown(adr_dict[i])
            print_tuple(adr_dict[i], ukb)
            prev = adr_dict[i]
        else:
            print(i)
            prev = None

main()
