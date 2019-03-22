from camera.devices.ikon import IKon
from andor_server.proxy import AndorSDKProxy

AndorSDKProxy.verbose = False

class Microscope(IKon):
    andor_servername = 'yesr10_andor'
    andor_serialnumber = 11115
    
    def initialize(self, config):
        super(IKon, self).initialize(config)
        self.connect_to_labrad()
        
        andor_server = self.cxn[self.andor_servername]
        andor = AndorSDKProxy(andor_server)
        
        andor.Initialize()
        andor.SetFanMode(2)
        andor.SetTemperature(-70)
        andor.SetCoolerMode(0)
        andor.CoolerON()
    
    def record(self, record_path=None, record_type=None, record_settings={}):
        if record_path is None:
            return
        
        andor_server = self.cxn[self.andor_servername]
        andor = AndorSDKProxy(andor_server)

        # abort if acquiring
        andor.AbortAcquisition()

        if record_type == 'g':
            andor.SetAcquisitionMode(3)
            andor.SetReadMode(4)
            andor.SetNumberAccumulations(1)
            andor.SetNumberKinetics(3)
            andor.SetAccumulationCycleTime(0)
            andor.SetKineticCycleTime(0)
            andor.SetPreAmpGain(0)
            andor.SetHSSpeed(0, 0)
            andor.SetVSSpeed(1)
            andor.SetShutter(1, 1, 0, 0)
            andor.SetTriggerMode(1)
            andor.SetExposureTime(500e-6)
            andor.SetImage(1, 1, 1, 1024, 1, 1024)
            
            for i in range(3):
                andor.StartAcquisition()
                andor.WaitForAcquisition()

            data = andor.GetAcquiredData(3 * 1024 * 1024).reshape(3, 1024, 1024)
            images = {key: data[i] 
                      for i, key in enumerate(["image", "bright", "dark"])}
            
            self._save(images, record_path)
            self._send_update(record_path, record_type)
        
        if record_type == 'eg':
            andor.SetAcquisitionMode(4)
            andor.SetReadMode(4)
            andor.SetPreAmpGain(0)
            andor.SetHSSpeed(0, 0)
            andor.SetVSSpeed(1)
            andor.SetShutter(1, 1, 0, 0)
            andor.SetTriggerMode(1)
            andor.SetFastKineticsEx(341, 3, 500e-6, 4, 1, 1, 682)

            andor.StartAcquisition()
            andor.WaitForAcquisition()
            data = andor.GetAcquiredData(3 * 341 * 1024).reshape(3, 341, 1024)
            images = {key: data[i] 
                    for i, key in enumerate(["image_g", "image_e", "bright"])}
            
            andor.StartAcquisition()
            andor.WaitForAcquisition()
            data = andor.GetAcquiredData(3 * 341 * 1024).reshape(3, 341, 1024)
            
            background_images = {key: data[i] 
                    for i, key in enumerate(["dark_g", "dark_e", "dark_bright"])}

            images.update(background_images)
            
            self._save(images, record_path)
            self._send_update(record_path, record_type)
        
        if record_type == 'fast-g':
            andor.SetAcquisitionMode(4)
            andor.SetReadMode(4)
            andor.SetPreAmpGain(0)
            andor.SetHSSpeed(0, 0)
            andor.SetVSSpeed(1)
            andor.SetShutter(1, 1, 0, 0)
            andor.SetTriggerMode(1)
            andor.SetFastKineticsEx(341, 3, 500e-6, 4, 1, 1, 683)

            andor.StartAcquisition()
            andor.WaitForAcquisition()
            data = andor.GetAcquiredData(3 * 341 * 1024).reshape(3, 341, 1024)
            images = {key: data[i] 
                    for i, key in enumerate(["image", "bright", "dark"])}
            
            self._save(images, record_path)
            self._send_update(record_path, record_type)
        
        if record_type == 'fast-eg':
            andor.SetAcquisitionMode(4)
            andor.SetReadMode(4)
            andor.SetPreAmpGain(0)
            andor.SetHSSpeed(0, 0)
            andor.SetVSSpeed(1)
            andor.SetShutter(1, 1, 0, 0)
            andor.SetTriggerMode(1)
            andor.SetFastKineticsEx(256, 4, 500e-6, 4, 1, 1, 1024 - 256)
#            andor.SetFastKinetics(256, 4, 500e-6, 4, 1, 1)

            andor.StartAcquisition()
            andor.WaitForAcquisition()
            data = andor.GetAcquiredData(4 * 256 * 1024).reshape(4, 256, 1024)
            images = {key: data[i] 
#                    for i, key in enumerate(["empty", "image-g", "image-e", "bright"])}
                    for i, key in enumerate(["image-g", "image-e", "bright", "empty"])}
            
            self._save(images, record_path)
            self._send_update(record_path, record_type)

Device = Microscope
