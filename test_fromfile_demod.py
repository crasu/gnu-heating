from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fromfile_demod import top_block

def data_to_str(data):
    return ''.join(map(str, data))


class test_samples(gr_unittest.TestCase):
    def test_dat_samples(self):
        tb = top_block('file10_5_4.13421120.dat')

        sink = blocks.vector_sink_b()
        tb.connect(tb.blocks_burst_tagger_0, sink)    

        tb.run()

        self.assertTrue('1010' in data_to_str(sink.data()))

if __name__ == '__main__':
    gr_unittest.run(test_samples)
