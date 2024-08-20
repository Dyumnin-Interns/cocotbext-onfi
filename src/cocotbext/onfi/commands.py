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
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 0},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'sync_reset': {
        'cmd1': 0xFC,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 0},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'reset_lun': {
        'cmd1': 0x00,
        'addr_len': 3,
        'cmd2': 0xFA,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_device_id': {
        'cmd1': 0x90,
        'addr_len': 1,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_param_page': {
        'cmd1': 0xEC,
        'addr_len': 1,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_unique_id': {
        'cmd1': 0xED,
        'addr_len': 1,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'block_erase': {
        'cmd1': 0x60,
        'addr_len': 3,
        'cmd2': 0xD0,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_status': {
        'cmd1': 0x70,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 0},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_status_enhanced': {
        'cmd1': 0x78,
        'addr_len': 3,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'standard_read': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x30,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_cache_sequential': {
        'cmd1': 0x31,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 0},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_cache_random': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x31,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'copyback_read': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x35,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'copyback_program': {
        'cmd1': 0x85,
        'addr_len': 5,
        'cmd2': 0x10,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'copyback_read_with_data_output': {
        'cmd1': 0x05,
        'addr_len': 5,
        'cmd2': 0xE0,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'copyback_program_with_data_mod': {
        'cmd1': 0x85,
        'addr_len': 5,
        'cmd2': 0x10,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'zq_calibration_long': {
        'cmd1': 0xF9,
   
    },
    'zq_calibration_long': {
        'cmd1': 0xF9,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 0},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'zq_calibration_short': {
        'cmd1': 0xFB,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 0},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'get_feature': {
        'cmd1': 0xEE,
        'addr_len': 1,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'set_feature': {
        'cmd1': 0xEF,
        'addr_len': 1,
        'cmd2': None,
        'data': [0x00, 0x00, 0x00, 0x00],  
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_page': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x30,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'random_data_input': {
        'cmd1': 0x85,
        'addr_len': 2,
        'cmd2': None,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'random_data_output': {
        'cmd1': 0x05,
        'addr_len': 2,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'program_page': {
        'cmd1': 0x80,
        'addr_len': 5,
        'cmd2': 0x10,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'program_page_cache': {
        'cmd1': 0x80,
        'addr_len': 5,
        'cmd2': 0x15,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_page_cache_sequential': {
        'cmd1': 0x31,
        'addr_len': None,
        'cmd2': None,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 0},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'read_page_cache_random': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x31,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'two_plane_page_read': {
        'cmd1': 0x00,
        'addr_len': 5,
        'cmd2': 0x32,
        'data': None,
        'await_data': True,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 1},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'two_plane_page_program': {
        'cmd1': 0x80,
        'addr_len': 5,
        'cmd2': 0x11,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    },
    'two_plane_block_erase': {
        'cmd1': 0x60,
        'addr_len': 3,
        'cmd2': 0xD1,
        'data': None,
        'await_data': False,
        'signal_ops': [
            {'signal': 'CLE', 'value': 1},
            {'signal': 'ALE', 'value': 1},
            {'signal': 'WE', 'value': 1},
            {'signal': 'RE', 'value': 0},
            {'signal': 'CE', 'value': 1}
        ]
    }
}
async def txn(command_name,dut,addr=None, data=None):
    
    txdata = []
    signal_keywords = ["CLE", "ALE", "WE", "RE", "CE"]
   
    def find_signals_with_keywords(dut, keywords):
        matching_signals = {}
        for attr_name in dir(dut):
            for keyword in keywords:
                if keyword in attr_name:
                    matching_signals.setdefault(keyword, []).append(attr_name)
        return matching_signals

    
    relevant_signals = find_signals_with_keywords(dut, signal_keywords)

    # Print all matching signals found
    print("Matching signals are the following:")
    for keyword, signal_names in relevant_signals.items():
        for signal_name in signal_names:
            print(f"Signal containing '{keyword}': {signal_name}")

   
    for keyword, signal_names in relevant_signals.items():
        signal_value = txn_template.get(keyword, None)  
        if signal_value is not None:
            for signal_name in signal_names:
               
                setattr(dut, signal_name, signal_value)
                print(f"Driving {signal_name} to {signal_value}")

   
    '''signal_ops = txn_template.get('signal_ops', None)
    if isinstance(signal_ops, list):
        for op in signal_ops:
            signal_name = op['signal']
            value = op['value']
            for signal in self.signals:
                if signal_name in signal:
                    signal_obj = self.signals[signal]
                    print(f"Toggling {signal} to value {value}")
                    signal_obj.drive(value)
    elif signal_ops is not None:
        raise TypeError("signal_ops must be a list of dictionaries ") 

       # Extract signals from the bus
    command_info = cmds.get(command_name)
    
    if not command_info:
        raise ValueError(f"Command {command_name} not found in cmds dictionary.")
    
    signal_ops = command_info.get('signal_ops', {})

    # Extract signals from the bus (dut)
    signals = [s for s in dir(dut) if not s.startswith("_")]
    print(f"Extracted the following signals: {signals}")

    # Matching and driving signals based on command signal operations
    for keyword, value in signal_ops.items():
        for sig in signals:
            if keyword in sig:
                # Drive the value
                signal_to_drive = getattr(dut, sig)
                signal_to_drive.value = value
                print(f"Driving {sig} with value {value} based on keyword {keyword}")'''



    await Timer(10, units='ns')

    txdata.append(txn_template['cmd1'])

    if txn_template['addr_len'] is not None:
        if addr is None:
            addr = [0x00] * txn_template['addr_len']  # Default address if none provided
        txdata.extend(addr[:txn_template['addr_len']])
        
    if txn_template['cmd2'] is not None:
        txdata.append(txn_template['cmd2'])

    
    if data is None and txn_template.get('data') is not None:
        data = txn_template['data']
    if data is not None:
        txdata.extend(data)

    await _send_bytes(dut,txdata)
    
    if txn_template.get('await_data'):
        rv = await _get_bytes(len(txdata))
        return rv
    else:
        return None

async def _send_bytes(dut,txdata):
    for byte in txdata:
        await _drive_to_io_ports(dut,byte)
        await Timer(10, units='ns')  # Simulate a delay between each byte
async def _drive_to_io_ports(dut, byte):
    for i in range(8):
        setattr(dut, f"IO{i}_0", (byte >> i) & 0x1)
    for i in range(8):
        setattr(dut, f"IO{i}_1", (byte >> (i + 8)) & 0x1)
    dut.IO_bus.value = byte    
async def _get_bytes(num_bytes):
    rv = [0xFF] * num_bytes  # Dummy data for simulation
    print(f"Received bytes: {rv}")
    return rv

