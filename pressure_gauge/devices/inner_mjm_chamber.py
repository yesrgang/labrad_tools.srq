class Device(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'ljm' not in globals():
            global ljm
            from labjack import ljm

        self._handle = ljm.openS()
    
    @property
    def pressure(self):
        try:
            return ljm.eReadName(self._handle, 'AIN0')
        except:
            self._handle = ljm.openS()
            return ljm.eReadName(self._handle, 'AIN0')

class DeviceProxy(Device):
    _labjack_servername = 'yesr3_labjack'
    
    def __init__(self, **kwargs):
        import labrad
        cxn = labrad.connect()
        from labjack_server.proxy import LJMProxy
        global ljm
        ljm = LJMProxy(cxn[self._labjack_servername])
        Device.__init__(self, **kwargs)

