from rf.devices.sg382.device import SG382

class ClockSteer(SG382):
    vxi11_address = "192.168.1.29"
    
    frequency_range = (20e3, 2e9)

Device = ClockSteer
