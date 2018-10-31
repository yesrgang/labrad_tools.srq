from spectrum_analyzer.devices.dsa815.device import DSA815

class SA(DSA815):
    vxi11_address = '128.138.107.81'
    trace_index = 1

Device = SA
