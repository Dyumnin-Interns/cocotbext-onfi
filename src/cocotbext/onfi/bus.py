from memory import sigdict

class Bus:

    def __init__(self, top, name=None, signals=sigdict, optional_signals=None, bus_separator="_", case_insensitive=True, array_idx=None):
        self._dut = top
        self._name = name
        self._signals = signals
        self._expanded_signals = {}

        num_luns = 2  # Adjust as needed

        
        for sig_name, sig_aliases in signals.items():
            if 'x' in sig_name:
                for lun in range(num_luns):
                    expanded_name = sig_name.replace('x', str(lun))
                    self._expanded_signals[expanded_name] = {
                        "Primary name": sigdict[sig_name]["Primary name"].replace('x', str(lun)),
                        "Secondary name": sigdict[sig_name]["Secondary name"].replace('x', str(lun)) if sigdict[sig_name]["Secondary name"] else None
                    }
            else:
                self._expanded_signals[sig_name] = sigdict[sig_name]

        
        dut_signals = {name for name in dir(self._dut) if not name.startswith('__')}

        
        renamed_signals = {}
        for sig_name, names in self._expanded_signals.items():
            primary_name = names["Primary name"]
            secondary_name = names["Secondary name"]

            if secondary_name and secondary_name in dut_signals:
                renamed_signals[primary_name] = secondary_name
                print(f"Renaming signal {secondary_name} to {primary_name}")
            elif primary_name in dut_signals:
                renamed_signals[primary_name] = primary_name
            else:
                print(f"Warning: Signal {primary_name} (or {secondary_name}) does not exist in the DUT. Skipping.")

        self.renamed_signals = renamed_signals

        # Step 4: Adding signals to the Bus with the correct names
        for primary_name, actual_name in renamed_signals.items():
            if name:
                signame = name + bus_separator + primary_name
            else:
                signame = primary_name

            print(f"Adding signal: {signame}")
            self._add_signal(primary_name, actual_name, array_idx, case_insensitive)

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
        for attr_name in self._signals:
            signal = getattr(self, attr_name)
            if strict and not hasattr(obj, attr_name):
                raise AttributeError(f"Missing attribute {attr_name} in object.")
            value = getattr(obj, attr_name, None)
            if value is not None:
                signal.value = value

    def capture(self):
        captured = {}
        for attr_name in self._signals:
            captured[attr_name] = getattr(self, attr_name).value
        return captured

