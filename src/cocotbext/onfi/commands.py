import cocotb
from cocotb.triggers import Timer
import sys
import os
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge, Timer
from bus import Bus
from memory import sigdict
cmds = {
    'reset': {
        'cmd1': 0xFF,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 0,
        'WE': 1,
        'RE': 1,
        'CE': 1,
        'DQS':1
##R/B_n xxtolowtohigh,xx to low takes tWb time ,tWB to to high takes tRST time
    },
    'sync_reset': {
        'cmd1': 0xFC,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 0,
        'W/R_n': 1,
        'RE': 0,
        'CE': 1,
        'DQS':1
##R/B_n xxtolowtohigh,xx to low takes tWb time ,tWB to to high takes tRST time
    },
    'reset_lun': {
        'cmd1': 0xFA,
        'addr_len': 3,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'read_device_id': {
        'cmd1': 0x90,
        'addr_len': 1,##address value is always 20h, 00h JEDEc manufacturer ID
        'cmd2': None,
        'data': None,
        'await_data': True, ##6 cycles of DOUT will be received
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1,
        'R/B_n':1
    },
    'read_param_page': {
        'cmd1': 0xEC,
        'addr_len': 1,##00h
        'cmd2': None,
        'data': None,
        'await_data': True,
        'R/B_n':1
    },
    'read_unique_id': {
        'cmd1': 0xED,
        'addr_len': 1,##00h
        'cmd2': None,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1,
        'R/B_n':1 ##High till tWB,then low till tR,cecomes high DQ arrives within tRR
    },
    'block_erase': {
        'cmd1': 0x60,
        'addr_len': 3,## R1+R2+R3 for 3 addr
        'cmd2': 0xD0,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1, ##SR[6] to be added here 
    },
    'read_status': {
        'cmd1': 0x70,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 0,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'read_status_enhanced': {
        'cmd1': 0x78,
        'addr_len': 3,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'standard_read': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x30,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'read_cache_sequential': {
        'cmd1': 0x31, ##after read
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 0,
        'WE': 1,
        'RE': 1,
        'CE': 1 ##SR[6] to be added
    },
    'read_cache_random': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x31,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'copyback_read': { ##SR[6] to be added 
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x35,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'copyback_program': {
        'cmd1': 0x85,
        'addr_len': 5,
        'cmd2': 0x10,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'copyback_read_with_data_output': {
        'cmd1': 0x05,
        'addr_len': 5,
        'cmd2': 0xE0,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'copyback_program_with_data_mod': { ##Not solved
        'cmd1': 0x85,
        'addr_len': 5,
        'cmd2': 0x10,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'zq_calibration_long': {
        'cmd1': 0xF9,
        'addr_len': 1,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 0,
        'WE': 1,
        'RE': 0,
        'CE': 1,
        'R/B_n':0 ## to 0 first in tWB time , stays 0 for tZQCL and then becomes 1
    },
    'zq_calibration_short': {
        'cmd1': 0xFB,
        'addr_len':1,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 0,
        'WE': 1,
        'RE': 0,
        'CE': 1,
        'R/B_n':0 ## to 0 first in tWB time , stays 0 for tZQCL and then becomes 1
    },
    'get_feature': {## tWB+tFEAT+tRR
        'cmd1': 0xEE,
        'addr_len': 1,
        'cmd2': None,
        'data': None,
        'await_data': True,##4 bytes
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1,
        'R/B_n':0 ##becomes 0 in tWB time , stays 0 for tFEAT+trr,goes back to 1
    },
    'set_feature': {##add tADL
        'cmd1': 0xEF,
        'addr_len': 1,##Might be more reminder to check again for LUN set features
        'cmd2': None,
        'data': [0x00, 0x00, 0x00, 0x00],  
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1,
        'R/B_n':0 
    },
    'read_page': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x30,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'random_data_input': {
        'cmd1': 0x85,
        'addr_len': 2,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'random_data_output': {
        'cmd1': 0x05,
        'addr_len': 2,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'program_page': {
        'cmd1': 0x80,
        'addr_len': 5,
        'cmd2': 0x10,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'program_page_cache': {
        'cmd1': 0x80,
        'addr_len': 5,
        'cmd2': 0x15,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'read_page_cache_sequential': {
        'cmd1': 0x31,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 0,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'read_page_cache_random': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x31,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'multi_plane_page_read': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x32,
        'data': None,
        'await_data': True,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 1,
        'CE': 1
    },
    'multi_plane_page_program': {
        'cmd1': 0x80,
        'addr_len': 5,
        'cmd2': 0x11,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    },
    'multi_plane_block_erase': {
        'cmd1': 0x60,
        'addr_len': 3,
        'cmd2': 0xD1,
        'data': None,
        'await_data': False,
        'CLE': 1,
        'ALE': 1,
        'WE': 1,
        'RE': 0,
        'CE': 1
    }
}

async def txn(name, dut,bus=None,byte=None, addr=None, data=None):
    txn_template = cmds[name]
    txdata = []
    signal_keywords = ["CLE", "ALE", "WE", "RE", "CE"]
    
    
    bus = Bus(dut.u_nand_controller)

    
    bus_signal_names = dir(bus)
    print("Available signals in Bus:", bus_signal_names)

    
    relevant_signals = {}
    for sig_name in bus_signal_names:
        if any(keyword in sig_name for keyword in signal_keywords):
            actual_name = bus.get_actual_signal_name(sig_name)
            relevant_signals[actual_name] = getattr(bus, actual_name)
    
    print("Relevant signals to drive:")
    for sig_name, sig_obj in relevant_signals.items():
        print(f"{sig_name}: {sig_obj}")

    # Drive the relevant signals
    for sig_name, sig_obj in relevant_signals.items():
        keyword = next((kw for kw in signal_keywords if kw in sig_name), None)
        signal_value = txn_template.get(keyword, None)
        if signal_value is not None:
            sig_obj.value = signal_value
            print(f"Driving {sig_name} to {signal_value}")
        else:
            print(f"Warning: No value found for {sig_name} in the txn template. Skipping.")

    await Timer(10, units='ns')

    
    txdata.append(txn_template['cmd1'])

    if txn_template['addr_len'] is not None:
        if addr is None:
            addr = [0x00] * txn_template['addr_len']  
        txdata.extend(addr[:txn_template['addr_len']])
        
    if txn_template['cmd2'] is not None:
        txdata.append(txn_template['cmd2'])

    if data is None and txn_template.get('data') is not None:
        data = txn_template['data']
    if data is not None:
        txdata.extend(data)

    await _send_bytes(dut, txdata)
    
    if txn_template.get('await_data'):
        rv = await _get_bytes(len(txdata))
        return rv
    else:
        return None

    for i in range(8):
        signal_name_0 = f"IO{i}_0"
        signal_name_1 = f"IO{i}_1"

        if hasattr(bus, signal_name_0):
            setattr(getattr(bus, signal_name_0), 'value', (byte >> i) & 0x1)
        else:
            print(f"Warning: Signal {signal_name_0} not found in Bus. Skipping.")

        if hasattr(bus, signal_name_1):
            setattr(getattr(bus, signal_name_1), 'value', (byte >> (i + 8)) & 0x1)
        else:
            print(f"Warning: Signal {signal_name_1} not found in Bus. Skipping.")
        dut.IO_bus.value = byte
async def _send_bytes(dut, txdata):
    bus = Bus(dut.u_nand_controller)
    for byte in txdata:
        await _drive_to_io_ports(dut, bus, byte)
        await Timer(10, units='ns')  

async def _drive_to_io_ports(dut, bus, byte):
    for i in range(8):
        signal_name_0 = f"IO{i}_0"
        signal_name_1 = f"IO{i}_1"

        if hasattr(bus, signal_name_0):
            setattr(getattr(bus, signal_name_0), 'value', (byte >> i) & 0x1)
        else:
            print(f"Warning: Signal {signal_name_0} not found in Bus. Skipping.")

        if hasattr(bus, signal_name_1):
            setattr(getattr(bus, signal_name_1), 'value', (byte >> (i + 8)) & 0x1)
        else:
            print(f"Warning: Signal {signal_name_1} not found in Bus. Skipping.")
        dut.IO_bus.value = byte

async def _get_bytes(num_bytes):
    rv = [0xFF] * num_bytes  
    return rv



