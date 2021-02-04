import os

from sequencer.clients.default import SequencerClient

class TestClient(SequencerClient):
    conductor_servername = 'conductor'
    sequencer_servername = 'sequencer'
    sequence_directory = os.path.join(os.getenv('PROJECT_DATA_PATH'), 
                                      'sequences', '{}')
    master_channel = 'Trigger@D15'
    timing_channel = 'Trigger@D15'

    display_names = {
        "@A00": "Blue MOT AOM",
        "@A01": "Blue MOT Shutter",
        "@A02": "Blue Fluor. AOM",
        "@A03": "Blue Fluor. Shutter",
        "@A04": "Blue Abs. AOM",
        "@A05": "Horiz. Abs. Shutter",
        "@A06": "Vert. Abs. Shutter",
        "@A07": "2D MOT Shutter",
        "@A08": "Zeeman Shutter",
        "@A09": "AH Enable",
        "@A10": "AH Bottom Enable",
        "@A11": "Kuro Trig.",
        "@A12": "Ikon Trig.",
        "@A13": "Mako Trig.",
        "@A14": "TTL A14",
        "@A15": "?TTL A15",
        
        "@B00": "AH Hall Probe Sw.",
        "@B01": "MOT Retro Disable",
        "@B02": "Beta FM Switch",
        "@B03": "Spin Pol. LC WP",
        "@B04": "HODT AOM",
        "@B05": "VODT AOM",
        "@B06": "HODT Shutter",
        "@B07": "VODT Shutter",
        "@B08": "?TTL B08",
        "@B09": "H1 AOM",
        "@B10": "H2 AOM",
        "@B11": "V AOM",
        "@B12": "?TTL B12",
        "@B13": "H1 Shutter",
        "@B14": "H2 Shutter",
        "@B15": "V Shutter",

        "@C00": "Broken",
        "@C01": "RM Gain Sw.",
        "@C02": "?TTL C02",
        "@C03": "?TTL C03",
        "@C04": "?TTL C04",
        "@C05": "?TTL C05",
        "@C06": "?TTL C06",
        "@C07": "?TTLC07",
        "@C08": "MOT Retro Enable",
        "@C09": "?TTL C09",
        "@C10": "?TTL C10",
        "@C11": "Transp. AOM",
        "@C12": "Troubleshoot",
        "@C13": "Alpha FM Sw.",
        "@C14": "Transp. Shutter",
        "@C15": "?TTL C15",

        "@D00": "Alpha AOM",
        "@D01": "Alpha Shutter",
        "@D02": "Beta AOM",
        "@D03": "Beta Shutter",
        "@D04": "Spin Pol. AOM",
        "@D05": "Spin Pol. Shutter",
        "@D06": "679 AOM",
        "@D07": "707 AOM",
        "@D08": "Repump Shutter",
        "@D09": "RM FM Trig.",
        "@D10": "?TTL D10",
        "@D11": "?TTL D11",
        "@D12": "?TTL D12",
        "@D13": "?TTL D13",
        "@D14": "AOSense Heat En.",
        "@D15": "Trigger",
        }


if __name__ == '__main__':
    from PyQt4 import QtGui
    app = QtGui.QApplication([])
    import client_tools.qt4reactor as qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    widget = TestClient(reactor)
    print widget.sequence_directory
    widget.show()
    reactor.run()
