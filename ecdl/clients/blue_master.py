from ecdl.clients.ecdl_control import ECDLControl

class MyECDLControl(ECDLControl):
    servername = 'ecdl'
    name = 'blue_master'
    update_id = 461014

    piezo_voltage_display_units = [(0, 'V')]
    piezo_voltage_digits = 2
    diode_current_display_units = [(0, 'mA')]
    diode_current_digits = 1
    update_time = 100

    spinbox_width = 80

if __name__ == '__main__':
    from PyQt4 import QtGui
    a = QtGui.QApplication([])
    from client_tools import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = MyECDLControl(reactor)
    widget.show()
    reactor.run()
