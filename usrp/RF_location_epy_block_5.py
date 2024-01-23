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
            name='Set_sink_center_freq',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.selectPortName= 'get_message'
        self.outPortName= 'sink_message'
        self.message_port_register_in(pmt.intern(self.selectPortName))
        self.message_port_register_out(pmt.intern(self.outPortName))
        self.set_msg_handler(pmt.intern(self.selectPortName), self.handle_msg)
        self.selector = 0
        self.freqency_list = [400e6, 420e6, 440e6, 460e6, 480e6]
        self.now = 0
    
    def handle_msg(self, msg):
        self.selector = pmt.to_long(msg)
    
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        self.now = self.frequency_list[self.selector]
        # set the center frequency of sink
        # 创建一个PMT字典
        command = pmt.make_dict()
        command = pmt.dict_add(command, pmt.intern("freq"), pmt.from_double(self.now))
        command = pmt.dict_add(command, pmt.intern("chan"), pmt.from_long(1))

        # 发送命令消息到输出端口
        self.message_port_pub(pmt.intern(self.outPortName), command)

        return len(output_items[0])
