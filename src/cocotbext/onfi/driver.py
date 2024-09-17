import cocotb
import logging
from cocotb_bus.drivers import BusDriver
from cocotb.triggers import RisingEdge, Timer
from bus import Bus  # Assuming your custom Bus class is correctly implemented here

class NFCOpcodeDriver(BusDriver):
    """Driver to handle sending opcodes and other necessary signals to the NandFlashController_Top.

    Args:
        entity: A handle to the top module entity.
        name: Name of the bus.
        clock: The clock signal associated with this bus.
    """

    _signals = ['iOpcode', 'iEnable', 'iControl']  # Add other relevant signals here
    _optional_signals = []

    def __init__(self, entity, name, clock, **kwargs):
        """Initialize the bus driver for NFCOpcodeDriver.

        Args:
            entity: Handle to the top module.
            name: Name of the bus.
            clock: The clock signal for synchronization.
            **kwargs: Additional keyword arguments.
        """
        # Set up logging
        self.log = logging.getLogger(f"cocotb.{entity._name}.{name}")

        # Manually initialize BusDriver
        BusDriver.__init__(self, entity, name, clock, **kwargs)

        # Capture the entity (top module) and clock
        self.entity = entity
        self.clock = clock

        # Instantiate the custom Bus class with provided signals
        self.bus = Bus(
            self.entity, name, signals={sig: sig for sig in self._signals}, optional_signals=self._optional_signals, **kwargs
        )

        # Initialize signals to default states
        for signal in self._signals:
            signal_name = self.bus.get_actual_signal_name(signal)
            if hasattr(self.bus, signal_name):
                getattr(self.bus, signal_name).value = 0  # Set to default value (e.g., 0)

        # Give this instance a unique name (handling array indexing if provided)
        index = kwargs.get("array_idx", None)
        self.name = name if index is None else f"{name}_{index}"

    async def _driver_send(self, transaction, sync: bool = True, delay_after_opcode: int = 0):
        """Send an opcode and other signals to the bus and apply a delay after.

        Args:
            transaction: The transaction (opcode) to send.
            sync: Synchronize the transfer by waiting for a rising edge.
            delay_after_opcode: Delay in ns after sending the opcode (default is 0).
        """
        # Ensure synchronization with the rising edge of the clock
        if sync:
            await RisingEdge(self.clock)

        # Set the value of iOpcode signal using the custom Bus class
        signal_name = self.bus.get_actual_signal_name('iOpcode')
        opcode_signal = getattr(self.bus, signal_name)
        opcode_signal.value = transaction  # Drive the signal with the transaction

        # Optionally handle additional signals here
        self._drive_additional_signals()

        # Log the transaction
        self.log.info(f"Sent transaction: {transaction} on signal: {signal_name}")

        # Add a delay after sending the opcode if specified
        if delay_after_opcode > 0:
            await Timer(delay_after_opcode, units="ns")

    def _drive_additional_signals(self):
        """Drive additional control signals if necessary."""
        # Example: Set some default or specific values for other signals
        for signal in self._signals:
            if signal != 'iOpcode':  # Skip the main signal
                signal_name = self.bus.get_actual_signal_name(signal)
                if hasattr(self.bus, signal_name):
                    getattr(self.bus, signal_name).value = 0  # Set to default value or modify as needed

