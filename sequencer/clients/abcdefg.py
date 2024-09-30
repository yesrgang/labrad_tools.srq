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
        "@A03": "Horizontal Abs. Shutter",
        "@A04": "Blue Abs. AOM",
        "@A05": "Vertical. LR Abs. Shutter",
        "@A06": "?",
        "@A07": "2D MOT Shutter",
        "@A08": "Zeeman Shutter",
        "@A09": "AH Enable",
        "@A10": "V Clock AOM",
        "@A11": "Kuro Trig.",
        "@A12": "Pxlfly Trig.",
        "@A13": "Mako Trig.",
        "@A14": "3D1 shutter",
        "@A15": "Remove Clock ND",
        
        "@B00": "AH Hall Probe Sw.",
        "@B01": "MOT Retro Disable",
        "@B02": "Beta FM Switch",
        "@B03": "Spin Pol. LC WP",
        "@B04": "HODT AOM",
        "@B05": "VODT AOM",
        "@B06": "HODT Shutter",
        "@B07": "VODT Shutter",
        "@B08": "CLK AOM 2 TTL",
        "@B09": "H1 AOM",
        "@B10": "H2 AOM",
        "@B11": "V AOM",
        "@B12": "?TTL B12",
        "@B13": "H1 Shutter",
        "@B14": "H2 Shutter",
        "@B15": "V Shutter",

        "@C00": "Broken",
        "@C01": "RM Gain Sw.",
        "@C02": "H Clock Shutter",
        "@C03": "Cleanup Enable",
        "@C04": "AOM 3 TTL",
        "@C05": "Oblique Cleanup Enb.",
        "@C06": "1354 AOM",
        "@C07": "1354 shutter",
        "@C08": "MOT Retro Enable",
        "@C09": "Oblique Clock Shutter",
        "@C10": "Horizontal Abs. Shutter",
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
        "@D07": "Vertical HR Abs. Shutter",
        "@D08": "Repump Shutter",
        "@D09": "RM FM Trig.",
        "@D10": "TenS4 AOM",
        "@D11": "TenS4 Shutter",
        "@D12": "Alpha Pol. Shutter",
        "@D13": "Alpha Pol. AOM",
        "@D14": "AOSense Heat En.",
        "@D15": "Trigger",

#        "@G04": "NOISY",
        "@H03": "813 H2 Intensity",
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
