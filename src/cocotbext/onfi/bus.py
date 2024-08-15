from memory import sigdict

class Bus:
   

    def __init__(self, top, name=None, signals=sigdict, optional_signals=None, bus_separator="_", case_insensitive=True, array_idx=None):
        self._dut = top
        self._name= name
        self._signals = signals
      

        num_luns =  2 ##2 for now then later change it to len([s for s in dir(dut) if "LUN" in s])

        expanded_signals = {}
  
      
        for sig_name, sig_aliases in signals.items():
            if 'x' in sig_name:
                for lun in range(num_luns):
                    expanded_name = sig_name.replace('x', str(lun))
                    expanded_signals[expanded_name] = [alias.replace('x', str(lun)) for alias in sig_aliases]
            else:
                expanded_signals[sig_name] = sig_aliases

        
        for sig_name, sig_aliases in expanded_signals.items():
            sig_alternate = sig_aliases

            if name:
                signame = name + bus_separator + sig_name
            else:
                signame = sig_name

            
            self._add_signal(sig_name, signame, array_idx, case_insensitive)

        
        for attr_name, sig_name in self._optional_signals.items():
            self._add_optional_signal(attr_name, sig_name, array_idx, case_insensitive)

    def _add_signal(self, attr_name, sig_name, array_idx=None, case_insensitive=True):
        signal = self._get_signal(sig_name, case_insensitive)
        if array_idx is not None:
            signal = signal[array_idx]
        setattr(self, attr_name, signal)

    def _add_optional_signal(self, attr_name, sig_name, array_idx=None, case_insensitive=True):
        signal = self._get_signal(sig_name, case_insensitive)
        if signal is not None:
            if array_idx is not None:
                signal = signal[array_idx]
            setattr(self, attr_name, signal)

    def _get_signal(self, sig_name, case_insensitive=True):
        if case_insensitive:
            for name in dir(self._dut):
                if name.casefold() == sig_name.casefold():
                    return getattr(self._dut, name)
        return getattr(self._dut, sig_name, None)

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
            capture[attr_name] = getattr(self, attr_name).value
        return capture
