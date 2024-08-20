import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/cocotbext/onfi')))
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from commands import txn, cmds
from bus import Bus
from memory import sigdict

async def generate_clock(dut):
    """Generate clock pulses."""
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())
@cocotb.test()
async def test_bus_signal_expansion(top):
    bus = Bus(top, name="u_nand_controller", signals=sigdict)
    
    
    assert hasattr(bus, "RE_0_n"), "Signal RE_0_n not found"
    assert hasattr(bus, "RE_1_n"), "Signal RE_1_n not found"

  
    assert getattr(bus, "IO0_0") == getattr(bus, "IO0_0") 

    found = False
    for sig_name in dir(bus):
        if sig_name.casefold() == "re_0_n".casefold():
            found = True
            break
    assert found, "Signal re_0_n (case-insensitive) not found"  
    


'''@cocotb.test()
async def test_command_signals(dut):
    await generate_clock(dut)
    await RisingEdge(dut.clk)

    
    signals, unrecognizable_signals = fetch_signals(dut)

  
    cocotb.log.info(f"Total signals found: {len(signals)} out of {len(signal_names_with_alternates)}")
    for name, handle in signals.items():
        cocotb.log.info(f"Signal name: {name}, Handle: {handle}")

  
    if unrecognizable_signals:
        cocotb.log.warning(f"Unrecognizable signals: {', '.join(unrecognizable_signals)}")

    await test_read_command(dut, signals)

async def test_read_command(dut, signals):
   
    pass'''

@cocotb.test()
async def test_reset(dut):
    """Test reset command."""
    await generate_clock(dut)
    await txn('reset',dut)
    await Timer(10, units='ns')

@cocotb.test()
async def test_read_device_id(dut):
    """Test read device ID command."""
    await generate_clock(dut)
    addr = [0x00]  # Example address
    rv = await txn('read_device_id',dut,addr=addr)
    dut._log.info(f"Read Device ID: {rv}")

@cocotb.test()
async def test_block_erase(dut):
    """Test block erase command."""
    await generate_clock(dut)
    addr = [0x00, 0x00, 0x01]  # Example address
    await txn('block_erase',dut,addr=addr)
    await Timer(10, units='ns')

@cocotb.test()
async def test_standard_read(dut):
    """Test standard read command."""
    await generate_clock(dut)
    addr = [0x00, 0x00, 0x00, 0x00, 0x00]  # Example address
    rv = await txn('standard_read',dut, addr=addr)
    dut._log.info(f"Standard Read: {rv}")
