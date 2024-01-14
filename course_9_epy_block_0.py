"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Multiplexer',   # will show up in GRC
            in_sig=[np.complex64, np.complex64, np.complex64, np.complex64, np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.selectPortName= 'selectPort'
        self.message_port_register_in(pmt.intern(self.selectPortName))
        self.set_msg_handler(pmt.intern(self.selectPortName), self.handle_msg)
        self.selector = 0
    
    def handle_msg(self, msg):
        self.selector = pmt.to_long(msg)
    
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        if(self.selector == 0):
            output_items[0][:] = input_items[0]
        elif(self.selector == 1):
            output_items[0][:] = input_items[1]
        elif(self.selector == 2):
            output_items[0][:] = input_items[2]
        elif(self.selector == 3):
            output_items[0][:] = input_items[3]
        else:
            output_items[0][:] = input_items[4]
        return len(output_items[0])
