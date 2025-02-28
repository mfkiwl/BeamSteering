
#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Mon Nov 25 14:23:16 2013
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time
import sys

class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self)

        parser = OptionParser(option_class=eng_option, usage="%prog: [options] directory")
        parser.add_option("-r", "--rate", type="eng_float", default=25e6,
            metavar="samples/second", help="Sample rate [default=%default]")
        parser.add_option("-b", "--bw", type="eng_float", default=0,
            metavar="Hz", help="Bandwidth [default=%default]")
        parser.add_option("-o", "--offset", type="eng_float", default=0,
            metavar="Hz", help="Local oscillator offset - Hz [default=%default]")
        parser.add_option("-g", "--gain", type="eng_float", default=28                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         ,
            metavar="dB", help="RX front-end gain [default=%default]")
        parser.add_option("-t", "--time", type="eng_float", default=180,
            metavar="sec", help="Length of time to record [default=%default]")
        parser.add_option("-f", "--format", type="string", default="sc16",
            help="File format: {sc16, fc32, ??} [default=%default]")
        parser.add_option("-w", "--wire_format", type="string", default="sc16",
            help="Wire format: {sc8, sc16} [default=%default]")        
        parser.add_option("", "--freq", type="eng_float", default=1.57542e9,
            metavar="Hz", help="Center frequency [default=%default]")
        parser.add_option("-a", "--stream_args", type="string", default="",
            help="Stream arguments [default=%default]") 
        parser.add_option("-c", "--clock_source", type="string", default="gpsdo",
            help="Stream arguments [default=%default]") 

        (options, args) = parser.parse_args()

        if len(args) != 1:
            parser.print_help()
            sys.exit(1)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate =  options.rate
        self.lo_off =  options.offset
        self.freq_l1 =  options.freq
        self.gain = options.gain
        self.record_time = options.time
        self.file_format = options.format
        self.wire_format = options.wire_format
        self.directory = directory = args[0]
        self.bandwidth = options.bw
        self.stream_args = options.stream_args
        self.clock_source = options.clock_source

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            device_addr="",
            stream_args=uhd.stream_args(
                cpu_format=self.file_format,
                otw_format=self.wire_format,
                channels=range(1),
                args=self.stream_args,
            ),
        )

        print("Wire format: " + self.wire_format)
        print("File format: " + self.file_format+"\n")

        print("\nSetting clock source to: " + str(self.clock_source))
        self.uhd_usrp_source_0.set_clock_source(self.clock_source, 0)
        print("Actual clock source: " + self.uhd_usrp_source_0.get_clock_source(0) + "\n")

        print("Setting sample rate to: " + str(self.samp_rate/1e6) + " Msps")
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        print("Actual sample rate: " + str(self.uhd_usrp_source_0.get_samp_rate()/1e6)+" Msps\n")

        print("Setting center freq to: " + str(self.freq_l1/1e6) + " MHz") 
        self.uhd_usrp_source_0.set_center_freq(uhd.tune_request(self.freq_l1, self.lo_off), 0)
        print("Actual center freq: " + str(self.uhd_usrp_source_0.get_center_freq()/1e6) + " MHz\n")

        print("Gain names " + str(self.uhd_usrp_source_0.get_gain_names()))
        print("Gain range " + str(self.uhd_usrp_source_0.get_gain_range()))
        print("Setting gain to: " + str(self.gain) + " dB")
        self.uhd_usrp_source_0.set_gain(self.gain, 0)
        print("Actual gain: " + str(self.uhd_usrp_source_0.get_gain()) + " dB\n")

        print("Possible antennas: " + str(self.uhd_usrp_source_0.get_antennas()))
        print("Setting antenna to: RX2")
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        print("Actual antenna: " + self.uhd_usrp_source_0.get_antenna() + "\n")

        print("Bandwidth range: " + str(self.uhd_usrp_source_0.get_bandwidth_range()))
        print("Setting bandwidth to: " + str(self.bandwidth))
        self.uhd_usrp_source_0.set_bandwidth(self.bandwidth, 0)
        print("Actual bandwidth: " + str(self.uhd_usrp_source_0.get_bandwidth()) + "\n")

        self.filename = directory + "usrp_data_" + str(self.samp_rate/1e6) + "Msps_" + self.file_format + "_" + str(self.gain) + "dB_" +  time.strftime("%Y_%m_%d-%H_%M_%S") + ".bin"

        if self.file_format == "fc32":
            self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*2, self.filename, False)
        else:
            self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*2, self.filename, False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_file_sink_0, 0))

if __name__ == '__main__':
    tb = top_block()
    tb.start()
    print("Recording for " + str(tb.record_time) + " seconds to file:")
    print(tb.filename)

    print("")
    # check gpsdo status
    #print(tb.uhd_usrp_source_0.get_mboard_sensor("lo_locked"))
    print(tb.uhd_usrp_source_0.get_mboard_sensor("gps_locked"))
    print(tb.uhd_usrp_source_0.get_mboard_sensor("gps_time"))
    print(tb.uhd_usrp_source_0.get_mboard_sensor("gps_gpgga"))
    print(tb.uhd_usrp_source_0.get_mboard_sensor("gps_gprmc"))
    print(tb.uhd_usrp_source_0.get_mboard_sensor("ref_locked"))


    time.sleep(tb.record_time)
    tb.stop()
    print("Recording finished.")

