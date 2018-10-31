from awg.devices.ag335xxx.device import AG335xxx

class BetaFM(AG335xxx):
    vxi11_address = '192.168.1.24'
    source = 2

    waveforms = [
        'INT:\\BETA.ARB',
        'INT:\\BETA_FAST.ARB',
        ]

Device = BetaFM
