from awg.devices.ag335xxx.device import AG335xxx

class AlphaFM(AG335xxx):
    vxi11_address = '192.168.1.24'
    source = 1

    waveforms = [
        'INT:\\ALPHA.ARB',
        'INT:\\ALPHA_FAST.ARB',
        ]

Device = AlphaFM
