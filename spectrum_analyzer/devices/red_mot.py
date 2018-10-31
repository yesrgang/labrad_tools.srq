from spectrum_analyzer.devices.dsa815.device import DSA815

class RedMOT(DSA815):
    vxi11_address = '192.168.1.4'
    trace_index = 1

Device = RedMOT
