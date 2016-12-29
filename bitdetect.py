#!/usr/bin/env python
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from glob import glob
from random import shuffle
import re


def bit_slice(input, rate=5):
    output = ""
    i = 0

    while i < len(input):
        sample = input[i:i + rate]
        if len(sample) < rate/2:
            return output

        if sample.count("1") > len(sample)/2:
            output += "1"
        else:
            output += "0"
        
        if len(sample) != rate:
            return output

        i = find_phase_change(input, rate, i)

    return output

def find_phase_change(input, rate, i):
    if input[i + rate/2] == "1":
        char_to_find = "0"
    else:
        char_to_find = "1"
    before_idx = input.rfind(char_to_find, i, i + rate/2)
    after_idx = input.find(char_to_find, i + rate/2, i)

    if before_idx == -1 and after_idx == -1:
        return i + rate
    
    if before_idx == -1:
        return after_idx 

    if after_idx == -1:
        return before_idx + rate

    return before_idx + rate if rate/2 - before_idx > after_idx - rate/2 else after_idx

class test_slice(gr_unittest.TestCase):
    def test_process_sample(self):
        input = "110101"
        self.assertEqual(bit_slice(input, 1), input)
        self.assertEqual(bit_slice("00111100111", 3), "0101")
        self.assertEqual(bit_slice("000111", 3), "01")
        self.assertEqual(bit_slice("00111", 3), "01") # fixme
        self.assertEqual(bit_slice("001111", 3), "01")
        self.assertEqual(bit_slice("001111", 2), "011")
        self.assertEqual(bit_slice("001111", 7), "1")

if __name__ == '__main__':
    gr_unittest.run(test_slice)

