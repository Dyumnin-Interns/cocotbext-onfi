import cocotb
from cocotb.triggers import RisingEdge

class NFCOpcodeDriver:
    def __init__(self, dut, bus, clock):
        self.dut = dut
        self.bus = bus  
        self.clock = clock  

    async def send_opcode(self, opcode):
        
        iopcode_signal_name = self.bus.get_actual_signal_name("iOpcode")

        
        iopcode_signal = getattr(self.dut, iopcode_signal_name)

      
        iopcode_signal.value = opcode

        
        await RisingEdge(self.clock)
        print(f"Opcode {opcode} driven to {iopcode_signal_name}")



