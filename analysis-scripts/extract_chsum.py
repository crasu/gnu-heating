#!/usr/bin/python3
import string
import re
import fileinput
from collections import namedtuple, defaultdict
import operator

Entry=namedtuple("Entry", ["Adr", "Cmd", "RawSeq", "Seq", "Sum", "CmdStr"])

def parse(val):
    cmd_str = val[56::]
    cmd_str = cmd_str.replace("\n", "")
    cmd_str = cmd_str.replace(")", "")
    return Entry(val[5:17], val[23:27], val[33:37], val[39:43], val[50:54], cmd_str)

def read_input():
    return [parse(input) for input in fileinput.input()]

def print_tuple(t):
    line = ",".join(list(t))
    print(line)

def get_key(t):
    key = "-".join([t.Adr, t.Cmd, t.Seq])
    return key

def get_adr_dict(input):
    adr_dict = defaultdict(list)
    for t in input:
        if t.Sum and t.Cmd and t.Seq != "None":
            adr_dict[get_key(t)].append(t)
    return adr_dict

def clean_adr_dict(adr_dict):
    clean = defaultdict(list)
    for k, v in adr_dict.items():
        hist = defaultdict(int)
        for t in v:
            hist[t.Sum]+=1 
        smax = sorted(hist, key=operator.itemgetter(1), reverse=True)[0]
        for t in v:
            if t.Sum == smax:
                clean[get_key(t)].append(t)

    return clean

def get_group_key(t):
    key = "-".join([t.Adr, t.Cmd])
    return key

def group_by_adr_n_cmd(adr_dict):
    group_dict = defaultdict(dict)
    for k, v in adr_dict.items():
        t=v[0]
        group_dict[get_group_key(t)][t.Seq]=t
    return group_dict

def group_by_chksum_key(group_dict):
    for k, g in group_dict.items():
        if len(g) == 16:
            first = g[sorted(list(g))[0]]
            print("-".join([first.Adr[-1], first.Cmd, first.Sum]))
            for e in sorted(list(g)):
                v=g[e]
                print(v.Seq, v.Sum)

def main():
    input = read_input() 
    adr_dict = get_adr_dict(input)
    clean = clean_adr_dict(adr_dict)
    group_dict = group_by_adr_n_cmd(clean)
    group_by_chksum_key(group_dict)

main()
