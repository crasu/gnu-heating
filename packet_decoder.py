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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import bitslice
import configparser
import manchesterpdu
import osmosdr
import time
import packet_decoder_epy_block_0 as epy_block_0  # embedded python block
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
        self.variable_qtgui_xlating_filter_width_range = variable_qtgui_xlating_filter_width_range = 200
        self.variable_qtgui_waterfall_update_interval_multiplier = variable_qtgui_waterfall_update_interval_multiplier = 2
        self.variable_qtgui_squelch_threshold_0 = variable_qtgui_squelch_threshold_0 = -44
        self.variable_qtgui_sdr_if_gain_range_0 = variable_qtgui_sdr_if_gain_range_0 = 24
        self.variable_qtgui_sdr_bb_gain_range_0 = variable_qtgui_sdr_bb_gain_range_0 = 42
        self.variable_qtgui_enable_button = variable_qtgui_enable_button = True
        self.samp_rate = samp_rate = 2000000
        self.in_frequency = in_frequency = 868.8e6
        self.center_frequency_0 = center_frequency_0 = 140000
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
        self._variable_qtgui_xlating_filter_width_range_range = Range(0, 500, 1, 200, 200)
        self._variable_qtgui_xlating_filter_width_range_win = RangeWidget(self._variable_qtgui_xlating_filter_width_range_range, self.set_variable_qtgui_xlating_filter_width_range, "Filter Width in khz", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._variable_qtgui_xlating_filter_width_range_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_waterfall_update_interval_multiplier_range = Range(1, 5, 0.5, 2, 200)
        self._variable_qtgui_waterfall_update_interval_multiplier_win = RangeWidget(self._variable_qtgui_waterfall_update_interval_multiplier_range, self.set_variable_qtgui_waterfall_update_interval_multiplier, "FFT  interval multiplier in 1/10*n", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._variable_qtgui_waterfall_update_interval_multiplier_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_squelch_threshold_0_range = Range(-100, -10, 1, -44, 200)
        self._variable_qtgui_squelch_threshold_0_win = RangeWidget(self._variable_qtgui_squelch_threshold_0_range, self.set_variable_qtgui_squelch_threshold_0, "Squelch threshold", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._variable_qtgui_squelch_threshold_0_win, 5, 2, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_sdr_if_gain_range_0_range = Range(0, 40, 8, 24, 200)
        self._variable_qtgui_sdr_if_gain_range_0_win = RangeWidget(self._variable_qtgui_sdr_if_gain_range_0_range, self.set_variable_qtgui_sdr_if_gain_range_0, "IF Gain (lna)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._variable_qtgui_sdr_if_gain_range_0_win, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_sdr_bb_gain_range_0_range = Range(0, 60, 2, 42, 200)
        self._variable_qtgui_sdr_bb_gain_range_0_win = RangeWidget(self._variable_qtgui_sdr_bb_gain_range_0_range, self.set_variable_qtgui_sdr_bb_gain_range_0, "BB Gain (vga)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._variable_qtgui_sdr_bb_gain_range_0_win, 4, 2, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        if bool == bool:
        	self._variable_qtgui_enable_button_choices = {'Pressed': bool(True), 'Released': bool(False)}
        elif bool == str:
        	self._variable_qtgui_enable_button_choices = {'Pressed': "True".replace("'",""), 'Released': "False".replace("'","")}
        else:
        	self._variable_qtgui_enable_button_choices = {'Pressed': True, 'Released': False}

        _variable_qtgui_enable_button_toggle_button = qtgui.ToggleButton(self.set_variable_qtgui_enable_button, 'Run', self._variable_qtgui_enable_button_choices, True,"'value'".replace("'",""))
        _variable_qtgui_enable_button_toggle_button.setColors("default","default","default","default")
        self.variable_qtgui_enable_button = _variable_qtgui_enable_button_toggle_button

        self.top_grid_layout.addWidget(_variable_qtgui_enable_button_toggle_button, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.satellites_fixedlen_tagger_0 = satellites.fixedlen_tagger('syncword', 'packet_len', 48, numpy.byte)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=160,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            in_frequency+center_frequency_0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(1/(10**variable_qtgui_waterfall_update_interval_multiplier))
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 0, 0, 5, 2)
        for r in range(0, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            500, #size
            samp_rate/160, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-10, 10)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(True)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            in_frequency+center_frequency_0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', '', False, False, '1', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_win, 6, 0, 1, 3)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
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
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(0, 0)
        self.osmosdr_source_0.set_if_gain(variable_qtgui_sdr_if_gain_range_0, 0)
        self.osmosdr_source_0.set_bb_gain(variable_qtgui_sdr_bb_gain_range_0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.network_socket_pdu_0 = network.socket_pdu('TCP_SERVER', '', '52001', 10000, False)
        self.manchesterpdu_manchester_pdu_decoder_0 = manchesterpdu.manchester_pdu_decoder(2)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1,  firdes.low_pass(1,samp_rate,variable_qtgui_xlating_filter_width_range*1000/(2*1), 10000), center_frequency_0, samp_rate)
        self.epy_block_0 = epy_block_0.my_sync_block()
        self.digital_map_bb_0 = digital.map_bb([48,49])
        self.digital_correlate_access_code_tag_xx_0 = digital.correlate_access_code_tag_bb('00001100011', 0, 'syncword')
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0.set_enabled(variable_qtgui_enable_button)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.bitslice_slicer_0 = bitslice.slicer(5)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(variable_qtgui_squelch_threshold_0, 0.005)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate)/(2*math.pi*50000/8.0))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.manchesterpdu_manchester_pdu_decoder_0, 'out'), (self.epy_block_0, 'msg_in'))
        self.msg_connect((self.manchesterpdu_manchester_pdu_decoder_0, 'out'), (self.network_socket_pdu_0, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.manchesterpdu_manchester_pdu_decoder_0, 'in'))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.bitslice_slicer_0, 0), (self.digital_correlate_access_code_tag_xx_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.bitslice_slicer_0, 0))
        self.connect((self.digital_correlate_access_code_tag_xx_0, 0), (self.satellites_fixedlen_tagger_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.satellites_fixedlen_tagger_0, 0), (self.digital_map_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "packet_decoder")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_qtgui_xlating_filter_width_range(self):
        return self.variable_qtgui_xlating_filter_width_range

    def set_variable_qtgui_xlating_filter_width_range(self, variable_qtgui_xlating_filter_width_range):
        self.variable_qtgui_xlating_filter_width_range = variable_qtgui_xlating_filter_width_range
        self.freq_xlating_fir_filter_xxx_0_0.set_taps( firdes.low_pass(1,self.samp_rate,self.variable_qtgui_xlating_filter_width_range*1000/(2*1), 10000))

    def get_variable_qtgui_waterfall_update_interval_multiplier(self):
        return self.variable_qtgui_waterfall_update_interval_multiplier

    def set_variable_qtgui_waterfall_update_interval_multiplier(self, variable_qtgui_waterfall_update_interval_multiplier):
        self.variable_qtgui_waterfall_update_interval_multiplier = variable_qtgui_waterfall_update_interval_multiplier
        self.qtgui_waterfall_sink_x_0.set_update_time(1/(10**self.variable_qtgui_waterfall_update_interval_multiplier))

    def get_variable_qtgui_squelch_threshold_0(self):
        return self.variable_qtgui_squelch_threshold_0

    def set_variable_qtgui_squelch_threshold_0(self, variable_qtgui_squelch_threshold_0):
        self.variable_qtgui_squelch_threshold_0 = variable_qtgui_squelch_threshold_0
        self.analog_simple_squelch_cc_0.set_threshold(self.variable_qtgui_squelch_threshold_0)

    def get_variable_qtgui_sdr_if_gain_range_0(self):
        return self.variable_qtgui_sdr_if_gain_range_0

    def set_variable_qtgui_sdr_if_gain_range_0(self, variable_qtgui_sdr_if_gain_range_0):
        self.variable_qtgui_sdr_if_gain_range_0 = variable_qtgui_sdr_if_gain_range_0
        self.osmosdr_source_0.set_if_gain(self.variable_qtgui_sdr_if_gain_range_0, 0)

    def get_variable_qtgui_sdr_bb_gain_range_0(self):
        return self.variable_qtgui_sdr_bb_gain_range_0

    def set_variable_qtgui_sdr_bb_gain_range_0(self, variable_qtgui_sdr_bb_gain_range_0):
        self.variable_qtgui_sdr_bb_gain_range_0 = variable_qtgui_sdr_bb_gain_range_0
        self.osmosdr_source_0.set_bb_gain(self.variable_qtgui_sdr_bb_gain_range_0, 0)

    def get_variable_qtgui_enable_button(self):
        return self.variable_qtgui_enable_button

    def set_variable_qtgui_enable_button(self, variable_qtgui_enable_button):
        self.variable_qtgui_enable_button = variable_qtgui_enable_button
        self.blocks_selector_0.set_enabled(self.variable_qtgui_enable_button)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate)/(2*math.pi*50000/8.0))
        self.freq_xlating_fir_filter_xxx_0_0.set_taps( firdes.low_pass(1,self.samp_rate,self.variable_qtgui_xlating_filter_width_range*1000/(2*1), 10000))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.in_frequency+self.center_frequency_0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate/160)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.in_frequency+self.center_frequency_0, self.samp_rate)

    def get_in_frequency(self):
        return self.in_frequency

    def set_in_frequency(self, in_frequency):
        self.in_frequency = in_frequency
        self.osmosdr_source_0.set_center_freq(self.in_frequency, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.in_frequency+self.center_frequency_0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.in_frequency+self.center_frequency_0, self.samp_rate)

    def get_center_frequency_0(self):
        return self.center_frequency_0

    def set_center_frequency_0(self, center_frequency_0):
        self.center_frequency_0 = center_frequency_0
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.center_frequency_0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.in_frequency+self.center_frequency_0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.in_frequency+self.center_frequency_0, self.samp_rate)

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
