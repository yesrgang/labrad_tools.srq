"""
Provides low-level control of the 4-channel RF synthesizer developed by the JILA shop.

"""

import sys, os
import numpy as np
from labrad.server import LabradServer, setting
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet import reactor
from labrad.util import getNodeName
from jsonpickle import loads
import socket

import fpga_dds_settings as dds_settings
import fpga_dds_sequences as ds

class SynthesizerServer(LabradServer):
    """Provides low-level control of the 4-channel RF synthesizer developed by the JILA shop."""
    name = '%LABRADNODE%_synthesizer'

    def __init__(self):
        self.name = '{}_synthesizer'.format(getNodeName())
        super(SynthesizerServer, self).__init__()

    def initServer(self):
        """
        initServer(self)

        Called by LabRAD when server is started. Connects to the synthesizer using the socket library.
        """
        timeout = 1.02
        port = 804
        host = '192.168.1.110'
        self.dest = (host, int(port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.sock.settimeout(timeout)

    @staticmethod
    def f_to_ftw(f):
        """
        f_to_ftw(f)

        Converts a frequency in Hertz to the format required for programming the synthesizer

        Args:
            f (float): The frequency in Hertz

        Raises:
            ValueError: Raises an error if the frequency is less than zero or greater than the maximum frequency

        Returns:
            int: The unsigned integer corresponding to f
        """
        if f < 0 or f >= dds_settings.F_MAX:
            raise ValueError("Frequency of {} Hz outside valid range of 0 to {} Hz".format(f, dds_settings.F_MAX))
        f_int = int(round((f/dds_settings.F_MAX)*(2**dds_settings.F_BITS))) # overflows at F_MAX
        return f_int

    @staticmethod
    def a_to_atw(a):
        """
        a_to_atw(a)

        Converts an amplitude to the format required for programming the synthesizer

        Args:
            a (float): The amplitude, relative to full scale

        Raises:
            ValueError: Raises an error if the amplitude is less than zero or greater than one

        Returns:
            int: The unsigned integer corresponding to a
        """
        if a < 0 or a > 1:
            raise ValueError("Amplitude of {} outside valid range of 0 to 1".format(a))
        a_int = int(round(a*(2**dds_settings.A_BITS-1)))
        return a_int

    @staticmethod
    def t_to_timestamp(t):
        """
        t_to_timestamp(t)

        Converts a time to the format required for programming the synthesizer

        Args:
            t (float): The time, in seconds

        Raises:
            ValueError: Raises an error if the time is less than zero or greater than 27.962 seconds

        Returns:
            int: The unsigned integer corresponting to t
        """
        if t < 0 or t > dds_settings.T_MAX:
            raise ValueError("Time step of {} s outside valid range of 0 to {} s".format(t, dds_settings.T_MAX))
        t_int = int(round(t / dds_settings.T_MIN))
        return t_int

    @staticmethod
    def phase_to_ptw(phi):
        """
        phase_to_ptw(phi)

        Converts a phase to the format required for programming the synthesizer

        Args:
            phi (float): The phase in radians.

        Returns:
            int: The unsigned integer corresponting to phi
        """
        a_int = int(round((phi % (2*np.pi))/(2*np.pi)*(2**dds_settings.P_BITS)))
        return a_int

    @staticmethod
    def print_buffers(buffers):
        for i, buf in enumerate(buffers):
            #print(f'buffers[{i}]: 0x {int.from_bytes(buf[:4], "big"):08X} {int.from_bytes(buf[4:], "big"):08X}')
            print(f'buffers[{i}]: 0x  ', end='')
            for i in range(0, 4):
                print(f'{buf[i]:02X} ', end='')
            print('  ', end='')
            for i in range(4, 7):
                print(f'{buf[i]:02X} ', end='')
            print(f'{buf[7]:02X}')

    @staticmethod
    def compile_timestamp(channel, address, timestamp, phase_update, phase, amplitude, frequency, wait_for_trigger=False, digital_out=[False]*7):
        """
        compile_timestamp(self, channel, address, timestamp, phase_update, ptw, atw, ftw)

        Compiles a timestamp into a binary command which can be written to the synthesizer

        Args:
            channel (int): The channel to set. Must be between 0 and 3.
            address (int): The address of the timestep
            timestamp (int): The time of the timestamp (in s).
            phase_update (int): Whether to update the phase. 0 to not change phase, 1 to set absolute phase, 2 to increment phase.
            phase (int): The phase (in radians) to set
            amplitude (int): The amplitude (relative to full scale) to set
            frequency (int): The frequency (in Hz) to set
            wait_for_trigger (bool): Whether to wait for a trigger. Defaults to False.
            digital_out ([bool]): A list of 7 booleans, corresponding to whether each channel should be turned on. Defaults to [False]*7, in which case the digital outputs are off.

        Returns:
            List[ByteArray]: The messages to send to the synthesizer that represent the timestamp.
        """

        if channel >= dds_settings.N_CHANNELS or channel < 0 or not isinstance(channel, int):
            raise ValueError("Channel number {} must be an integer between 0 and {}.".format(channel, dds_settings.N_CHANNELS - 1))

        if address >= dds_settings.N_ADDRESSES or address < 0 or not isinstance(address, int):
            raise ValueError("Address {} must be an integer between 0 and {}.".format(address, dds_settings.N_ADDRESSES - 1))

        if phase_update != 0 and phase_update != 1 and phase_update != 2:
            raise ValueError("phase_update {} must be 0, 1, or 2.".format(phase_update))

        buffers = []
        for i in range(4):
            b = bytearray(8)
            b[0] = 0xA1 # Start bits
            b[1] = 2**4 * i + channel # Memory, channel
            b[2:4] = address.to_bytes(2, "big")
            buffers.append(b)

        # Timestamp, trigger & digital outputs
        dds_data = SynthesizerServer.t_to_timestamp(timestamp)
        dds_data |= int(wait_for_trigger) << 48
        for i in range(dds_settings.N_DIGITAL):
            dds_data |= digital_out[i] << (56+i)

        buffers[0][4:] = (dds_data & 0xFFFFFFFF).to_bytes(4, "big")
        buffers[1][4:] = (dds_data >> 32).to_bytes(4, "big")

        # Frequency (36-bit)
        dds_data = SynthesizerServer.f_to_ftw(frequency)

        # Amplitude (8-bit)
        dds_data |= (SynthesizerServer.a_to_atw(amplitude) & 0xFF) << 36

        # Phase (16-bit)
        dds_data |= (SynthesizerServer.phase_to_ptw(phase) & 0xFFFF) << 44

        dds_data |= phase_update << 60 # 0: don't change phase
                                       # 1: absolute phase
                                       # 2: phase increment wrt previous timestamp

        buffers[2][4:] = (dds_data & 0xFFFFFFFF).to_bytes(4, "big")
        buffers[3][4:] = (dds_data >> 32).to_bytes(4, "big")

        print('Compiled timestamp:')
        SynthesizerServer.print_buffers(buffers)
        return buffers

    @inlineCallbacks
    @setting(3)
    def trigger(self, c):
        """
        trigger(self)

        Triggers the synthesizer

        Args:
            c: The LabRAD context.
        """
        buffer = bytearray.fromhex(f"A200")
        yield self.sock.sendto(buffer, self.dest)
        print("Synthesizer triggered.")


    @inlineCallbacks
    @setting(4, reset_outputs='b')
    def reset(self, c, reset_outputs=False):
        """
        reset(self)

        Resets the synthesizer

        Args:
            c: The LabRAD context.
            reset_outputs: Whether to zero the outputs or just the sequencer
        """
        if reset_outputs:
            buffer = bytearray.fromhex(f"A400")
        else:
            buffer = bytearray.fromhex(f"A300")
        yield self.sock.sendto(buffer, self.dest)
        print("Synthesizer reset.")

    def _write_timestamps(self, timestamps, channel, freq_offs, freq_mult, verbose=False):
        """
            _write_timestamps(self, timestamps, channel, freq_offs, freq_mult, verbose=False)

            Programs the synthesizer with a list of timestamps.

        Args:
            timestamps (list of dictionaries): Each timestamp must contain fields:
                *timestamp: The time in seconds before the update
                *phase_update: 0 to preserve phase, 1 to set absolute phase, 2 to set relative phase
                *phase: The phase in radians
                *amplitude: The amplitude (between 0 and 1) relative to full scale
                *frequency: The frequency (between 0 and 300 MHz) in Hz
            channel (int): An integer between 0 and 3 determining the channel to program
            freq_offs (float): offset added to all frequencies (in Hz)
            freq_mult (float): multiplier for the timestep frequencies (before adding offset)
            verbose (bool, optional): Whether to print the messages sent to the synthesizer. Defaults to False.
        """
        buffers = []
        for i, s in enumerate(timestamps):
            timestamp = s["timestamp"]
            phase_update = s["phase_update"]
            phase = s["phase"]
            address = i
            amplitude = s["amplitude"]
            frequency = (freq_mult * np.array(s["frequency"]) + freq_offs).tolist()
            wait_for_trigger = bool(s["wait_for_trigger"])
            digital_out = s["digital_out"]
            buffers += SynthesizerServer.compile_timestamp(channel, address, timestamp, phase_update, phase, amplitude, frequency, wait_for_trigger, digital_out)
        print("Writing Channel {}.".format(channel))
        for b in buffers:
            if verbose:
                print(b.hex())
            self.sock.sendto(b, self.dest)

    @inlineCallbacks
    @setting(5, timestamps='s', compile='b', verbose='b')
    def write_timestamps(self, c, timestamps, freq_offs=0., freq_mult=1., compile=False, verbose=False):
        """
        write_timestamps(self, c, timestamps, freq_offs, freq_mult, compile=False, verbose=False)

        Writes timestamps from a JSON-formatted string. See :meth:`write_timestamps` for specification.

        Args:
            c: The LabRAD context. Not used.
            timestamps (str): A JSON-formatted string containing a dictionary (keys: channels, values: sequences) of lists of dictionaries, each of which is a timestamp.
            freq_offs (float): offset added to all frequencies (in Hz)
            freq_mult (float): multiplier for the timestep frequencies (before adding offset)
        """
        timestamps = loads(timestamps, keys=True)
        if compile:
            timestamps = loads(ds.compile_sequence(timestamps)[0], keys=True)
        for channel, ts in timestamps.items():
            yield self._write_timestamps(ts, int(channel), freq_offs, freq_mult, verbose)

if __name__ == '__main__':
    from labrad import util
    util.runServer(SynthesizerServer())
