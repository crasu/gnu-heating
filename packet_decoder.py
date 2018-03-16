#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Packet Decoder
# Generated: Fri Mar 16 22:24:32 2018
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
import bitslice
import manchesterpdu
import math
import mqtt
import numpy
import osmosdr
import synctags
import time


class packet_decoder(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Packet Decoder")

        ##################################################
        # Variables
        ##################################################
        self.decimation = decimation = 19
        self.sample_per_sym = sample_per_sym = 95/decimation
        self.samp_rate = samp_rate = 250000
        self.in_frequency = in_frequency = 868.8e6

        ##################################################
        # Blocks
        ##################################################
        self.synctags_fixedlen_tagger_0 = synctags.fixedlen_tagger('syncword', 'packet_len', 48, numpy.byte)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=decimation,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(in_frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.mqtt_mqtt_0 = mqtt.mqtt('192.168.100.60', 1883, '/gnuradio')
        self.manchesterpdu_manchester_pdu_decoder_0 = manchesterpdu.manchester_pdu_decoder()
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, (filter.firdes_low_pass(1.0,samp_rate, 60000, 55000,filter.firdes.WIN_BLACKMAN,6.72)), 115000, samp_rate)
        self.digital_map_bb_0 = digital.map_bb(([48,49]))
        self.digital_correlate_access_code_tag_bb_0 = digital.correlate_access_code_tag_bb('000011000110', 0, 'syncword')
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.bitslice_slicer_0 = bitslice.slicer(5)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-45, 0.001)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate)/(2*math.pi*50000/8.0))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.manchesterpdu_manchester_pdu_decoder_0, 'in'))    
        self.msg_connect((self.manchesterpdu_manchester_pdu_decoder_0, 'out'), (self.mqtt_mqtt_0, 'in'))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.bitslice_slicer_0, 0), (self.digital_correlate_access_code_tag_bb_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.bitslice_slicer_0, 0))    
        self.connect((self.digital_correlate_access_code_tag_bb_0, 0), (self.synctags_fixedlen_tagger_0, 0))    
        self.connect((self.digital_map_bb_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_simple_squelch_cc_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.synctags_fixedlen_tagger_0, 0), (self.digital_map_bb_0, 0))    

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_sample_per_sym(95/self.decimation)

    def get_sample_per_sym(self):
        return self.sample_per_sym

    def set_sample_per_sym(self, sample_per_sym):
        self.sample_per_sym = sample_per_sym

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((filter.firdes_low_pass(1.0,self.samp_rate, 60000, 55000,filter.firdes.WIN_BLACKMAN,6.72)))
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate)/(2*math.pi*50000/8.0))

    def get_in_frequency(self):
        return self.in_frequency

    def set_in_frequency(self, in_frequency):
        self.in_frequency = in_frequency
        self.osmosdr_source_0.set_center_freq(self.in_frequency, 0)


def main(top_block_cls=packet_decoder, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
