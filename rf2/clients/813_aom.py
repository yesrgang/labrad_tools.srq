from rf.clients.rf_client import RFClient, MultipleWidgetsContainer

class XClient(RFClient):
    name = '813_x_aom'
    servername = 'rf'
    
    frequency_display_units = [(6, 'MHz')]
    frequency_digits = 2
    amplitude_display_units = [(0, 'arb')]
    amplitude_digits = 2
    update_time = 100

    spinbox_width = 100

class YClient(RFClient):
    name = '813_y_aom'
    servername = 'rf'
    
    frequency_display_units = [(6, 'MHz')]
    frequency_digits = 2
    amplitude_display_units = [(0, 'arb')]
    amplitude_digits = 2
    update_time = 100

    spinbox_width = 100

class ZClient(RFClient):
    name = '813_z_aom'
    servername = 'rf'
    
    frequency_display_units = [(6, 'MHz')]
    frequency_digits = 2
    amplitude_display_units = [(0, 'arb')]
    amplitude_digits = 2
    update_time = 100

    spinbox_width = 100

class LatticeAOMClient(MultipleWidgetsContainer):
    name = 'lattice AOMs'
    widgets = [
        XClient,
        YClient,
        ZClient,
        ]

Client = LatticeAOMClient

if __name__ == '__main__':
    from PyQt4 import QtGui
    a = QtGui.QApplication([])
    import client_tools.qt4reactor as qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = Client(reactor)
    widget.show()
    reactor.run()
