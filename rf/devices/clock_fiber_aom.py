from rf.devices.afg3252.device import AFG3252

class ClockFiberDemod(AFG3252):
    visa_server_name = 'yesr5_gpib'
    visa_address = 'USB0::0x0699::0x0345::C020003::INSTR' 
    source = 1
    
Device = ClockFiberDemod
