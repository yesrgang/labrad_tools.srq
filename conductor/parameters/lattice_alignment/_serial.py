import socket
import codecs

def _comm(data, host=('localhost', 4292), timeout=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(host)
    s.settimeout(timeout)
    s.send(data)
    r = s.recv(1024)
    return r 

class SerialProxy(object):
    """ module proxy """
    EIGHTBITS = 8
    PARITY_NONE = 'N'
    STOPBITS_ONE = 1
    LF = b'\n'

    def __init__(self, inithost=('localhost', 4292)):
        self._inithost = inithost
        r = _comm('START libs _serial.py'.encode(), inithost)
        self._libhost = inithost[0], int(r.decode())
    
    def __del__(self):
        r = _comm('STOP {}'.format(self._libhost[1]).encode(), self._inithost)
    
    def _echo(self, message):
        r = _comm('_echo {}'.format(message).encode(), self._libhost)
        return r.decode()

    def Serial(self, port=None, baudrate=9600, bytesize=EIGHTBITS, 
               parity=PARITY_NONE, stopbits=STOPBITS_ONE, 
               timeout=None, xonxoff=False, rtscts=False, write_timeout=None, 
               dsrdtr=False, inter_byte_timeout=None):
        """ The port is immediately opened on object creation, 
        when a port is given. It is not opened when port is None and 
        a successive call to open() is required.

        port is a device name: depending on operating system. e.g. 
        /dev/ttyUSB0 on GNU/Linux or COM3 on Windows. The parameter 
        baudrate can be one of the standard values: 50, 75, 110, 134, 
        150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 
        38400, 57600, 115200. These are well supported on all 
        platforms. Standard values above 115200, such as: 230400, 
        460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 
        2000000, 2500000, 3000000, 3500000, 4000000 also work on many 
        platforms and devices. Non-standard values are also supported 
        on some platforms (GNU/Linux, MAC OSX >= Tiger, Windows). 
        Though, even on these platforms some serial ports may reject 
        non-standard values. Possible values for the parameter timeout 
        which controls the behavior of read():

            timeout = None: wait forever / until requested number of 
                            bytes are received
            timeout = 0: non-blocking mode, return immediately in 
                         any case, returning zero or more, up to the 
                         requested number of bytes
            timeout = x: set timeout to x seconds (float allowed) 
                         returns immediately when the requested number 
                         of bytes are available, otherwise wait until 
                         the timeout expires and return all bytes that 
                         were received until then.

        write() is blocking by default, unless write_timeout is set. 
        For possible values refer to the list for timeout above. Note 
        that enabling both flow control methods (xonxoff and rtscts) 
        together may not be supported. It is common to use one of the 
        methods at once, not both. dsrdtr is not supported by all 
        platforms (silently ignored). Setting it to None has the 
        effect that its state follows rtscts. Also consider using the 
        function serial_for_url() instead of creating Serial instances 
        directly.
        """
        return SerialSerialProxy(self._libhost, port, baudrate, bytesize, parity, 
                               stopbits, timeout, xonxoff, rtscts, 
                               write_timeout, dsrdtr, inter_byte_timeout)

class SerialSerialProxy(object):
    def __init__(self, host, port=None, baudrate=9600, 
                 bytesize=SerialProxy.EIGHTBITS, parity=SerialProxy.PARITY_NONE, 
                 stopbits=SerialProxy.STOPBITS_ONE, timeout=None, xonxoff=False, 
                 rtscts=False, write_timeout=None, dsrdtr=False, 
                 inter_byte_timeout=None):
        """ The port is immediately opened on object creation, 
        when a port is given. It is not opened when port is None and 
        a successive call to open() is required.

        port is a device name: depending on operating system. e.g. 
        /dev/ttyUSB0 on GNU/Linux or COM3 on Windows. The parameter 
        baudrate can be one of the standard values: 50, 75, 110, 134, 
        150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 
        38400, 57600, 115200. These are well supported on all 
        platforms. Standard values above 115200, such as: 230400, 
        460800, 500000, 576000, 921600, 1000000, 1152000, 1500000, 
        2000000, 2500000, 3000000, 3500000, 4000000 also work on many 
        platforms and devices. Non-standard values are also supported 
        on some platforms (GNU/Linux, MAC OSX >= Tiger, Windows). 
        Though, even on these platforms some serial ports may reject 
        non-standard values. Possible values for the parameter timeout 
        which controls the behavior of read():

            timeout = None: wait forever / until requested number of 
                            bytes are received
            timeout = 0: non-blocking mode, return immediately in 
                         any case, returning zero or more, up to the 
                         requested number of bytes
            timeout = x: set timeout to x seconds (float allowed) 
                         returns immediately when the requested number 
                         of bytes are available, otherwise wait until 
                         the timeout expires and return all bytes that 
                         were received until then.

        write() is blocking by default, unless write_timeout is set. 
        For possible values refer to the list for timeout above. Note 
        that enabling both flow control methods (xonxoff and rtscts) 
        together may not be supported. It is common to use one of the 
        methods at once, not both. dsrdtr is not supported by all 
        platforms (silently ignored). Setting it to None has the 
        effect that its state follows rtscts. Also consider using the 
        function serial_for_url() instead of creating Serial instances 
        directly.
        """
        self._host = host

        kwargs = {'port': port, 'baudrate': baudrate, 
                  'bytesize': bytesize, 'parity': parity, 
                  'stopbits': stopbits, 'timeout': timeout,
                  'xonxoff': xonxoff, 'rtscts': rtscts, 
                  'write_timeout': write_timeout, 'dsrdtr': dsrdtr,
                  'inter_byte_timeout': inter_byte_timeout}
        
        r = _comm('Serial {}'.format(kwargs).encode(), self._host)
    
    def __del__(self):
        self.close()

    @property
    def baudrate(self):
        """ Read or write current baud rate setting.
        Type: int
        """
        r = _comm('Serial.baudrate_getattr'.encode(), self._host)
        return int(codecs.encode(r, 'hex'), 16)

    @baudrate.setter
    def baudrate(self, baudrate):
        """ Read or write current baud rate setting.
        Type: int
        """
        r = _comm('Serial.baudrate_setattr {}'.format(baudrate).encode(), self._host)

    @property
    def bytesize(self):
        """ Read or write current byte size setting.
        Type: int
        """
        r = _comm('Serial.bytesize_getattr'.encode(), self._host)
        return int(codecs.encode(r, 'hex'), 16)

    @bytesize.setter
    def bytesize(self, bytesize):
        """ Read or write current byte size setting.
        Type: int
        """
        r = _comm('Serial.bytesize_setattr {}'.format(bytesize).encode(), self._host)

    def close(self):
        """ Close port """
        r = _comm('Serial.close'.encode(), self._host)
        
    @property
    def dsrdtr(self):
        """ Read or write current hardware flow control setting.
        Type: bool
        """
        r = _comm('Serial.dsrdtr_getattr'.encode(), self._host)
        return bool(r)

    @dsrdtr.setter
    def dsrdtr(self, dsrdtr):
        """ Read or write current hardware flow control setting.
        Type: bool
        """
        r = _comm('Serial.dsrdtr_setattr {}'.format(dsrdtr).encode(), self._host)

    @property
    def parity(self):
        """ Get current parity setting 
        """
        r = _comm('Serial.parity_getattr'.encode(), self._host)
        return r.decode()

    @parity.setter
    def parity(self, parity):
        """ Set new parity mode. 
        Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD,
                         PARITY_MARK, PARITY_SPACE
        """
        r = _comm('Serial.parity_setattr {}'.format(parity).encode(), self._host)
    
    @property
    def rtscts(self):
        """ Get current hardware flow control setting
        Type: bool
        """
        r = _comm('Serial.rtscts_getattr'.encode(), self._host)
        return bool(r)

    @rtscts.setter
    def rtscts(self, rtscts):
        """ Enable or disable hardware flow control setting
        Type: bool
        """
        r = _comm('Serial.rtscts_setattr {}'.format(rtscts).encode(), self._host)

    @property
    def stopbits(self):
        """ Get current stop bit setting """
        r = _comm('Serial.stopbits_getattr'.encode(), self._host)
        return int(codecs.encode(r, 'hex'), 16)

    @stopbits.setter
    def stopbits(self, stopbits):
        """ Set new stop bit settings
        Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
        """
        r = _comm('Serial.stopbits_setattr {}'.format(stopbits).encode(), self._host)

    @property
    def timeout(self):
        """ Get current read timeout setting
        Type: float (seconds)
        """
        r = _comm('Serial.timeout_getattr'.encode(), self._host)
        return struct.unpack('>f', r)[0]

    @timeout.setter
    def timeout(self, timeout):
        """ Set read timeout 
        Type: float (seconds)
        """
        r = _comm('Serial.timeout_setattr {}'.format(timeout).encode(), self._host)

    def read(self, size=1):
        """ Read size bytes from the serial port. If a timeout is 
        set it may return less characters as requested. With no 
        timeout it will block until the requested number of bytes is 
        read.
        
        Parameters:	
            size (int): Number of bytes to read.
        Returns:
            (bytes) Bytes read from the port.
        """
        r = _comm('Serial.read {}'.format(size).encode(), self._host)
        return r

    def read_until(self, expected=SerialProxy.LF, size=None):
        """ Read size bytes from the serial port. If a timeout is set 
        it may return less characters as requested. With no timeout it 
        will block until the requested number of bytes is read.

        Parameters:	
            expected (bytes): The byte string to search for.
            size (int): Number of bytes to read.
        Returns:	
            (bytes) Bytes read from the port.
        """
        r = _comm('Serial.read_until {} {}'.format(expected.decode(), size).encode(), self._host)
        return r

    def write(self, data):
        """ Write the bytes data to the port. 
        
        This should be of type bytes (or compatible such as bytearray 
        or memoryview). Unicode strings must be encoded 
        e.g. 'hello'.encode('utf-8')

        Parameters:	
            data (bytes): Data to send.
        Returns:
            (int) Number of bytes written.
        Raises:
            SerialTimeoutException
                In case a write timeout is configured for the port and 
                the time is exceeded.
        """
        r = _comm('Serial.write {}'.format(data.decode()).encode(), self._host)
        return int(codecs.encode(r, 'hex'), 16)

def handle_request(conn):
    global ser
    data = conn.recv(1024)
    action, _, args = data.partition(b" ")

    if action == b'_echo':
        conn.send(args)
    elif action == b'Serial':
        kwargs = eval(args)
        ser = serial.Serial(**kwargs)
        conn.send(b'')
    elif action == b'Serial.baudrate_getattr':
        baudrate = ser.baudrate
        conn.send(int(baudrate).to_bytes(4, 'big'))
    elif action == b'Serial.baudrate_setattr':
        baudrate = int(args)
        ser.baudrate = baudrate
        conn.send(b'')
    elif action == b'Serial.bytesize_getattr':
        bytesize = ser.bytesize
        conn.send(int(bytesize).to_bytes(4, 'big'))
    elif action == b'Serial.bytesize_setattr':
        bytesize = int(args)
        ser.bytesize = bytesize
        conn.send(b'')
    elif action == b'Serial.close':
        try:
            ser.close()
        except:
            pass
        conn.send(b'')
    elif action == b'Serial.dsrdtr_getattr':
        dsrdtr = ser.dsrdtr
        conn.send(int(dsrdtr).to_bytes(1, 'big'))
    elif action == b'Serial.dsrdtr_setattr':
        dsrdtr = int(args)
        ser.dsrdtr = dsrdtr
        conn.send(b'')
    elif action == b'Serial.parity_getattr':
        parity = ser.parity
        conn.send(parity.encode())
    elif action == b'Serial.parity_setattr':
        parity = args.decode()
        ser.parity = parity
        conn.send(b'')
    elif action == b'Serial.rtscts_getattr':
        rtscts = ser.rtscts
        conn.send(int(rtscts).to_bytes(1, 'big'))
    elif action == b'Serial.rtscts_setattr':
        rtscts = int(args)
        ser.rtscts = rtscts
        conn.send(b'')
    elif action == b'Serial.stopbits_getattr':
        stopbits = ser.stopbits
        conn.send(int(stopbits).to_bytes(4, 'big'))
    elif action == b'Serial.stopbits_setattr':
        stopbits = int(args)
        ser.stopbits = stopbits
        conn.send(b'')
    elif action == b'Serial.timeout_getattr':
        timeout = ser.timeout
        try:
            conn.send(struct.pack('>f', float(timeout)))
        except TypeError:
            conn.send(b'')
    elif action == b'Serial.timeout_setattr':
        timeout = float(args)
        ser.timeout = timeout
        conn.send(b'')
    elif action == b'Serial.read':
        size = args.decode()
        size = None if size == 'None' else int(size)
        bytes_ = ser.read(size)
        conn.send(bytes_)
    elif action == b'Serial.read_until':
        expected, size = args.decode().split(' ')
        size = None if size == 'None' else int(size)
        bytes_ = ser.read_until(expected.encode(), size)
        conn.send(bytes_)
    elif action == b'Serial.write':
        data = args.decode()
        numbytes = ser.write(data.encode())
        conn.send(int(numbytes).to_bytes(4, 'big'))


if __name__ == "__main__":
    import serial 
    import sys

    ser = None

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if len(sys.argv) == 2:
        s.bind(("0.0.0.0", 0))
        pid = sys.argv[1]
        port = s.getsockname()[1]
        stmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        stmp.connect(("localhost", 42922))
        stmp.send("PORT {} {}".format(pid, port).encode())
        s.listen(1)
    else:
        s.bind(("0.0.0.0", 65050))
        s.listen(1)

    while True:
        conn, addr = s.accept()
        handle_request(conn)
        conn.close()
