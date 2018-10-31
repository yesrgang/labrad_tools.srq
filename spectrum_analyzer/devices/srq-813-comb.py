from spectrum_analyzer.devices.dsa815.device import DSA815

class SA(DSA815):
    vxi11_address = '192.168.1.32'
    trace_index = 1

Device = SA
