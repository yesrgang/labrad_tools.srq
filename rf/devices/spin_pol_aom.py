from rf.devices.ds345.device import DS345

class SpinPolAOM(DS345):
    visa_servername = 'yesr9_visa'
    visa_address = 'GPIB0::21::INSTR'

Device = SpinPolAOM
