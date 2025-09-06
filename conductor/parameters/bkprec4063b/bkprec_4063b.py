class BKPrec4063B:
  def __init__(self, socket, recv_size=1024):
    self._socket = socket
    self._recv_size = recv_size # number of bytes to receive when reading from device

  def send_cmd(self, cmd): # cmd must be a byte string b''
    print('cmd:', cmd)
    self._socket.sendall(cmd + b'\r\n') # append telnet line termination
    try:
      return self._socket.recv(self._recv_size)
    except socket.timeout: # don't get upset about a timeout
      print('timeout!')
      pass # equivalent to returning None

