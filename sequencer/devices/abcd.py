from sequencer.devices.yesr_digital_board.device import YeSrDigitalBoard
from sequencer.devices.yesr_digital_board.channel import YeSrDigitalChannel

class ABCD(YeSrDigitalBoard):
    autostart = True
    conductor_servername = 'conductor'
    ok_servername = 'yesr20_ok'
#    ok_interface = '14290008VW'
    #ok_interface = '14290008VF'
    ok_interface = '1616000EHA'

    is_master = True

#    channels = [
#        YeSrDigitalChannel(loc=['A', 0], name='3D MOT AOM', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['A', 1], name='3D MOT Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 2], name='HR Abs. AOM', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['A', 3], name='HR Abs. Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 4], name='LR Abs. AOM', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['A', 5], name='LR H Abs. Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 6], name='LR V Abs. Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 7], name='2D MOT Shutter', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['A', 8], name='Zeeman Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 9], name='AH Enable', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 10], name='AH Bottom Enable', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 11], name='V Camera Trig.', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 12], name='H Camera Trig.', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 13], name='LR V Camera Trig.', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 14], name='TTLA14', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['A', 15], name='Gage Trig.', mode='auto', manual_output=False, invert=True),
#        
#        YeSrDigitalChannel(loc=['B', 0], name='Clock Detune', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 1], name='Clock Center/Sweep', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 2], name='Beta Phase', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 3], name='Spin Pol. LC Wave', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 4], name='HODT AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 5], name='VODT AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 6], name='HODT Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 7], name='VODT Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 8], name='MOT V Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 9], name='813 H1 AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 10], name='813 H2 AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 11], name='813 V AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 12], name='M2 Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 13], name='813 H1 Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 14], name='813 H2 Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['B', 15], name='813 V Shutter', mode='auto', manual_output=False, invert=False),
#        
#        YeSrDigitalChannel(loc=['C', 0], name='Broken!C00', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 1], name='RM Gain Switch', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 2], name='STIRAP P Switch', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['C', 3], name='STIRAP P Trigger', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 4], name='STIRAP S Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 5], name='STIRAP S Switch', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 6], name='STIRAP S Trigger', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 7], name='V Clock Switch', mode='manual', manual_output=True, invert=True),
#        YeSrDigitalChannel(loc=['C', 8], name='Clock Servo Enable', mode='manual', manual_output=True, invert=False),
#        YeSrDigitalChannel(loc=['C', 9], name='TTLC09', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 10], name='TTLC10', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 11], name='TTLC11', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 12], name='Troubleshoot', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 13], name='SrQ Comb Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 14], name='Sr1 Comb Shutter', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['C', 15], name='ODT Servo Enable', mode='manual', manual_output=True, invert=False),
#        
#        YeSrDigitalChannel(loc=['D', 0], name='Alpha AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 1], name='Alpha Shutter', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['D', 2], name='Beta AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 3], name='Beta Shutter', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['D', 4], name='Spin Pol. AOM', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['D', 5], name='Spin Pol. Shutter', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['D', 6], name='679 AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 7], name='707 AOM', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 8], name='Repump Shutter', mode='auto', manual_output=False, invert=True),
#        YeSrDigitalChannel(loc=['D', 9], name='RM FM Trigger', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 10], name='TTLD10', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 11], name='TTLD11', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 12], name='TTLD12', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 13], name='TTLD13', mode='auto', manual_output=False, invert=False),
#        YeSrDigitalChannel(loc=['D', 14], name='AOSense Heater Enable', mode='manual', manual_output=True, invert=False),
#        YeSrDigitalChannel(loc=['D', 15], name='Trigger', mode='auto', manual_output=False, invert=True),
#        ]
    channels = [
        YeSrDigitalChannel(loc=['A', 0], name='3D MOT AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 1], name='3D MOT Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 2], name='HR Abs. AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 3], name='HR Abs. Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 4], name='LR Abs. AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 5], name='LR H Abs. Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 6], name='LR V Abs. Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 7], name='2D MOT Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 8], name='Zeeman Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 9], name='AH Enable', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 10], name='AH Bottom Enable', mode='manual', manual_output=True, invert=False),
        YeSrDigitalChannel(loc=['A', 11], name='V Camera Trig.', mode='auto', manual_output=False, invert=False),#, delay=-300),
        YeSrDigitalChannel(loc=['A', 12], name='H Camera Trig.', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 13], name='LR V Camera Trig.', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 14], name='TTLA14', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['A', 15], name='Gage Trig.', mode='auto', manual_output=False, invert=True),
        
        YeSrDigitalChannel(loc=['B', 0], name='Clock Detune', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 1], name='Clock Center/Sweep', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['B', 2], name='Beta FM Switch', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 3], name='Spin Pol. LC Wave', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['B', 4], name='HODT AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 5], name='VODT AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 6], name='HODT Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 7], name='VODT Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 8], name='MOT V Shutter', mode='manual', manual_output=True, invert=False),
        YeSrDigitalChannel(loc=['B', 9], name='813 H1 AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 10], name='813 H2 AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 11], name='813 V AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 12], name='M2 Shutter', mode='manual', manual_output=True, invert=False),
        YeSrDigitalChannel(loc=['B', 13], name='813 H1 Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 14], name='813 H2 Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['B', 15], name='813 V Shutter', mode='auto', manual_output=False, invert=False),
        
        YeSrDigitalChannel(loc=['C', 0], name='Broken!C00', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 1], name='RM Gain Switch', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 2], name='LR AOM Sweep', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['C', 3], name='LR Demod Sweep', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 4], name='LR/HR [hi/lo]', mode='auto', manual_output=True, invert=False),
        YeSrDigitalChannel(loc=['C', 5], name='HR AOM Sweep', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 6], name='HR Demod Sweep', mode='manual', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 7], name='V Clock Switch', mode='manual', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['C', 8], name='Clock Servo Enable', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 9], name='RM Table Shutters', mode='auto', manual_output=True, invert=False),
        YeSrDigitalChannel(loc=['C', 10], name='RM Horizontal Shutter', mode='manual', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 11], name='Transp. AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 12], name='Troubleshoot', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 13], name='Alpha FM Switch', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 14], name='Transp. Shutter', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['C', 15], name='ODT Servo Enable', mode='manual', manual_output=True, invert=False),
        
        YeSrDigitalChannel(loc=['D', 0], name='Alpha AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 1], name='Alpha Shutter', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['D', 2], name='Beta AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 3], name='Beta Shutter', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['D', 4], name='Spin Pol. AOM', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['D', 5], name='Spin Pol. Shutter', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['D', 6], name='679 AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 7], name='707 AOM', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 8], name='Repump Shutter', mode='auto', manual_output=False, invert=True),
        YeSrDigitalChannel(loc=['D', 9], name='RM FM Trigger', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 10], name='TTLD10', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 11], name='StepperMotor', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 12], name='TTLD12', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 13], name='TTLD13', mode='auto', manual_output=False, invert=False),
        YeSrDigitalChannel(loc=['D', 14], name='AOSense Heater Enable', mode='manual', manual_output=True, invert=False),
        YeSrDigitalChannel(loc=['D', 15], name='Trigger', mode='auto', manual_output=False, invert=False),
        ]
    
        
Device = ABCD
