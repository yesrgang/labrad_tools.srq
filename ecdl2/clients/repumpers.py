from client_tools.widgets import MultipleClientContainer
from ecdl2.clients import _679
from ecdl2.clients import _707

class Client(MultipleClientContainer):
    name = 'Repumpers'

if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    from client_tools import qt4reactor 
    qt4reactor.install()
    from twisted.internet import reactor

    widgets = [_707.Client(reactor), _679.Client(reactor)]
    widget = Client(widgets, reactor)
    widget.show()
    reactor.run()
