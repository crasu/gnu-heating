#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sun May 24 21:43:33 2015
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import math
import sip
import sys
import os

from distutils.version import StrictVersion
class top_block(gr.top_block):

    def __init__(self, filename):
        gr.top_block.__init__(self, "Top Block")


        ##################################################
        # Variables
        ##################################################
        self.sample_per_sym = sample_per_sym = 906
        self.samp_rate = samp_rate = 2500000
        self.filename = filename
        self.points = points = os.path.getsize(filename)/8-10


        ##################################################
        # Blocks
        ##################################################
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
            1, samp_rate, 6000, 500, firdes.WIN_BLACKMAN, 6.76))
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, (filter.firdes_low_pass(1.0,samp_rate, 80000,60000,filter.firdes.WIN_HAMMING,6.72)), 915000, samp_rate)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(sample_per_sym*(1+0.0), 6*0.3*0.3, 0.5, 0.3, 0.1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.1, 2, 0)
        self.blocks_tagged_file_sink_0 = blocks.tagged_file_sink(gr.sizeof_char*1, samp_rate)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, filename, False)
        self.blocks_burst_tagger_0 = blocks.burst_tagger(gr.sizeof_char)
        self.blocks_burst_tagger_0.set_true_tag("burst",True)
        self.blocks_burst_tagger_0.set_false_tag("burst",False)
        	
        self.blocks_abs_xx_0 = blocks.abs_ff(1)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-40, 0.5)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(2*math.pi*50000/8.0))
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 6)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_feedforward_agc_cc_0, 0))    
        self.connect((self.blocks_abs_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_burst_tagger_0, 0), (self.blocks_tagged_file_sink_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.blocks_float_to_short_0, 0), (self.blocks_burst_tagger_0, 1))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_short_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_burst_tagger_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.blocks_abs_xx_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_simple_squelch_cc_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sample_per_sym(self):
        return self.sample_per_sym

    def set_sample_per_sym(self, sample_per_sym):
        self.sample_per_sym = sample_per_sym
        self.digital_clock_recovery_mm_xx_0.set_omega(self.sample_per_sym*(1+0.0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((filter.firdes_low_pass(1.0,self.samp_rate, 80000,60000,filter.firdes.WIN_HAMMING,6.72)))
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*50000/8.0))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 6e3, 1000, firdes.WIN_BLACKMAN, 6.76))

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

if __name__ == '__main__':
    import ctypes
    import sys
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block(sys.argv[1])
    tb.run()
