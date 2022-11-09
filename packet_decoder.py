#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Packet Decoder
# GNU Radio version: 3.10.1.1

from gnuradio import analog
import math
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
import bitslice
import manchesterpdu
import mqtt
import osmosdr
import time
import satellites
import numpy




class packet_decoder(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Packet Decoder", catch_exceptions=True)

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
        self.satellites_fixedlen_tagger_0 = satellites.fixedlen_tagger('syncword', 'packet_len', 48, numpy.byte)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=decimation,
                taps=[],
                fractional_bw=0)
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'packet_len')
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ''
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
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
        self.mqtt_mqtt_0 = mqtt.mqtt('192.168.100.60', 1883, '/gnuradio'
        self.manchesterpdu_manchester_pdu_decoder_0 = manchesterpdu.manchester_pdu_decoder()
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, firdes.low_pass(1,samp_rate,samp_rate/(2*1), 55000), 115000, samp_rate)
        self.digital_map_bb_0 = digital.map_bb([48,49])
        self.digital_correlate_access_code_tag_xx_0 = digital.correlate_access_code_tag_bb('000011000110', 0, '')
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.bitslice_slicer_0 = bitslice.slicer(5)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(-50, 0.005)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate)/(2*math.pi*50000/8.0))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.manchesterpdu_manchester_pdu_decoder_0, 'out'), (self.mqtt_mqtt_0, 'in'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.manchesterpdu_manchester_pdu_decoder_0, 'in'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.bitslice_slicer_0, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.bitslice_slicer_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.satellites_fixedlen_tagger_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.satellites_fixedlen_tagger_0, 0), (self.digital_map_bb_0, 0))


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
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate)/(2*math.pi*50000/8.0))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps(firdes.low_pass(1,self.samp_rate,self.samp_rate/(2*1), 55000))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_in_frequency(self):
        return self.in_frequency

    def set_in_frequency(self, in_frequency):
        self.in_frequency = in_frequency
        self.osmosdr_source_0.set_center_freq(self.in_frequency, 0)




def main(top_block_cls=packet_decoder, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
