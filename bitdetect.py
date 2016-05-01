#!/usr/bin/env python
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fromfile_demod import top_block, data_to_str
from glob import glob
from random import shuffle
import re


def bit_slice(input, rate=5):
    output = ""
    sample = input[0:rate]
    i = 0

    while sample:
        if find_phase_change(sample) == -1:
            output += sample[0]
        i += rate
        sample = input[i:i + rate] 

    return output

def find_phase_change(input, reversed=False):
    for i in range(len(input) - 1, 0, -1) if reversed else range(0, len(input) - 1):
        bit = input[i]
        nextbit = input[i - 1] if reversed else input[i + 1]
        if bit != nextbit:
            return i 
    return -1

class test_slice(gr_unittest.TestCase):
    def test_process_sample(self):
        input = "110101"
        self.assertEqual(bit_slice(input, 1), input)
        #self.assertEqual(bit_slice([-1, -1, -1, 1, 1, 1]), 3, [-1, 1])

    def test_find_phase_change(self):
        self.assertEqual(find_phase_change(""), -1)
        self.assertEqual(find_phase_change("1"), -1)
        self.assertEqual(find_phase_change("110101"), 1)
        self.assertEqual(find_phase_change("110101", reversed=True), 5)

if __name__ == '__main__':
    gr_unittest.run(test_slice)

