#!/usr/bin/env python
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fromfile_demod import top_block
from glob import glob
from random import shuffle
import re

def data_to_str(data):
    return ''.join(map(str, data))


class test_samples(gr_unittest.TestCase):
    def test_all_dat_sample(self):
        files = glob('samples/[10][10]*.dat*')
        shuffle(files)
        for filename in files:
            self.process_sample(filename)

    def process_sample(self, filename):
        print 'checking sample ' + filename

        tb = top_block(filename)

        sink = blocks.vector_sink_b()
        tb.connect(tb.blocks_burst_tagger_0, sink)    

        tb.run()
        pattern = re.search(r"([01]+)", filename).group()

        self.assertTrue(pattern in data_to_str(sink.data()), 
                msg='pattern from filename {} not contained in gnuradio data {}'.format(filename, data_to_str(sink.data())))

if __name__ == '__main__':
    gr_unittest.run(test_samples)
