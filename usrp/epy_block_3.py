from gnuradio import gr, uhd
import pmt

class blk(gr.sync_block):
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Set_sink_center_freq',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        self.selectPortName= 'get_message'
        self.outPortName= 'sink_message'
        self.message_port_register_in(pmt.intern(self.selectPortName))
        self.message_port_register_out(pmt.intern(self.outPortName))
        self.set_msg_handler(pmt.intern(self.selectPortName), self.handle_msg)
        self.selector = 0
        self.frequency_list = [0, 0, 0, 0, 0]
        self.now = 0
        self.Gain = 45

        # Create USRP Sink block
        self.usrp_sink = uhd.usrp_sink(device_addr="", stream_args=uhd.stream_args(cpu_format="fc32", channels=range(1)))

    def handle_msg(self, msg):
        self.selector = pmt.to_long(msg)
    
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        self.now = self.frequency_list[self.selector]
        self.Gain = 45

        # Set the center frequency and gain of the USRP Sink
        self.usrp_sink.set_center_freq(self.now)
        self.usrp_sink.set_gain(self.Gain)

        # Pass
        self.message_port_pub(pmt.intern(self.outPortName), pmt.PMT_T)

        return len(output_items[0])

