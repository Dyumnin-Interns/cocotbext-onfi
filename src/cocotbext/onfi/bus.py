from memory import sigdict

class Bus:

    def __init__(self, NandFlashController_Top, name=None, signals=sigdict, optional_signals=None, bus_separator="_", case_insensitive=True, array_idx=None):
        self._dut = NandFlashController_Top
        self._name = name
        self._signals = signals
        self._expanded_signals = {}

        num_luns = 2  # Adjust as needed

        # Expand signals, whether they contain 'x' or not
        for sig_name, sig_aliases in signals.items():
            primary_name = sigdict[sig_name]["Primary name"]
            secondary_name = sigdict[sig_name]["Secondary name"]

            # Check if primary or secondary name contains 'x' for expansion
            if 'x' in sig_name or (secondary_name and any('x' in sec for sec in (secondary_name if isinstance(secondary_name, list) else [secondary_name]))):
                # Expand the primary name and secondary names if 'x' is present
                for lun in range(num_luns):
                    expanded_primary = primary_name.replace('x', str(lun))

                    expanded_secondary = []
                    if secondary_name and isinstance(secondary_name, list):
                        expanded_secondary = [sec.replace('x', str(lun)) for sec in secondary_name]
                    elif secondary_name and isinstance(secondary_name, str):
                        expanded_secondary = [secondary_name.replace('x', str(lun))]

                    self._expanded_signals[expanded_primary] = {
                        "Primary name": expanded_primary,
                        "Secondary name": expanded_secondary
                    }
            else:
                # Add signals that don't contain 'x' without expansion
                self._expanded_signals[primary_name] = {
                    "Primary name": primary_name,
                    "Secondary name": secondary_name if isinstance(secondary_name, list) else [secondary_name]
                }

      
        dut_signals = {name for name in dir(self._dut) if not name.startswith('__')}

        
        renamed_signals = {}
        for sig_name, names in self._expanded_signals.items():
            primary_name = names["Primary name"]
            secondary_names = names["Secondary name"]

            # Check if any of the secondary names exist in the DUT
            found_secondary = None
            if secondary_names:
                for secondary_name in secondary_names:
                    if secondary_name in dut_signals:
                        found_secondary = secondary_name
                        break

            if found_secondary:
                renamed_signals[primary_name] = found_secondary
                print(f"Renaming signal {found_secondary} to {primary_name}")
            elif primary_name in dut_signals:
                renamed_signals[primary_name] = primary_name
            else:
                print(f"Warning: Signal {primary_name} (or one of {secondary_names}) does not exist in the DUT. Skipping.")

        self.renamed_signals = renamed_signals

        #  Adding signals to the Bus with the correct names
        for primary_name, actual_name in renamed_signals.items():
            if name:
                signame = name + bus_separator + primary_name
            else:
                signame = primary_name

            print(f"Adding signal: {signame}")
            self._add_signal(primary_name, actual_name, array_idx, case_insensitive)

        
        def _get_actual_signal_name(sig_name):
            """Return the actual signal name after considering renaming."""
            return self.renamed_signals.get(sig_name, sig_name)

        
        self.get_actual_signal_name = _get_actual_signal_name

    def _add_signal(self, attr_name, sig_name, array_idx=None, case_insensitive=True):
        signal = self._get_signal(sig_name, case_insensitive)
        if signal is None:
            available_signals = [name for name in dir(self._dut) if not name.startswith('__')]
            print(f"Warning: Signal {sig_name} not found in DUT. Available signals: {available_signals}")
            return
        if array_idx is not None:
            signal = signal[array_idx]
        setattr(self, attr_name, signal)


    def _add_signal(self, attr_name, sig_name, array_idx=None, case_insensitive=True):
        signal = self._get_signal(sig_name, case_insensitive)
        if signal is None:
            available_signals = [name for name in dir(self._dut) if not name.startswith('__')]
            print(f"Warning: Signal {sig_name} not found in DUT. Available signals: {available_signals}")
            return
        if array_idx is not None:
            signal = signal[array_idx]
        setattr(self, attr_name, signal)

    def _get_signal(self, sig_name, case_insensitive=True):
        if case_insensitive:
            for name in dir(self._dut):
                if name.casefold().strip() == sig_name.casefold().strip():
                    return getattr(self._dut, name)
        return getattr(self._dut, sig_name.strip(), None)

    def get_actual_signal_name(self, sig_name):
        """Return the actual signal name after considering renaming."""
        return self.renamed_signals.get(sig_name, sig_name)

    def drive(self, obj, strict=False):
        # Custom logic to handle combined signals like IO[7:0]
        for attr_name, signal_info in self._signals.items():
            if attr_name.startswith("IO") and "_0" in attr_name:
                combined_signal_name = "IO"  # Adjust based on how it's represented in the DUT
                combined_signal = getattr(self, combined_signal_name)
                if combined_signal is not None:
                    
                    value = combined_signal.value
                    for i in range(8):
                        individual_signal = getattr(self, f"IO{i}_0")
                        individual_signal.value = (value >> i) & 0x1
            elif strict and not hasattr(obj, attr_name):
                raise AttributeError(f"Missing attribute {attr_name} in object.")
            else:
                signal = getattr(self, attr_name)
                value = getattr(obj, attr_name, None)
                if value is not None:
                    signal.value = value

    def capture(self):
        captured = {}
        for attr_name, signal_info in self._signals.items():
            if attr_name.startswith("IO") and "_0" in attr_name:
                # Combine individual IO signals into one value
                combined_value = 0
                for i in range(8):
                    individual_signal = getattr(self, f"IO{i}_0")
                    combined_value |= (individual_signal.value << i)
                captured["IO"] = combined_value
            else:
                captured[attr_name] = getattr(self, attr_name).value
        return captured


