from rf.devices.n5181a.device import N5181A

class ClockSteer(N5181A):
    vxi11_address = "192.168.1.10"
    
    amplitude_units = 'V'
    amplitude_range = (0, 0.5)
    
    frequency_range = (20e3, 30e6)

Device = ClockSteer
