#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Packet Decoder
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
import math
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
import bitslice
import configparser
import osmosdr
import time
import satellites
import numpy



from gnuradio import qtgui

class packet_decoder(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Packet Decoder", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Packet Decoder")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "packet_decoder")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.decimation = decimation = 19
        self.sample_per_sym = sample_per_sym = 95/decimation
        self.samp_rate = samp_rate = 250000
        self.in_frequency = in_frequency = 868.8e6
        self._MQTT_USER_config = configparser.ConfigParser()
        self._MQTT_USER_config.read('/home/christian/projects/gnu-heating/credentials.config')
        try: MQTT_USER = self._MQTT_USER_config.get('main', MQTT_USER)
        except: MQTT_USER = '0'
        self.MQTT_USER = MQTT_USER
        self._MQTT_PASS_config = configparser.ConfigParser()
        self._MQTT_PASS_config.read('/home/christian/projects/gnu-heating/credentials.config')
        try: MQTT_PASS = self._MQTT_PASS_config.get('main', MQTT_PASS)
        except: MQTT_PASS = '0'
        self.MQTT_PASS = MQTT_PASS

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
        self.network_socket_pdu_0 = network.socket_pdu('TCP_SERVER', 'localhost', '52001', 10000, False)
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
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.network_socket_pdu_0, 'pdus'))
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


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "packet_decoder")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

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

    def get_MQTT_USER(self):
        return self.MQTT_USER

    def set_MQTT_USER(self, MQTT_USER):
        self.MQTT_USER = MQTT_USER
        self._MQTT_USER_config = configparser.ConfigParser()
        self._MQTT_USER_config.read('/home/christian/projects/gnu-heating/credentials.config')
        if not self._MQTT_USER_config.has_section('main'):
        	self._MQTT_USER_config.add_section('main')
        self._MQTT_USER_config.set('main', self.MQTT_USER, str(None))
        self._MQTT_USER_config.write(open('/home/christian/projects/gnu-heating/credentials.config', 'w'))

    def get_MQTT_PASS(self):
        return self.MQTT_PASS

    def set_MQTT_PASS(self, MQTT_PASS):
        self.MQTT_PASS = MQTT_PASS
        self._MQTT_PASS_config = configparser.ConfigParser()
        self._MQTT_PASS_config.read('/home/christian/projects/gnu-heating/credentials.config')
        if not self._MQTT_PASS_config.has_section('main'):
        	self._MQTT_PASS_config.add_section('main')
        self._MQTT_PASS_config.set('main', self.MQTT_PASS, str(None))
        self._MQTT_PASS_config.write(open('/home/christian/projects/gnu-heating/credentials.config', 'w'))




def main(top_block_cls=packet_decoder, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
