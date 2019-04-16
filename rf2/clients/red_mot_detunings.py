from client_tools.widgets import MultipleClientContainer
from rf2.clients import alpha, beta

class Client(MultipleClientContainer):
    name = 'Red MOT Detunings'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    widgets = [alpha.Client(reactor), beta.Client(reactor)]
    widget = Client(widgets, reactor)
    widget.show()
    reactor.run()
