"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from gnuradio import uhd
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Set_source_center_freq',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.selectPortName= 'get_message'
        self.outPortName= 'source_message'
        self.message_port_register_in(pmt.intern(self.selectPortName))
        self.message_port_register_out(pmt.intern(self.outPortName))
        self.set_msg_handler(pmt.intern(self.selectPortName), self.handle_msg)
        self.selector = 0
        self.freqency_list=[0, 0, 0, 0, 0]
        self.now_freq = 0
        self.now_gain = 0
        
    def handle_msg(self, msg):
        self.selector = pmt.to_long(msg)
    
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        self.now_freq = self.freqency_list[self.selector]
        self.now_gain = 45
        # set the center frequency of source
        # create PMT
        command = pmt.make_dict()
        command = pmt.dict_add(command, pmt.to_pmt("freq"), pmt.from_double(self.now_freq))
        command = pmt.dict_add(command, pmt.to_pmt("gain"), pmt.from_double(self.now_gain))
        # PASS
        self.message_port_pub(pmt.intern(self.outPortName), command)
             
        return len(output_items[0])

