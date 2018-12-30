import string
import re
import fileinput
from collections import namedtuple
digs = string.digits + string.ascii_letters
import png


def read_input():
    return [[int(x)*21 if x != "x" and x != "\n" else 100 for x in input.split(",")]  for input in fileinput.input()]

def main():
    inp = read_input()
    png.from_array(inp, 'L').save("bitdist.png")

main()
