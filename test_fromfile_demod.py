from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fromfile_demod import top_block

def sink_to_str(sink):
    data = sink.data()
    return ''.join(map(str, data))


class test_samples(gr_unittest.TestCase):
    def setUp (self):
        self.tb = top_block('file10_5_4.13421120.dat')
        self.sink = blocks.vector_sink_b()
        self.tb.connect(self.tb.blocks_burst_tagger_0, self.sink)    

    def tearDown (self):
        self.tb = None

    def test_dat_samples(self):
        self.tb.run()
        self.assertTrue('1010' in sink_to_str(self.sink))

if __name__ == '__main__':
    gr_unittest.run(test_samples)
