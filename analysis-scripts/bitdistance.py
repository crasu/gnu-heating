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

def print_tuple(t):
    line = ",".join(list(t)) + ","
    print(line, end='')

def get_adr_dict(input):
    return {i.Adr:i for i in input}

def calc_bitdist(i, j):
    a = int(i.Seq, 2)
    b = int(j.Seq, 2)
    diff = a ^ b
    diff_str = int2base(diff, 2)
    return str(diff_str.count("1"))


def main():
    input = read_input() 
    adr_dict = get_adr_dict(input)

    for i in range(0,4095):
        i = int2base(i, 2).zfill(12)
        for j in range(0,4095):
            j = int2base(j, 2).zfill(12)
            if i in adr_dict and j in adr_dict:
                print(calc_bitdist(adr_dict[i], adr_dict[j]) + ",", end='')
            else:
                print("x,", end='')

        print('')

main()
