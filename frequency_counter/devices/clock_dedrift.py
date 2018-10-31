from frequency_counter.devices.ag53220a.device import AG53220A

class ClockDedrift(AG53220A):
    vxi11_address = '192.168.1.13'
    channel = 1

Device = ClockDedrift
