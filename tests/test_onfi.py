import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from commands import txn, cmds

async def generate_clock(dut):
    """Generate clock pulses."""
    cocotb.start_soon(Clock(dut.clk, 1, units="ns").start())

# List of signals with alternate names
signal_names_with_alternates = {
    "RE_x_n": ["RE_x_n", "RE_x_t"],
    "RE_x_c": ["RE_x_c"],
    "WR_x_n": ["WR_x_n"],
    "CE_x_n": ["CE_x_n"],
    "Vcc": ["Vcc"],
    "VccQ": ["VccQ"],
    "Vss": ["Vss"],
    "VssQ": ["VssQ"],
    "VREFQ_x": ["VREFQ_x"],
    "Vpp": ["Vpp"],
    "CLE_x": ["CLE_x"],
    "ALE_x": ["ALE_x"],
    "WE_x_n": ["WE_x_n"],
    "CLK_x": ["CLK_x"],
    "WP_x_n": ["WP_x_n"],
    "IO0_0": ["IO0_0", "DQ0_0"],
    "IO1_0": ["IO1_0", "DQ1_0"],
    "IO2_0": ["IO2_0", "DQ2_0"],
    "IO3_0": ["IO3_0", "DQ3_0"],
    "IO4_0": ["IO4_0", "DQ4_0"],
    "IO5_0": ["IO5_0", "DQ5_0"],
    "IO6_0": ["IO6_0", "DQ6_0"],
    "IO7_0": ["IO7_0", "DQ7_0"],
    "IO8": ["IO8"],
    "IO9": ["IO9"],
    "IO10": ["IO10"],
    "IO11": ["IO11"],
    "IO12": ["IO12"],
    "IO13": ["IO13"],
    "IO14": ["IO14"],
    "IO15": ["IO15"],
    "IO0_1": ["IO0_1", "DQ0_1"],
    "IO1_1": ["IO1_1", "DQ1_1"],
    "IO2_1": ["IO2_1", "DQ2_1"],
    "IO3_1": ["IO3_1", "DQ3_1"],
    "IO4_1": ["IO4_1", "DQ4_1"],
    "IO5_1": ["IO5_1", "DQ5_1"],
    "IO6_1": ["IO6_1", "DQ6_1"],
    "IO7_1": ["IO7_1", "DQ7_1"],
    "DQS_x_t": ["DQS", "DQS_x_t"],
    "DQS_x_c": ["DQS_x_c"],
    "DBI_x": ["DBI_x"],
    "ENo": ["ENo"],
    "ENi": ["ENi"],
    "VSP_x": ["VSP_x"],
    "R": ["R"],
    "RFT": ["RFT"],
    "NU": ["NU"],
    "NC": ["NC"],
    "ZQ_x": ["ZQ_x"]
}

# Fetch signals function
def fetch_signals(dut):
    found_signals = {}
    unrecognizable_signals = []
    for primary_signal, alternates in signal_names_with_alternates.items():
        for signal_name in alternates:
            if hasattr(dut, signal_name):
                found_signals[primary_signal] = getattr(dut, signal_name)
                break
        else:
            unrecognizable_signals.append(primary_signal)
    return found_signals, unrecognizable_signals

@cocotb.test()
async def test_command_signals(dut):
    await generate_clock(dut)
    await RisingEdge(dut.clk)

    # Fetch all signals
    signals, unrecognizable_signals = fetch_signals(dut)

    # Print fetched signals for debugging
    cocotb.log.info(f"Total signals found: {len(signals)} out of {len(signal_names_with_alternates)}")
    for name, handle in signals.items():
        cocotb.log.info(f"Signal name: {name}, Handle: {handle}")

    # List unrecognizable signals
    if unrecognizable_signals:
        cocotb.log.warning(f"Unrecognizable signals: {', '.join(unrecognizable_signals)}")

    # Add your command tests below
    await test_read_command(dut, signals)

async def test_read_command(dut, signals):
    # Assuming your read command test logic is here
    pass

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
