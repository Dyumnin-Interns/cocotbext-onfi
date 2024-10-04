import cocotb
from cocotb.triggers import RisingEdge, FallingEdge

class NFCOpcodeDriver:
    def __init__(self, dut, bus, clock):
        self.dut = dut
        self.bus = bus  
        self.clock = clock  

    async def toggle_reset(self):
        # Set iReset to 0 → 1 → 0
        self.dut.iReset.value = 0
        await RisingEdge(self.clock)  # Wait for a clock cycle
        self.dut.iReset.value = 1
        await RisingEdge(self.clock)  # Wait for a clock cycle
        self.dut.iReset.value = 0
        await RisingEdge(self.clock)  # Ensure it remains stable for a cycle

    async def send_opcode(self, opcode):
        # Toggle iReset before sending each opcode
        await self.toggle_reset()

        # Get the signal name for iOpcode from the bus
        iopcode_signal_name = self.bus.get_actual_signal_name("iOpcode")
        iopcode_signal = getattr(self.dut, iopcode_signal_name)

        # Drive the opcode to the signal
        iopcode_signal.value = opcode

        # Wait for a clock edge
        await RisingEdge(self.clock)

        print(f"Opcode {opcode} driven to {iopcode_signal_name}")

