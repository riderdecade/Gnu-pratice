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

    def __init__(self, Num_Samples_To_Count=128):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Select Control sink',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.Num_Samples_To_Count = Num_Samples_To_Count
        self.portName = 'messageOutput'
        self.message_port_register_out(pmt.intern(self.portName))
        self.state = 0
        self.counter = 0
        self.frequency_list = [0, 2420e6, 2440e6, 0, 2500e6]
        self.gain_list = [20, 30, 40, 50, 60]

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        self.counter = self.counter + len(output_items[0])
        if (self.counter > self.Num_Samples_To_Count):
            now_gain=self.gain_list[self.state]
            now_freq=self.frequency_list[self.state]
            # command
            command = pmt.make_dict()
            command = pmt.dict_add(command, pmt.to_pmt("freq"), pmt.from_double(now_freq))
            command = pmt.dict_add(command, pmt.to_pmt("gain"), pmt.from_double(now_gain))

            PMT_msg = pmt.from_double(self.frequency_list[self.state])
            # PASS
            self.message_port_pub(pmt.intern(self.portName), command)
            
            self.state = (self.state + 1) % 5
            self.counter = 0
        output_items[0][:]=input_items[0]
        return len(output_items[0])

