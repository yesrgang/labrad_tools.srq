"""
Classes and functions for generating sequences for the RF synthesizer

To do:
    * Design functions for maintaining phase on frequency switching
    * Finish implementing SyncPoints
"""
from __future__ import annotations
from copy import copy, deepcopy
import numpy as np
from scipy.interpolate import interp1d
from typing import List, Optional
# from json import dumps, JSONEncoder
import json
# import jsonpickle
from dataclasses import dataclass

#import os, time, datetime
import os, datetime

#import plotly.graph_objects as go
#import plotly.express as px
#from plotly.subplots import make_subplots

import fpga_dds_settings as dds_settings


def set_float(val):
    return float(val) if val is not None else None


def set_float_or_str(val):
    if val is not None:
        return float(val) if type(val) is not str else str(val)
    else:
        return None


class SequenceState:
    """
    Records the state of a synthesizer channel at any point in the sequence. Used by :func:`compile_sequence` and the :meth:`RFBlock.compile`.
    """

    def __init__(
        self,
        phase: float = 0,
        frequency: float = 1e6,
        transition: Transition = None,
        pd_setpoint: float = 0,
        pd_selection: bool = False,
        clk_shutter: bool = False,
        clk_aom: bool = False,
        additional_params: dict = None,
        time: float = 0,
        tot_time: float = 0,
        dds_amplitude: float = 0,
        dds_triggers: int = 0,
        syncpoints: List[SyncPoint] = [],
        dds_digital_out: List[bool] = [False] * 7,
    ) -> None:
        """
        Args:
            phase (float): The phase of the channel. Defaults to 0.
            frequency (float): The frequency of the channel. Defaults to 1E6.
            transition (:class:`Transition`): The selected transition, as set by :class:`SetTransition`. Defaults to None.
            pd_setpoint (float): Setpoint of the clock PD. Defaults to 0.
            clk_shutter (bool): State of the clock shutter. Defaults to False.
            clk_aom (bool): State of the clock AOM. Defaults to False.
            additional_params (dict): Additional parameters ({"<param_name>": <value>}). Defaults to None.
            time (float): The time since the start or the last trigger. Defaults to 0.
            tot_time (float): The time since the start or the start of the sequence (first trigger). Defaults to 0.
            dds_amplitude (float): The amplitude of the DDS channel. Defaults to 0.
            dds_triggers (int): The number of DDS triggers required so far. Defaults to 0.
            syncpoints (list of str): The ordered list of :class:`SyncPoint` so far. Defaults to :code:`[]`.
            dds_digital_out (list of bool): The state of the digital outputs. Defaults to :code:`[False]*7`.
        """
        self.phase = set_float(phase)
        self.frequency = set_float(frequency)
        self.transition = transition
        self.pd_setpoint = set_float(pd_setpoint)
        self.pd_selection = pd_selection
        self.clk_shutter = clk_shutter
        self.clk_aom = clk_aom
        self.additional_params = additional_params
        self.time = set_float(time)
        self.tot_time = set_float(tot_time)
        self.dds_amplitude = set_float(dds_amplitude)
        self.dds_triggers = dds_triggers
        self.syncpoints = syncpoints
        self.dds_digital_out = dds_digital_out
    
    def update_additional_params(self, additional_params: dict):
        """
        Updates self.additional_params and checks for consistency.

        Args:
            additional_params (dict): Updated parameters.
        """
        # consistency checks between existing and new params
        if additional_params is not None:
            if self.additional_params is not None and (self.additional_params.keys() != additional_params.keys()):
                raise KeyError('Keys of additional_params change; they must stay the same within a sequence.\nold: {}\nnew: {}'.format(list(additional_params.keys()),
                                                                                                                                       list(self.additional_params.keys())))
        #if self.additional_params is None and additional_params is not None:
        #    raise ValueError('additional_params has previously been empty but has entries now; the number of entires cannot change within a sequence.')
        #elif self.additional_params is not None and additional_params is None:
        #    raise ValueError('additional_params was filled and is empty now; the number of entries cannot change within a sequence.')
        #for key,_ in self.additional_params.items():
        #    if type(self.additional_params[key]) is not type(additional_params[key]):
        #        raise TypeError('Type of additional_param {} changes from {} to {}; types cannot change within a sequence.'.format(
        #            key,
        #            type(self.additional_params[key]),
        #            type(additional_params[key])))

        # update parameters
        self.additional_params = copy(additional_params)


@dataclass
class RFBlock:
    """
    A base class for elements of a sequence for a synthesizer channel.

    Parameters:
        atomic (bool): Whether the block is handled directly by the compiler (True) or returns a sequence of blocks which need to be compiled (False). Defaults to False.
    """

    atomic = False

    def compile(self, state: Optional[SequenceState] = None) -> RFBlock | List[RFBlock]:
        """
        compile(self)

        Compiles the block into a list of basic :class:`RFBlock` that can be sent to the synthesizer.

        Args:
            state (:class:`SequenceState`, optional): The state of the channel when the block is to be called. Defaults to None, which can be used for testing :code:`compile` functions of :class:`RFBlock` objects that do not depend on channel state.

        Returns:
            (RFBlock | List[RFBlock]): The compiled :class:`RFBlock`.
        """
        return self

    def __repr__(self) -> str:
        raise NotImplementedError("Please implement me in subclasses.")


class RFPulse(RFBlock):
    """
    A base class for RF pulses.
    """

    @staticmethod
    def center(center: bool, sequence: List[RFBlock], duration: float):
        """
        center(center, sequence, duration):

        Helper function for centering a pulse by adjusting the duration of the surrounding :class:`Timestamp`. Should be included in the :meth:`RFBlock.compile` methods of subclasses as

        .. code-block:: python

            sequence = generate_some_stuff()
            return RFPulse.center(self.center, sequence, self.duration)

        Args:
            center (bool): Whether to center the sequence by adjusting the time of the surrounding :class:`Timestamp`.
            sequence (List[RFBlock]): The sequence.
            duration (float): The duration of the sequence in seconds.

        Returns:
            (list of :class:`RFBlock`): The sequence, centered if :code:`center`.
        """
        if center:
            return (
                [AdjustPrevDuration(-duration / 2)]
                + sequence
                + [AdjustNextDuration(-duration / 2)]
            )
        else:
            return sequence

    @property
    def area(self) -> float:
        """
        area(self)

        Returns the area of the pulse, relative to a rectangular pulse of the same duration and peak amplitude.

        Returns:
            (float): The area of the pulse, relative to a rectangular pulse of the same duration and peak amplitude
        """
        raise NotImplementedError("Please implement me in each subclass!")

    def compile(self, state: SequenceState = None) -> RFBlock | List[RFBlock]:
        raise NotImplementedError("Please implement me in each subclass!")


def validate_parameters(
    duration: float = None,
    phase: Optional[float] = None,
    frequency: Optional[float] = None,
    pd_setpoint: Optional[float] = None,
    additional_params: Optional[dict] = None,
    dds_amplitude: Optional[float] = None,
) -> None:
    """
    validate_parameters(duration=None, phase=None, frequency=None, pd_setpoint=None, additonal_params=None, dds_amplitude=None)

    Checks that commonly used parameters are within acceptable ranges.

    Args:
        duration (float, optional): Duration in seconds. Checks that it's non-negative. Defaults to None.
        phase (float, optional): Phase in radians. Checks that it's a real number. Defaults to None.
        frequency (float, optional): Frequency in Hertz. Checks that it's between zero and :code:`F_MAX`. Defaults to None.
        pd_setpoint (float, optional): Setpoint in volts. Checks that it's between -10 and +10. Defaults to None.
        additional_params (dict, optional): Checks that all values are either floats between -10 and +10 (analog channels) of bools (digital channels)
        dds_amplitude (float, optional): Amplitude relative to full scale. Checks that it's between zero and one. Defaults to None.

    Raises:
        ValueError: If any of the parameters are not None and outside their valid range.
    """
    if duration is not None and (duration < 0 or duration > dds_settings.T_MAX):
        raise ValueError(
            "Duration {} must be between zero and {}.".format(duration, dds_settings.T_MAX)
        )
    
    if phase is not None and not np.isreal(phase):
        raise ValueError("Phase {} must be a real number.".format(phase))
    #if frequency is not None and (frequency < 0 or frequency > dds_settings.F_MAX):
    #    raise ValueError(
    #        "Frequency {} must be between 0 and {}.".format(frequency, dds_settings.F_MAX)
    #    )
    if pd_setpoint is not None and (pd_setpoint < -10. or pd_setpoint > 10.):
        raise ValueError("PD setpoint {} must be between -10 and +10.".format(pd_setpoint))
    if additional_params is not None:
        for key,val in additional_params.items():
            if type(val) is float and (val < -10. or val > 10.):
                raise ValueError('Additional parameter {} (value: {}) must be between -10 and +10.'.format(key, val))
            elif type(val) is not bool:
                raise TypeError('Additional parameter {} is of type {} but only float or bool is allowed.'.format(key, type(val)))
    if dds_amplitude is not None and (dds_amplitude < 0 or dds_amplitude > 1):
        raise ValueError("DDS Amplitude {} must be between zero and one.".format(dds_amplitude))


class Timestamp(RFBlock):
    """
    A single timestamp, at which the amplitude, phase, and frequency of the tone can be set for a specified duration.
    """

    atomic = True

    def __init__(
        self,
        duration: float,
        phase: Optional[float] = None,
        frequency: Optional[float] = None,
        pd_setpoint: Optional[float] = None,
        pd_selection: Optional[int] = None,
        clk_shutter: Optional[bool] = None,
        clk_aom: Optional[bool] = None,
        additional_params: Optional[dict] = None,
        dds_amplitude: Optional[float] = None,
        dds_wait_for_trigger: Optional[bool] = False,
        dds_digital_out: Optional[dict] = {},
        dds_absolute_phase: Optional[bool] = False,
    ) -> None:
        """
        Args:
            duration (float): The duration of the timestamp. If the duration is zero, the parameters override ommited parameters in the next Timestamp.
            phase (float, optional): The phase of the tone in radians. Defaults to None, in which case the previous phase is maintained.
            frequency (float, optional): The frequency of the tone in Hertz. Defaults to None, in which case the previous frequency is maintained.
            pd_setpoint (float, optional): Clock PD setpoint (the value corresponds to the PD before the atoms and may be converted to the one after the atoms, depending on the value of selected_pd)
            pd_selection (bool, optional): Use PD before/after the chamber as input for the intensity servo
            clk_shutter (bool, optional): Position of the clock laser shutter
            clk_aom (bool, optional): Clock AOM disable / intensity servo integrator hold
            additional_params (dict, optional): Additional Sequencer channels ({"<ch_name>": <value>}, with <ch_name> being the same as the onces referenced in :class:'SequencerMapping)
            dds_amplitude (float, optional): The amplitude of the tone relative to full scale. Defaults to None, in which case the previous amplitude is maintained.
            dds_wait_for_trigger (bool, optional): Whether to wait for a trigger to start the timestamp. Defaults to False.
            dds_digital_out ({int: bool}, optional): A dictionary with keys (integers between 0 and 6) corresponding to the indices of digital outputs to set and boolean values corresponding to the desired state of the output. If a key is not present, the corresponding output is unchanged. Only used for the first channel. Defaults to {}.
            dds_absolute_phase (bool, optional): If true, sets the phase to :code:`phase` radians at the beginning of the timestamp. Otherwise offsets the phase to :code:`phase` radians relative to a reference clock. If True, :code:`phase` must not be None. Defaults to False.
        """
        self.duration = set_float(duration)
        self.phase = set_float(phase)
        self.frequency = set_float(frequency)
        self.pd_setpoint = set_float(pd_setpoint)
        self.pd_selection = pd_selection
        self.clk_shutter = clk_shutter
        self.clk_aom = clk_aom
        self.additional_params = additional_params
        self.dds_amplitude = set_float(dds_amplitude)
        self.dds_wait_for_trigger = dds_wait_for_trigger
        self.dds_digital_out = dds_digital_out
        self.dds_absolute_phase = dds_absolute_phase
        self.dds_phase_update = 0  # low-level phase-update bits for FPGA-DDS

    def __repr__(self) -> str:
        val = "Timestamp({}".format(self.duration)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        if self.frequency is not None:
            val += ", frequency={}".format(self.frequency)
        if self.pd_setpoint is not None:
            val += ", pd_setpoint={}".format(self.pd_setpoint)
        if self.pd_selection is not None:
            val += ", pd_selection={}".format(self.pd_selection)
        if self.clk_shutter is not None:
            val += ", clk_shutter={}".format(self.clk_shutter)
        if self.clk_aom is not None:
            val += ", clk_aom={}".format(self.clk_shutter)
        if self.additional_params is not None:
            val += ", additional_params={}".format(self.additional_params)
        if self.dds_amplitude is not None:
            val += ", dds_amplitude={}".format(self.dds_amplitude)
        if self.dds_wait_for_trigger:
            val += ", dds_wait_for_trigger={}".format(self.dds_wait_for_trigger)
        if len(self.dds_digital_out) > 0:
            val += ", dds_digital_out={}".format(self.dds_digital_out)
        return val + ")"
    
    def compile(self, state: Optional[SequenceState] = None) -> Timestamp:
        validate_parameters(self.duration, self.phase, self.frequency, self.pd_setpoint, self.additional_params, self.dds_amplitude)
        if self.dds_absolute_phase and self.phase is None:
            raise ValueError("Phase cannot be None if dds_absolute_phase is True")
        state.time += self.duration
        state.tot_time += self.duration
        if self.dds_absolute_phase:
            self.dds_phase_update = 1
            state.phase = self.phase
        elif self.phase is not None and self.phase != state.phase:
            self.dds_phase_update = 2
            state.phase = self.phase
        if self.frequency is not None:
            state.frequency = self.frequency
        if self.pd_setpoint is not None:
            state.pd_setpoint = self.pd_setpoint
        if self.pd_selection is not None:
            state.pd_selection = self.pd_selection
        if self.clk_shutter is not None:
            state.clk_shutter = self.clk_shutter
        if self.clk_aom is not None:
            state.clk_aom = self.clk_aom
        if self.additional_params is not None:
            state.update_additional_params(self.additional_params)
        if self.dds_amplitude is not None:
            state.dds_amplitude = self.dds_amplitude
        if self.dds_wait_for_trigger:
            state.dds_triggers += 1
            state.time = 0
        state.dds_digital_out = copy(state.dds_digital_out)
        for c, v in self.dds_digital_out.items():
            if not isinstance(v, bool):
                raise ValueError(
                    "Digital output {} must be boolean but is {}.".format(c, v)
                )
            if c < 0 or c >= dds_settings.N_DIGITAL:
                raise ValueError("Digital output {} is out of range.".format(c))
            state.dds_digital_out[c] = v

        return super().compile(state)


class Wait(Timestamp):
    """
    Waits for a fixed duration.
    """

    def __init__(self, duration: float, wait_for_trigger: bool = False) -> None:
        """
        Args:
            duration (float): The duration to wait in seconds.
            wait_for_trigger (bool): Whether to wait for a trigger. Defaults to False.
        """
        super().__init__(duration, wait_for_trigger=wait_for_trigger)


class SyncPoint(RFBlock):
    """
    Allows different channels to be synchronized. If SyncPoints with the same name appear in different channels, an appropriate sequence of :class:`Wait` blocks are inserted into the channels for which it would occur earlier such that all channels reach the SyncPoint at the same time.

    Throws an error upon compilation if multiple SyncPoints with the same name occur in one channel's sequence or in an order such that they cannot be applied.
    """

    atomic = True

    def __init__(self, name: str) -> None:
        """
        Args:
            name: An identifier for the synchronization point.
        """
        self.name = name

    def __repr__(self) -> str:
        return "SyncPoint('{}')".format(self.name)

    def compile(self, state: SequenceState) -> SyncPoint:
        state.syncpoints.append(self.name)
        return super().compile(state)


class AdjustPrevDuration(RFBlock):
    """
    Adjusts the duration of the previous :class:`Timestamp`. Throws an error on compilation if the previous :class:`RFBlock` is not a :class:`Timestamp` or the adjustment would result in negative duration.
    """

    atomic = True

    def __init__(self, duration: float) -> None:
        """
        Args:
            duration (float): The duration in seconds by which to increment the duration of the previous timestamp.
        """
        self.duration = duration

    def __repr__(self) -> str:
        return "AdjustPrevDuration({})".format(self.duration)

    def compile(self, state: SequenceState) -> AdjustPrevDuration:
        state.time += self.duration
        return super().compile(state)


class AdjustNextDuration(RFBlock):
    """
    Adjusts the duration of the next :class:`Timestamp`. Throws an error on compilation if the next :class:`RFBlock` is not a :class:`Timestamp` or the adjustment would result in negative duration.
    """

    atomic = True

    def __init__(self, duration: float) -> None:
        """
        Args:
            duration (float): The duration in seconds by which to increment the duration of the next timestamp.
        """
        self.duration = duration

    def __repr__(self) -> str:
        return "AdjustNextDuration({})".format(self.duration)

    def compile(self, state: SequenceState) -> AdjustNextDuration:
        state.time += self.duration
        return super().compile(state)


class RectangularPulse(RFPulse):
    """
    Generates a `rectangular pulse <https://en.wikipedia.org/wiki/List_of_window_functions#Rectangular_window>`_.
    """

    def __init__(
        self,
        duration: float,
        amplitude: float,
        phase: Optional[float] = None,
        frequency: Optional[float] = None,
        centered: bool = False,
    ) -> None:
        """
        Refer to :func:`Pulse` for descriptions of the arguments.
        """
        self.duration = duration
        self.amplitude = amplitude
        self.phase = phase
        self.frequency = frequency
        self.centered = centered

    @property
    def area(self) -> float:
        return 1

    def compile(self, state: Optional[SequenceState] = None) -> List[RFBlock]:
        validate_parameters(self.duration, self.amplitude, self.phase, self.frequency)
        sequence = [
            Timestamp(self.duration, self.amplitude, self.phase, self.frequency),
            Timestamp(0, 0),
        ]
        return RFPulse.center(self.centered, sequence, self.duration)

    def __repr__(self) -> str:
        val = "RectangularPulse({}, {}".format(self.duration, self.amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        if self.frequency is not None:
            val += ", frequency={}".format(self.frequency)
        if self.centered:
            val += ", centered=True"
        return val + ")"


class BlackmanPulse(RFPulse):
    """
    Generates a pulse with an `Blackman window <https://en.wikipedia.org/wiki/List_of_window_functions#Blackman_window>`_.
    """

    def __init__(
        self,
        duration: float,
        amplitude: float,
        phase: Optional[float] = None,
        frequency: Optional[float] = None,
        centered: Optional[float] = False,
        steps: int = 20,
        exact: bool = False,
    ) -> None:
        """
        Refer to :func:`Pulse` for descriptions of the arguments.

        Keyword Args:
            steps (int, optional): The number of steps to approximate the pulse. Should be at least 7. Defaults to 20.
            exact (bool, optional): Whether to use exact parameters for the window, as described `on Wikipedia <https://en.wikipedia.org/wiki/List_of_window_functions#Blackman_window>`_. Defaults to False.
        """
        self.duration = duration
        self.amplitude = amplitude
        self.phase = phase
        self.frequency = frequency
        self.centered = centered
        self.steps = steps
        self.exact = exact

    def __repr__(self) -> str:
        val = "BlackmanPulse({}, {}".format(self.duration, self.amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        if self.frequency is not None:
            val += ", frequency={}".format(self.frequency)
        if self.centered:
            val += ", centered=True"
        if self.steps is not None:
            val += ", steps={}".format(self.steps)
        return val + ", exact={})".format(self.exact)

    @property
    def area(self) -> float:
        self.compile()
        step = self.duration / self.steps
        return step * sum(self.amplitudes) / (self.amplitude * self.duration)

    def compile(self, state: Optional[SequenceState] = None) -> List[RFBlock]:
        validate_parameters(self.duration, self.amplitude, self.phase, self.frequency)
        if self.steps < 7 or int(self.steps) != self.steps:
            raise ValueError(
                "Steps (currently {}) must be an integer >= 7.".format(self.steps)
            )
        if self.exact:
            a = [7938.0 / 18608, 9240.0 / 18608, 1430.0 / 18608]
        else:
            a = [0.42, 0.5, 0.08]
        step = self.duration / self.steps
        N = self.steps - 1
        n = np.linspace(0, N, self.steps, endpoint=True)
        self.amplitudes = self.amplitude * (
            a[0] - a[1] * np.cos(2 * np.pi * n / N) + a[2] * np.cos(4 * np.pi * n / N)
        )
        timestamps = [Timestamp(step, min(1, max(amp, 0))) for amp in self.amplitudes]
        timestamps[0].phase = self.phase
        timestamps[0].frequency = self.frequency
        return RFPulse.center(
            self.centered, timestamps + [Timestamp(0, 0)], self.duration
        )


class GaussianPulse(RFPulse):
    """
    Generates a pulse with an `approximate confined Gaussian window <https://en.wikipedia.org/wiki/List_of_window_functions#Approximate_confined_Gaussian_window>`_. See also `here <http://dx.doi.org/10.1016/j.sigpro.2014.03.033>`_ for more details.
    """

    def __init__(
        self,
        duration: float,
        amplitude: float,
        phase: Optional[float] = None,
        frequency: Optional[float] = None,
        centered: bool = False,
        steps: int = 26,
        sigt: float = 0.11,
    ) -> None:
        """
        Refer to :func:`Pulse` for descriptions of the arguments.

        Keyword Args:
            steps (int, optional): The number of steps to approximate the pulse. Should be at least 16. Defaults to 26.
            sigt (float, optional): The RMS time width of the pulse relative to duration. Approximates a cosine window for :math:`\\sigma_{t} \\approx 0.18` and approaches the time-frequency uncertainty limit for :math:`\\sigma_{t} \\leq 0.13`. Throws an error if not between 0.08 and 0.20. Defaults to 0.11.
        """
        self.duration = duration
        self.amplitude = amplitude
        self.phase = phase
        self.frequency = frequency
        self.centered = centered
        self.sigt = sigt
        self.steps = steps

    @property
    def area(self) -> float:
        self.compile()
        step = self.duration / self.steps
        return step * sum(self.amplitudes) / (self.amplitude * self.duration)

    def compile(self, state: Optional[SequenceState] = None) -> List[RFBlock]:
        validate_parameters(self.duration, self.amplitude, self.phase, self.frequency)
        if self.sigt < 0.08 or self.sigt > 0.2:
            raise ValueError(
                "sigt (currently {}) must be between 0.08 and 0.20.".format(self.sigt)
            )
        if self.steps < 16 or int(self.steps) != self.steps:
            raise ValueError(
                "Steps (currently {}) must be an integer >= 16.".format(self.steps)
            )

        step = self.duration / self.steps
        N = self.steps - 1
        L = self.steps
        n = np.linspace(0, N, self.steps, endpoint=True)

        def G(x):
            return np.exp(-(((x - N / 2.0) / (2 * L * self.sigt)) ** 2))

        self.amplitudes = self.amplitude * (
            G(n) - (G(-0.5) * (G(n + L) + G(n - L))) / (G(L - 0.5) + G(-L - 0.5))
        )
        timestamps = [Timestamp(step, min(1, max(amp, 0))) for amp in self.amplitudes]
        timestamps[0].phase = self.phase
        timestamps[0].frequency = self.frequency
        return RFPulse.center(
            self.centered, timestamps + [Timestamp(0, 0)], self.duration
        )

    def __repr__(self) -> str:
        val = "GaussianPulse({}, {}".format(self.duration, self.amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        if self.frequency is not None:
            val += ", frequency={}".format(self.frequency)
        if self.centered:
            val += ", centered=True"
        if self.steps is not None:
            val += ", steps={}".format(self.steps)
        if self.sigt is not None:
            val += ", sigt={}".format(self.sigt)
        return val + ")"


class FrequencyRamp(RFBlock):
    """
    Linearly ramps the frequency of the RF tone while maintaining constant amplitude and phase.
    """

    def __init__(
        self,
        duration: float,
        amplitude: Optional[float] = None,
        phase: Optional[float] = None,
        start_frequency: Optional[float] = None,
        end_frequency: Optional[float] = None,
        steps: int = 20,
    ):
        """
        Args:
            duration (float): The duration of the ramp in seconds.
            amplitude (float, optional): The amplitude of the tone relative to full scale. Defaults to None.
            phase (float, optional): The phase of the tone in radians. Defaults to None, in which case the previous phase setting is maintained.
            start_frequency (float, optional): The initial frequency in Hertz. Defaults to None, in which case the previous frequency setting is used.
            end_frequency (float, optional): The final frequency in Hertz. Defaults to None, in which case :code:`start_frequency` is used.
            steps (int, optional): The number of frequency steps to include in the ramp. Defaults to 20.
        """
        self.duration = duration
        self.amplitude = amplitude
        self.phase = phase
        self.start_frequency = start_frequency
        self.end_frequency = end_frequency
        self.steps = steps

    def compile(self, state: SequenceState) -> List[RFBlock]:
        validate_parameters(
            self.duration, self.amplitude, self.phase, self.start_frequency
        )
        validate_parameters(frequency=self.end_frequency)
        if self.steps < 2 or self.steps != int(self.steps):
            raise ValueError("The number of steps, {}, must be an integer >= 2")
        if self.start_frequency is None:
            self.start_frequency = state.frequency
        if self.end_frequency is None:
            self.end_frequency = self.start_frequency
        step = self.duration / self.steps
        freqs = np.linspace(self.start_frequency, self.end_frequency, self.steps)
        timestamps = [Timestamp(step, frequency=freq) for freq in freqs]
        timestamps[0].phase = self.phase
        timestamps[0].amplitude = self.amplitude
        return timestamps

    def __repr__(self) -> str:
        val = "FrequencyRamp({}".format(self.duration)
        if self.amplitude is not None:
            val += ", amplitude={}".format(self.amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        if self.start_frequency is not None:
            val += ", start_frequency={}".format(self.start_frequency)
        if self.end_frequency is not None:
            val += ", end_frequency={}".format(self.end_frequency)
        val += ", steps={})".format(self.steps)
        return val


class AmplitudeRamp(RFBlock):
    """
    Linearly ramps the amplitude of the RF tone while maintaining constant frequency and phase.
    """

    def __init__(
        self,
        duration: float,
        start_amplitude: Optional[float] = None,
        end_amplitude: Optional[float] = None,
        phase: Optional[float] = None,
        frequency: Optional[float] = None,
        steps: int = 20,
    ):
        """
        Args:
            duration (float): The duration of the ramp in seconds.
            start_amplitude (float, optional): The initial amplitude, relative to full scale. Defaults to None, in which case the amplitude of the previous :class:`RFBlock` is used.
            end_amplitude (float, optional): The final amplitude, relative to full scale. Defaults to None, in which case :code:`start_amplitude` is used.
            phase (float, optional): The phase of the tone in radians. Defaults to None, in which case the previous phase setting is maintained.
            frequency (float, optional): The frequency of the tone in Hertz. Defaults to None, in which case the previous frequency setting is maintained.
            steps (int, optional): The number of amplitude steps to include in the ramp. Must be at least 2. Defaults to 20.
        """
        self.duration = duration
        self.start_amplitude = start_amplitude
        self.end_amplitude = end_amplitude
        self.phase = phase
        self.frequency = frequency
        self.steps = steps

    def compile(self, state: SequenceState) -> List[RFBlock]:
        validate_parameters(
            self.duration, self.start_amplitude, self.phase, self.frequency
        )
        validate_parameters(amplitude=self.end_amplitude)
        if self.steps < 2 or self.steps != int(self.steps):
            raise ValueError("The number of steps, {}, must be an integer >= 2")
        if self.start_amplitude is None:
            self.start_amplitude = state.amplitude
        if self.end_amplitude is None:
            self.end_amplitude = self.start_amplitude
        step = self.duration / self.steps
        amps = np.linspace(self.start_amplitude, self.end_amplitude, self.steps)
        timestamps = [Timestamp(step, amplitude=amp) for amp in amps]
        timestamps[0].phase = self.phase
        timestamps[0].frequency = self.frequency
        return timestamps

    def __repr__(self) -> str:
        val = "AmplitudeRamp({}".format(self.duration)
        if self.start_amplitude is not None:
            val += ", start_amplitude={}".format(self.start_amplitude)
        if self.end_amplitude is not None:
            val += ", end_amplitude={}".format(self.end_amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        if self.frequency is not None:
            val += ", frequency={}".format(self.frequency)
        val += ", steps={})".format(self.steps)
        return val


class PhaseRamp(RFBlock):
    """
    Linearly ramps the amplitude of the RF tone while maintaining constant frequency and phase.
    """

    def __init__(
        self,
        duration: float,
        start_phase: Optional[float] = None,
        end_phase: Optional[float] = None,
        frequency: Optional[float] = None,
        pd_setpoint: Optional[float] = None,
        pd_selection: Optional[bool] = None,
        clk_shutter: Optional[bool] = None,
        clk_aom: Optional[bool] = None,
        additional_params: Optional[dict] = None,
        dds_amplitude: Optional[float] = None,
        steps: int = 20,
    ):
        """
        Args:
            duration (float): The duration of the ramp in seconds.
            start_phase (float, optional): The initial phase in radians. Defaults to None, in which case the phase of the previous :class:`RFBlock` is used.
            end_phase (float, optional): The final phase in radians. Defaults to None, in which case :code:`start_phase` is used.
            frequency (float, optional): The frequency of the tone in Hertz. Defaults to None, in which case the previous frequency setting is maintained.
            pd_setpoint (float, optional): Clock PD setpoint (the value corresponds to the PD before the atoms and may be converted to the one after the atoms, depending on the value of selected_pd)
            pd_selection (bool, optional): Use PD before/after the chamber as input for the intensity servo
            clk_shutter (bool, optional): Position of the clock laser shutter
            clk_aom (bool, optional): Clock AOM disable / intensity servo integrator hold
            additional_params (dict, optional): Additional Sequencer channels ({"<ch_name>": <value>}, with <ch_name> being the same as the onces referenced in :class:'SequencerMapping)
            dds_amplitude (float, optional): The amplitude of the DDS tone relative to full scale. Defaults to None, in which case the previous ammplitude setting is maintained.
            steps (int, optional): The number of amplitude steps to include in the ramp. Must be at least 2. Defaults to 20.
        """
        self.duration = set_float(duration)
        self.start_phase = set_float(start_phase)
        self.end_phase = set_float(end_phase)
        self.frequency = set_float(frequency)
        self.pd_setpoint = set_float(pd_setpoint)
        self.pd_selection = pd_selection
        self.clk_shutter = clk_shutter
        self.clk_aom = clk_aom
        self.additional_params = additional_params
        self.dds_amplitude = set_float(dds_amplitude)
        self.steps = steps

    def compile(self, state: SequenceState) -> List[RFBlock]:
        validate_parameters(
            self.duration,
            self.start_phase,
            self.frequency,
            self.pd_setpoint,
            self.additional_params,
            self.dds_amplitude,
        )
        validate_parameters(phase=self.end_phase)
        if self.steps < 2 or self.steps != int(self.steps):
            raise ValueError("The number of steps, {}, must be an integer >= 2")
        if self.start_phase is None:
            self.start_phase = state.phase
        if self.end_phase is None:
            self.end_phase = self.start_phase
        step = self.duration / self.steps
        phis = np.linspace(self.start_phase, self.end_phase, self.steps)
        timestamps = [Timestamp(step, phase=phi) for phi in phis]
        timestamps[0].frequency = self.frequency
        timestamps[0].pd_setpoint = self.pd_setpoint
        timestamps[0].pd_selection = self.pd_selection
        timestamps[0].clk_shutter = self.clk_shutter
        timestamps[0].clk_aom = self.clk_aom
        timestamps[0].additional_params = self.additional_params
        timestamps[0].dds_amplitude = self.dds_amplitude
        return timestamps

    def __repr__(self) -> str:
        val = "PhaseRamp({}".format(self.duration)
        if self.start_phase is not None:
            val += ", start_phase={}".format(self.start_phase)
        if self.end_phase is not None:
            val += ", end_phase={}".format(self.end_phase)
        if self.frequency is not None:
            val += ", frequency={}".format(self.frequency)
        if self.pd_setpoint is not None:
            val += ", pd_setpoint={}".format(self.pd_setpoint)
        if self.pd_selection is not None:
            val += ", pd_selection={}".format(self.pd_selection)
        if self.clk_shutter is not None:
            val += ", clk_shutter={}".format(self.clk_shutter)
        if self.clk_aom is not None:
            val += ", clk_aom={}".format(self.clk_shutter)
        if self.additional_params is not None:
            val += ", additional_params={}".format(self.additional_params)
        if self.dds_amplitude is not None:
            val += ", dds_amplitude={}".format(self.dds_amplitude)
        val += ", steps={})".format(self.steps)
        return val


class Transition:
    """
    Describes the calibrated frequency and Rabi frequencies for a transition. Used in :class:`SetTransition` to set parameters for :func:`AreaPulse`.
    """

    def __init__(
        self,
        frequency: float,
        amplitudes,
        Rabi_frequencies=None,
        default_amplitude: Optional[float] = None,
        frequency_offset: float = 0,
    ) -> None:
        """
        Args:
            frequency (float): The frequency of the transition in Hertz.
            amplitudes (dict or list of float): A list of amplitudes (relative to full scale) for which the Rabi frequencies are calibrated. Linearly interpolates and extrapolates relative to specified amplitudes. Can also take a dictionary with amplitude keys and Rabi frequency values, in which case Rabi_frequencies is ignored.
            Rabi_frequencies (list of float, optional): A list of Rabi frequencies (in Hertz) corresponding to :code:`amplitudes`. Must be the same length as :code:`amplitudes` if lists are used. Defaults to None.
            default_amplitude (float, optional): The default amplitude for pulses on the transition. Defaults to None, in which case the first element of amplitudes is used.
            frequency_offset (float, optional): The frequency (in Hertz) of the tone that is mixed with the synthesizer output. The actual output frequency of the synthesizer is :code:`frequency - frequency_offset`. Defaults to 0.
        """
        if isinstance(amplitudes, dict):
            amplitudes_list = []
            Rabi_frequencies = []
            for k, v in amplitudes.items():
                amplitudes_list.append(k)
                Rabi_frequencies.append(v)
            amplitudes = amplitudes_list
        if len(amplitudes) == 0 or len(Rabi_frequencies) != len(amplitudes):
            raise ValueError(
                "amplitudes and Rabi_frequencies must be non-empty arrays of the same length."
            )
        for a in amplitudes:
            if a <= 0 or a > 1:
                raise ValueError(
                    "All amplitudes must be > 0 and <= 1; {} isn't.".format(a)
                )
        for f in Rabi_frequencies:
            if f <= 0:
                raise ValueError(
                    "All Rabi frequencies must be positive; {} isn't.".format(f)
                )
        if default_amplitude is not None and (
            default_amplitude <= 0 or default_amplitude > 1
        ):
            raise ValueError(
                "Default amplitude {} must be > 0 and <= 1".format(default_amplitude)
            )
        if (
            np.abs(frequency - frequency_offset) < 0
            or np.abs(frequency - frequency_offset) > dds_settings.F_MAX
        ):
            raise ValueError(
                "The output frequency (frequency {} - frequency_offset {}) must be between 0 and {} but is {}".format(
                    frequency,
                    frequency_offset,
                    dds_settings.F_MAX,
                    np.abs(frequency - frequency_offset),
                )
            )
        self.frequency = frequency
        self.amplitudes = amplitudes
        self.Rabi_frequencies = Rabi_frequencies
        if default_amplitude is None:
            default_amplitude = amplitudes[0]
        self.default_amplitude = default_amplitude

        self.frequency_offset = frequency_offset
        if len(self.amplitudes) > 1:
            itp = interp1d(
                self.amplitudes,
                self.Rabi_frequencies,
                copy=False,
                fill_value="extrapolate",
            )
            self.default_Rabi_frequency = itp(self.default_amplitude)
        else:
            self.default_Rabi_frequency = Rabi_frequencies[0]

    def __repr__(self) -> str:
        return (
            "Transition({}, {}, {}, default_amplitude={}, frequency_offset={})".format(
                self.frequency,
                self.amplitudes,
                self.Rabi_frequencies,
                self.default_amplitude,
                self.frequency_offset,
            )
        )

    def Rabi_frequency(self, amplitude: Optional[float] = None) -> float:
        """
        Rabi_frequency(self, amplitude=None)

        Computes the Rabi frequency corresponding to :code:`amplitude` using interpolation or extrapolation from the values provided by :code:`amplitudes` and :code:`Rabi_frequencies`.

        Args:
            amplitude (float, optional): The amplitude for which to compute the Rabi frequency. Defaults to None, in which case :code:`default_amplitude` is used.

        Returns:
            float: The Rabi frequency, in Hertz, associated with :code:`amplitude`.
        """
        if amplitude is None:
            amplitude = self.default_amplitude
        if amplitude <= 0 or amplitude > 1:
            raise ValueError("Amplitude {} must be > 0 and <= 1".format(amplitude))
        if len(self.amplitudes) > 1:
            itp = interp1d(
                self.amplitudes,
                self.Rabi_frequencies,
                copy=False,
                fill_value="extrapolate",
            )
            return itp(amplitude)
        else:
            return self.default_Rabi_frequency


class SetTransition(RFBlock):
    """
    Sets the transition to be used for subsequent :meth:`AreaPulse` commands.
    """

    atomic = True

    def __init__(self, transition: Transition) -> None:
        """
        Args:
            transition (Transition): The transition to use for the following :meth:`AreaPulse` commands.
        """
        self.transition = transition

    def __repr__(self) -> str:
        return "SetTransition({})".format(self.transition)

    def compile(self, state: SequenceState) -> RFBlock:
        state.transition = self.transition
        state.frequency = np.abs(
            self.transition.frequency - self.transition.frequency_offset
        )
        return super().compile(state)


#def todB(amplitude_lin):
#    """
#    todB(amplitude_lin)
#
#    Converts an amplitude ratio from linear to decibels per :math:`A_{dB} = 20 \\log_{10}(A)`.
#
#    Args:
#        amplitude_lin (float): An amplitude ratio.
#
#    Returns:
#        float: The amplitude ratio in decibels.
#    """
#    return 20.0 * np.log10(amplitude_lin)


#def fromdB(amplitude_dB):
#    """
#    fromdB(amplitude_dB)
#
#    Converts an amplitude ratio from decibels to linear per :math:`A = 10^{A_{dB}/20}`.
#
#    Args:
#        amplitude_lin (float): An amplitude ratio in decibels.
#
#    Returns:
#        float: The amplitude ratio.
#    """
#    return 10 ** (amplitude_dB / 20)


def Pulse(
    duration: float,
    amplitude: float,
    phase: Optional[float] = None,
    frequency: Optional[float] = None,
    centered: bool = False,
    window: type[RFPulse] = RectangularPulse,
    **kwargs,
) -> RFPulse:
    """
    Pulse(duration, amplitude, phase=None, frequency=None, centered=False, window=RectangularPulse, **kwargs)

    Low level function for generating an RF pulse. Provides a unified constructor for all subclasses of :class:`RFPulse`. See also :func:`AreaPulse` for a higher level interface to pulses on a specified :class:`Transition`.

    Args:
        duration (float): The duration of the pulse in seconds.
        amplitude (float): The peak amplitude of the pulse, relative to full scale.
        phase (float, optional): The phase of the pulse in radians. Defaults to None, in which case the previous phase setting is maintained.
        frequency (float, optional): The frequency of the pulse in Hertz. Defaults to None, in which case the previous frequency setting is maintained.
        centered (bool, optional): Whether to reduce the duration of the preceding and following :class:`Wait` commands :code:`duration/2`. Will throw an error during compilation if the :class:`Wait` commands are too short or the pulse is not adjacent to at least one :class:`Wait` command. If there is only one neighboring :class:`Wait` command, its duration is reduced by :code:`duration/2`. Defaults to False.
        window (RFPulse, optional): The shape of the pulse. Defaults to RectangularPulse.
        **kwargs: Additional keyword arguments, which are passed to :code:`window`'s :code:`__init__` method

    Returns:
        RFPulse: An :class:`RFPulse` with the specified parameters
    """
    return window(duration, amplitude, phase, frequency, centered, **kwargs)


class AreaPulse(RFPulse):
    """
    Class for generating an RF pulse on a specified :class:`Transition`, which must be set by a :class:`SetTransition` command before the first :func:`AreaPulse`. The pulse timing is calculated to provide the specified pulse :code:`area`. See also :func:`Pulse` for a low level function for generating pulses with manually specified frequency, amplitude, and duration.
    """

    def __init__(
        self,
        pulse_area: float,
        amplitude: Optional[float] = None,
        phase: Optional[float] = None,
        frequency: Optional[float] = None,
        centered: bool = False,
        window: type[RFPulse] = RectangularPulse,
        **kwargs,
    ) -> None:
        """
        Args:
            pulse_area (float): The pulse area in radians.
            amplitude (float, optional): The peak amplitude of the pulse, relative to full scale. Defaults to None, in which case the default amplitude for the specified :class:`Transition` is used.
            phase (float, optional): The phase of the pulse in radians. Defaults to None, in which case the previous phase setting is maintained.
            centered (bool, optional): Whether to reduce the duration of the preceding and following :class:`Wait` commands :code:`duration/2`. Will throw an error during compilation if the :class:`Wait` commands are too short or the pulse is not adjacent to at least one :class:`Wait` command. If there is only one neighboring :class:`Wait` command, its duration is reduced by :code:`duration/2`. Defaults to False.
            window (RFPulse, optional): The shape of the pulse. Defaults to RectangularPulse.
            **kwargs: Additional keyword arguments, which are passed to window's :code:`__init__` method
        """
        self.pulse_area = pulse_area
        self.amplitude = amplitude
        self.phase = phase
        self.frequency = frequency
        self.centered = centered
        self.window = window
        self.kwargs = kwargs

    def compile(self, state: SequenceState) -> List[RFPulse]:
        if issubclass(self.window, AreaPulse):
            return self.window(
                self.pulse_area,
                self.amplitude,
                self.phase,
                self.centered,
                **self.kwargs,
            ).compile(state)
        transition = state.transition
        if self.frequency is None:
            self.frequency = transition.frequency
        if self.amplitude is None:
            self.amplitude = transition.default_amplitude
        if self.amplitude <= 0 or self.amplitude > 1:
            raise ValueError("Amplitude {} must be > 0 and <= 1".format(self.amplitude))
        if self.pulse_area < 0:
            raise ValueError(
                "Pulse area {} must be non-negative".format(self.pulse_area)
            )
        validate_parameters(phase=self.phase)
        if self.pulse_area == 0:
            return [Wait(0)]
        Rabi_frequency = transition.Rabi_frequency(self.amplitude)
        rect_pulse_duration = self.pulse_area / (2 * np.pi * Rabi_frequency)
        pulse = Pulse(
            1,
            self.amplitude,
            self.phase,
            np.abs(self.frequency - transition.frequency_offset),
            self.centered,
            self.window,
            **self.kwargs,
        )
        pulse.duration = rect_pulse_duration / pulse.area
        return [pulse]

    def __repr__(self) -> str:
        val = "AreaPulse({}".format(self.pulse_area)
        if self.amplitude is not None:
            val += ", amplitude={}".format(self.amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        val += ", centered={}, window={}".format(self.centered, self.window)
        if len(self.kwargs) > 0:
            val += ", {}".format(self.kwargs)
        val += ")"
        return val


def PiPulse(
    amplitude: Optional[float] = None,
    phase: Optional[float] = None,
    frequency: Optional[float] = None,
    centered: bool = False,
    window: type[RFPulse] = RectangularPulse,
    **kwargs,
) -> AreaPulse:
    """
    PiPulse(amplitude=None, phase=None, centered=False, window=RectangularPulse, **kwargs)

    A wrapper for :func:`AreaPulse` with pulse area set to pi. Refer to :func:`AreaPulse` for full documentation.
    """
    return AreaPulse(
        np.pi,
        amplitude=amplitude,
        phase=phase,
        frequency=frequency,
        centered=centered,
        window=window,
        **kwargs,
    )


def PiOver2Pulse(
    amplitude: Optional[float] = None,
    phase: Optional[float] = None,
    frequency: Optional[float] = None,
    centered: bool = False,
    window: type[RFPulse] = RectangularPulse,
    **kwargs,
) -> AreaPulse:
    """
    PiOver2Pulse(amplitude=None, phase=None, centered=False, window=RectangularPulse, **kwargs)

    A wrapper for :func:`AreaPulse` with pulse area set to pi/2. Refer to :func:`AreaPulse` for full documentation.
    """
    return AreaPulse(
        np.pi / 2,
        amplitude=amplitude,
        phase=phase,
        frequency=frequency,
        centered=centered,
        window=window,
        **kwargs,
    )


class BB1(AreaPulse):
    """
    Generates a `BB1 <https://doi.org/10.1006/jmra.1994.1159>`_ robust composite pulse.
    """

    def compile(self, state: SequenceState) -> List[RFPulse]:
        if self.phase is None:
            self.phase = state.phase
        phi1 = np.arccos(-self.pulse_area / (2 * np.pi))
        phi2 = 3 * phi1
        pulses = [
            PiPulse(
                self.amplitude, self.phase + phi1, False, self.window, **self.kwargs
            ),
            AreaPulse(
                2 * np.pi,
                self.amplitude,
                self.phase + phi2,
                False,
                self.window,
                **self.kwargs,
            ),
            PiPulse(
                self.amplitude, self.phase + phi1, False, self.window, **self.kwargs
            ),
            AreaPulse(
                self.pulse_area,
                self.amplitude,
                self.phase,
                False,
                self.window,
                **self.kwargs,
            ),
        ]
        self.duration = 0
        for p in pulses:
            self.duration += deepcopy(p).compile(deepcopy(state))[0].duration
        return AreaPulse.center(self.centered, pulses, self.duration)

    def __repr__(self) -> str:
        val = "BB1({}".format(self.pulse_area)
        if self.amplitude is not None:
            val += ", amplitude={}".format(self.amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        val += ", centered={}, window={}".format(self.centered, self.window)
        if len(self.kwargs) > 0:
            val += ", {}".format(self.kwargs)
        val += ")"
        return val


class CORPSE(AreaPulse):
    """
    Generates a `CORPSE <https://doi.org/10.1103/PhysRevA.67.042308>`_ robust composite pulse.
    """

    def compile(self, state: SequenceState) -> List[RFPulse]:
        if self.phase is None:
            self.phase = state.phase
        theta = self.pulse_area
        theta1 = 2 * np.pi + theta / 2.0 - np.arcsin(np.sin(theta / 2.0) / 2.0)
        theta2 = 2 * np.pi - 2 * np.arcsin(np.sin(theta / 2.0) / 2.0)
        theta3 = theta / 2.0 - np.arcsin(np.sin(theta / 2.0) / 2.0)
        pulses = [
            AreaPulse(
                theta1,
                self.amplitude,
                self.phase,
                self.centered,
                self.window,
                **self.kwargs,
            ),
            AreaPulse(
                theta2,
                self.amplitude,
                self.phase + np.pi,
                self.centered,
                self.window,
                **self.kwargs,
            ),
            AreaPulse(
                theta3,
                self.amplitude,
                self.phase,
                self.centered,
                self.window,
                **self.kwargs,
            ),
        ]
        self.duration = 0
        for p in pulses:
            self.duration += deepcopy(p).compile(deepcopy(state))[0].duration
        return AreaPulse.center(self.centered, pulses, self.duration)

    def __repr__(self) -> str:
        val = "CORPSE({}".format(self.pulse_area)
        if self.amplitude is not None:
            val += ", amplitude={}".format(self.amplitude)
        if self.phase is not None:
            val += ", phase={}".format(self.phase)
        val += ", centered={}, window={}".format(self.centered, self.window)
        if len(self.kwargs) > 0:
            val += ", {}".format(self.kwargs)
        val += ")"
        return val


def SpinEcho(duration: float, pulse: Optional[RFPulse] = None) -> List[RFBlock]:
    """
    SpinEcho(duration, pulse=None)

    Returns a list of pulses and :class:`Wait` commands implementing a spin echo decoupling sequence consisting of a `duration/2` :class:`Wait`, a pi pulse about the :code:`x` axis and another :code:`duration/2` :class:`Wait`.

    Args:
        duration (float): The duration of the decoupling sequence in seconds.
        pulse (RFPulse, optional): The pulse to use for the pi pulses in the decoupling sequence. Should normally be generated by :func:`PiPulse` or be a subclass of :class:`RFPulse`. The phase of the pulse is overridden in the sequence. Defaults to None, in which case a :class:`RectangularPulse` with the default amplitude and frequency for the selected :class:`Transition` is used.

    Returns:
        list of :class:`RFBlock`: Returns a list of pulses and :class:`Wait` commands implementing a spin echo decoupling sequence.
    """
    if pulse is None:
        pulse = PiPulse(phase=0, centered=True)
    elif isinstance(pulse, type) and issubclass(pulse, RFPulse):
        pulse = PiPulse(window=pulse, centered=True)
    else:
        pulse.phase = 0
    return [Wait(duration / 2), pulse, Wait(duration / 2)]


def XY8(duration: float, pulse: RFPulse = None) -> List[RFBlock]:
    """
    XY8(duration, pulse=None)

    Returns a list of pulses and :class:`Wait` commands implementing an XY8 decoupling sequence. Refer to `this review <https://doi.org/10.1098/rsta.2011.0355>`_ for information about the XY8 pulse sequence.

    Args:
        duration (float): The duration of the decoupling sequence in seconds.
        pulse (RFPulse, optional): The pulse to use for the pi pulses in the decoupling sequence. Should normally be generated by :func:`PiPulse` or be a subclass of :class:`RFPulse`. The phase of the pulses are overridden in the sequence. Defaults to None, in which case a :class:`RectangularPulse` with the default amplitude and frequency for the selected :class:`Transition` is used.

    Returns:
        list of :class:`RFBlock`: Returns a list of pulses and :class:`Wait` commands implementing an XY8 decoupling sequence.
    """
    if pulse is None:
        pulse = PiPulse(phase=0, centered=True)
    elif isinstance(pulse, type) and issubclass(pulse, RFPulse):
        pulse = PiPulse(window=pulse, centered=True)

    def phased_pulse(phase):
        new_pulse = copy(pulse)
        new_pulse.phase = phase
        return new_pulse

    phases = [0, np.pi / 2, 0, np.pi / 2, np.pi / 2, 0, np.pi / 2, 0]  # XYXYYXYX
    return (
        [Wait(duration / 16)]
        + [
            f(phi)
            for phi in phases
            for f in (phased_pulse, lambda x: Wait(duration / 8))
        ][:-1]
        + [Wait(duration / 16)]
    )


def XY16(duration: float, pulse: Optional[RFPulse] = None) -> List[RFBlock]:
    """
    XY16(duration, pulse=None)

    Returns a list of pulses and :class:`Wait` commands implementing an XY16 decoupling sequence. Refer to `this review <https://doi.org/10.1098/rsta.2011.0355>`_ for information about the XY8 pulse sequence.

    Args:
        duration (float): The duration of the decoupling sequence in seconds.
        pulse (RFPulse, optional): The pulse to use for the pi pulses in the decoupling sequence. Should normally be generated by :func:`PiPulse` or be a subclass of :class:`RFPulse`. The phase of the pulses are overridden in the sequence. Defaults to None, in which case a :class:`RectangularPulse` with the default amplitude and frequency for the selected :class:`Transition` is used.

    Returns:
        list of :class:`RFBlock`: Returns a list of pulses and :class:`Wait` commands implementing an XY16 decoupling sequence.
    """
    if pulse is None:
        pulse = PiPulse(phase=0, centered=True)
    elif isinstance(pulse, type) and issubclass(pulse, RFPulse):
        pulse = PiPulse(window=pulse, centered=True)

    def phased_pulse(phase):
        new_pulse = copy(pulse)
        new_pulse.phase = phase
        return new_pulse

    phases = [
        0,
        np.pi / 2,
        0,
        np.pi / 2,
        np.pi / 2,
        0,
        np.pi / 2,
        0,
        np.pi,
        3 * np.pi / 2,
        np.pi,
        3 * np.pi / 2,
        3 * np.pi / 2,
        np.pi,
        3 * np.pi / 2,
        np.pi,
    ]  # XYXYYXYX-X-Y-X-Y-Y-X-Y-X
    return (
        [Wait(duration / 32)]
        + [
            f(phi)
            for phi in phases
            for f in (phased_pulse, lambda x: Wait(duration / 16))
        ][:-1]
        + [Wait(duration / 32)]
    )


class KDD:
    """
    KDD(duration, pulse=None)

    Returns a list of pulses and :class:`Wait` commands implementing a KDD decoupling sequence. Refer to `this review <https://doi.org/10.1098/rsta.2011.0355>`_ and `this paper <https://journals.aps.org/prl/pdf/10.1103/PhysRevLett.106.240501>`_ for information about the KDD pulse sequence.

    Args:
        duration (float): The duration of the decoupling sequence in seconds.
        pulse (RFPulse, optional): The pulse to use for the pi pulses in the decoupling sequence. Should normally be generated by :func:`PiPulse` or be a subclass of :class:`RFPulse`. The phase of the pulses are overridden in the sequence. Defaults to None, in which case a :class:`RectangularPulse` with the default amplitude and frequency for the selected :class:`Transition` is used.

    Returns:
        list of :class:`RFBlock`: Returns a list of pulses and :class:`Wait` commands implementing a KDD decoupling sequence.
    """

    def __init__(self, duration: float, pulse: Optional[RFPulse] = None) -> None:
        self.duration = duration
        self.pulse = pulse

    def __repr__(self) -> str:
        return f"KDD({self.duration.__repr__()}, {self.pulse.__repr__()})"

    def compile(self, state: SequenceState) -> List[RFBlock]:
        if self.pulse is None:
            self.pulse = PiPulse(phase=0, centered=True)
        elif isinstance(self.pulse, type) and issubclass(self.pulse, RFPulse):
            self.pulse = PiPulse(window=self.pulse, centered=True)

        def phased_pulse(phase):
            new_pulse = copy(self.pulse)
            new_pulse.phase = phase
            return new_pulse

        tau = self.duration / 20.0

        def KDDphi(phi):
            return [
                Wait(tau / 2.0),
                phased_pulse(np.pi / 6 + phi),
                Wait(tau),
                phased_pulse(phi),
                Wait(tau),
                phased_pulse(np.pi / 2 + phi),
                Wait(tau),
                phased_pulse(phi),
                Wait(tau),
                phased_pulse(np.pi / 6 + phi),
                Wait(tau / 2.0),
            ]

        return KDDphi(0) + KDDphi(np.pi / 2) + KDDphi(0) + KDDphi(np.pi / 2)


def WAHUHA(duration: float, pulse: RFPulse = None):
    if pulse is None:
        pulse = PiOver2Pulse()

    def phased_pulse(phase, area):
        new_pulse = copy(pulse)
        new_pulse.phase = phase
        new_pulse.pulse_area = area
        new_pulse.centered = True
        return new_pulse

    sequence = [
        Wait(duration / 8),
        phased_pulse(np.pi, np.pi / 2),
        Wait(duration / 4),
        phased_pulse(0, np.pi / 2),
        Wait(duration / 8),
        phased_pulse(0, np.pi),
        Wait(duration / 8),
        phased_pulse(np.pi, np.pi / 2),
        Wait(duration / 4),
        phased_pulse(0, np.pi / 2),
        Wait(duration / 8),
    ]

    return sequence


def DROID60(duration: float, pulse: RFPulse = None):
    if pulse is None:
        pulse = PiOver2Pulse()

    def phased_pulse(phase, area):
        new_pulse = copy(pulse)
        new_pulse.phase = phase
        new_pulse.pulse_area = area
        new_pulse.centered = False
        return new_pulse

    def px():
        return phased_pulse(0, np.pi)

    def p2x():
        return phased_pulse(0, np.pi / 2)

    def py():
        return phased_pulse(np.pi / 2, np.pi)

    def p2y():
        return phased_pulse(np.pi / 2, np.pi / 2)

    def mpx():
        return phased_pulse(np.pi, np.pi)

    def mp2x():
        return phased_pulse(np.pi, np.pi / 2)

    def mpy():
        return phased_pulse(3 * np.pi / 2, np.pi)

    def mp2y():
        return phased_pulse(3 * np.pi / 2, np.pi / 2)

    def w():
        return Wait(duration / 48)

    seq = [
        w(),
        px(),
        w(),
        p2x(),
        mp2y(),
        w(),
        mpx(),
        w(),
        mpx(),
        w(),
        px(),
        w(),
        p2x(),
        mp2y(),
        w(),
        mpx(),
        w(),
        mpx(),
        w(),
        px(),
        w(),
        p2x(),
        mp2y(),
        w(),
        mpx(),
        w(),
        mpx(),
        w(),
        mpy(),
        w(),
        mp2y(),
        p2x(),
        w(),
        py(),
        w(),
        py(),
        w(),
        mpy(),
        w(),
        mp2y(),
        p2x(),
        w(),
        py(),
        w(),
        py(),
        w(),
        mpy(),
        w(),
        mp2y(),
        p2x(),
        w(),
        py(),
        w(),
        py(),
        w(),
        mpy(),
        w(),
        p2x(),
        p2y(),
        w(),
        py(),
        w(),
        mpy(),
        w(),
        mpy(),
        w(),
        p2x(),
        p2y(),
        w(),
        py(),
        w(),
        mpy(),
        w(),
        mpy(),
        w(),
        p2x(),
        p2y(),
        w(),
        py(),
        w(),
        mpx(),
        w(),
        mpx(),
        w(),
        p2y(),
        p2x(),
        w(),
        px(),
        w(),
        mpx(),
        w(),
        mpx(),
        w(),
        p2y(),
        p2x(),
        w(),
        px(),
        w(),
        mpx(),
        w(),
        mpx(),
        w(),
        p2y(),
        p2x(),
        w(),
        px(),
        w(),
        mpy(),
    ]
    return seq


def WAHUHA_echo(duration: float, pulse: RFPulse = None):
    if pulse is None:
        pulse = PiOver2Pulse()

    def phased_pulse(phase, area):
        new_pulse = copy(pulse)
        new_pulse.phase = phase
        new_pulse.pulse_area = area
        new_pulse.centered = False
        return new_pulse

    def px():
        return phased_pulse(0, np.pi)

    def p2x():
        return phased_pulse(0, np.pi / 2)

    def py():
        return phased_pulse(np.pi / 2, np.pi)

    def p2y():
        return phased_pulse(np.pi / 2, np.pi / 2)

    def mpx():
        return phased_pulse(np.pi, np.pi)

    def mp2x():
        return phased_pulse(np.pi, np.pi / 2)

    def mpy():
        return phased_pulse(3 * np.pi / 2, np.pi)

    def mp2y():
        return phased_pulse(3 * np.pi / 2, np.pi / 2)

    def w():
        return Wait(duration / 6)

    seq = [w(), p2x(), w(), mp2y(), w(), py(), w(), p2y(), w(), p2x(), w(), mpx()]
    return seq


def Ramsey(
    duration: float,
    phase: float = 0,
    pulse: RFPulse = None,
    decoupling: List[RFPulse | Wait] = None,
) -> List[RFBlock]:
    """
    Ramsey(duration, phase, pulse=None, decoupling=None)

    Returns a list of pulses and :class:`Wait` commands implementing a Ramsey interferometry sequence, consisting of a pi/2 pulse with zero phase, a :class:`Wait` of length :code:`duration`, and a final pi/2 pulse with phase :code:`phase`. A decoupling sequence can optionally be inserted instead of the :class:`Wait`.

    Args:
        duration (float): The dark time (in seconds) for the Ramsey sequence.
        phase (float, optional): The phase of the final pulse. Defaults to 0.
        pulse (RFPulse, optional): The pulse to use for the pi/2 pulses in the Ramsey sequence. Should normally be generated by :func:`PiOver2Pulse` or be a subclass of :class:`RFPulse`. The phase of the pulses are overridden in the sequence. Defaults to None, in which case a :class:`RectangularPulse` with the default amplitude and frequency for the selected :class:`Transition` is used.
        decoupling (list of :class:`RFBlock`, optional): A decoupling sequence (generated by :func:`XY8`, for example) to insert during the dark time. The duration of :class:`Wait` commands is adjusted to make the total length equal to :code:`duration`. Must only contain :class:`RFPulse` and :class:`Wait` blocks. Defaults to None.

    Returns:
        list of :class:`RFBlock`: Returns a list of pulses and :class:`Wait` commands implementing a Ramsey sequence.
    """
    if decoupling == None:
        decoupling = [Wait(duration)]
    else:
        decoupling = deepcopy(decoupling)
        decoupling_duration = 0
        for b in decoupling:
            if isinstance(b, Wait):
                decoupling_duration += b.duration
            elif isinstance(b, RFPulse):
                b.centered = True
            else:
                raise TypeError(
                    "Only RFPulse and Wait are allowed in the decoupling sequence. {} was included.".format(
                        b
                    )
                )
        for b in decoupling:
            if isinstance(b, Wait):
                b.duration *= duration / decoupling_duration
    if pulse is None:
        pulse = PiOver2Pulse()
    elif isinstance(pulse, type) and issubclass(pulse, RFPulse):
        pulse = PiPulse(window=pulse, centered=True)
    else:
        pulse.phase = 0
    end_pulse = copy(pulse)
    end_pulse.phase = phase
    return [pulse] + decoupling + [end_pulse]


class Repeat(RFBlock):
    def __init__(self, sequence: List[RFBlock], repetitions: int) -> None:
        self.sequence = sequence
        self.repetitions = repetitions

    def __repr__(self) -> str:
        return "Repeat({}, {})".format(self.sequence, self.repetitions)

    def compile(self, state: SequenceState) -> List[RFBlock]:
        return [deepcopy(self.sequence) for _ in range(self.repetitions)]


def compile_sequence(
    sequence: List[RFBlock], output_json: bool = True
) -> List[RFBlock] | str:
    """
    compile_sequence(sequence)

    Compilation steps:
        * Compiles instance of :class:`RFBlock` with :code:`compile` functions
        * Updates durations based on :class:`AdjustPrevDuration` and :class:`AdjustNextDuration`
        * Replaces :class:`SyncPoint` blocks with  :class:`Wait` blocks.
        * Converts timestamps from relative to absolute time
        * Computes durations of each section of the sequence
        * Outputs the sequence in a list of serializable dictionaries that can be sent to the synthesizer server.

    Args:
        sequence (dictionary of lists of :class:`RFBlock`): The sequence to compile. Keys should be channels, values should be list of :class:`RFBlock`.
        output_json (bool): Outputs a JSON-formatted string of timestamos that can be sent to :class:`synthesizer.synthesizer_server` if True, or a list of :class:`RFBlock` if False. Defaults to True.

    Returns
        ((List[RFBlock] | str), Dict[int : List[float]]): A tuple containing the compiled sequence and a list of lists the durations of the sequences for each channel
    """

    compiled = {}
    all_durations = {}

    sequence = deepcopy(sequence)
    for channel, stack in sequence.items():  # iterate DDS output channels
        stack.reverse()  # allow removing elements in chronological order by extracting them from the end of the list (reduces complexity(?))
        state = SequenceState()
        compiled_channel = []
        while len(stack) > 0:  # iterate trigger segments within the sequence
            head = stack.pop()
            if isinstance(head, List):
                head.reverse()  # ensure same order as stack
                stack += head
                continue
            if hasattr(head, "atomic") and head.atomic:  # process single pulse
                block = head.compile(state)
                if (
                    len(compiled_channel) > 0
                    and isinstance(compiled_channel[-1], AdjustNextDuration)
                    and not isinstance(block, Timestamp)
                ):
                    raise TypeError(
                        "{} must be followed by a Timestamp, but is followed by {}".format(
                            compiled_channel[-1], block
                        )
                    )
                if isinstance(block, SyncPoint):
                    raise (NotImplementedError())
                elif isinstance(block, SetTransition):
                    pass
                elif isinstance(block, AdjustPrevDuration):
                    if len(compiled_channel) == 0:
                        pass
                    elif not isinstance(compiled_channel[-1], Timestamp):
                        raise TypeError(
                            "{} must follow a Timestamp, but follows {}".format(
                                block, compiled_channel[-1]
                            )
                        )
                    elif -block.duration > compiled_channel[-1].duration:
                        raise ValueError(
                            "{} would make the duration of {} negative".format(
                                block, compiled_channel[-1]
                            )
                        )
                    else:
                        compiled_channel[-1].duration += block.duration
                elif isinstance(block, Timestamp):
                    if len(compiled_channel) > 0 and isinstance(
                        compiled_channel[-1], AdjustNextDuration
                    ):
                        adjust_next = compiled_channel.pop()
                        if -adjust_next.duration > block.duration:
                            raise ValueError(
                                "{} would make the duration of {} negative".format(
                                    adjust_next, block
                                )
                            )
                        else:
                            block.duration += adjust_next.duration

                    # adjust remaining None entries
                    if block.phase is None:
                        block.phase = state.phase
                    if block.frequency is None:
                        block.frequency = state.frequency
                    if block.pd_setpoint is None:
                        block.pd_setpoint = state.pd_setpoint
                    if block.pd_selection is None:
                        block.pd_selection = state.pd_selection
                    if block.clk_shutter is None:
                        block.clk_shutter = state.clk_shutter
                    if block.clk_aom is None:
                        block.clk_aom = state.clk_aom
                    if block.additional_params is None:
                        block.additional_params = state.additional_params
                    if block.dds_amplitude is None:
                        block.dds_amplitude = state.dds_amplitude

                    if block.duration > 0:
                        compiled_channel.append(block)
                    elif block.dds_wait_for_trigger:
                        if block.duration == 0:
                            block.duration = dds_settings.T_MIN
                        compiled_channel.append(block)
                    elif (
                        block.duration == 0
                        and len(stack) > 0
                        and isinstance(stack[-1], Timestamp)
                        and stack[-1].dds_wait_for_trigger
                    ):
                        block.duration = dds_settings.T_MIN
                        compiled_channel.append(block)
                    block.dds_digital_out = state.dds_digital_out
                elif isinstance(block, AdjustNextDuration):
                    compiled_channel.append(block)
                else:
                    raise TypeError("Cannot add a {} to the sequence".format(block))
            else:  # process composite pulse sequence
                blocks = head.compile(state)
                blocks.reverse()  # ensure same order as stack
                stack.extend(blocks)
        durations = []
        duration = 0.
        compiled_channel = [b for b in compiled_channel if isinstance(b, Timestamp)]
        for block in compiled_channel:
            if block.dds_wait_for_trigger:
                durations.append(duration)
                duration = 0
            block.duration, duration = duration, block.duration + duration
            if duration > dds_settings.T_MAX:
                raise ValueError(
                    "The duration {} s of channel {}'s sequence exceeds the maximum duration of {} s after {}".format(
                        duration, channel, dds_settings.T_MAX, block
                    )
                )
        durations.append(duration)
        if len(compiled_channel) > 0 and compiled_channel[-1].duration != duration:
            compiled_channel.append(
                Timestamp(
                    duration,
                    phase=state.phase,
                    frequency=state.frequency,
                    pd_setpoint=state.pd_setpoint,
                    pd_selection=state.pd_selection,
                    clk_shutter=state.clk_shutter,
                    clk_aom=state.clk_aom,
                    additional_params=state.additional_params,
                    dds_amplitude=state.dds_amplitude,
                    dds_digital_out=state.dds_digital_out,
                )
            )
        terminator = Timestamp(0, 0, 0, 0, dds_amplitude=0, dds_digital_out=[False] * dds_settings.N_DIGITAL)
        terminator.phase_update = 0
        compiled_channel.append(terminator)
        if len(compiled_channel) > dds_settings.N_ADDRESSES:
            raise ValueError(
                "The length {} of channel {}'s sequence exceeds the maximum length of {}".format(
                    len(compiled_channel), channel, dds_settings.N_ADDRESSES
                )
            )
        compiled[channel] = compiled_channel
        all_durations[channel] = durations

    if output_json:
        class RFBlockEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Timestamp):
                    return {
                        "timestamp": obj.duration,
                        "phase": obj.phase,
                        "frequency": obj.frequency,
                        "pd_setpoint": obj.pd_setpoint,
                        "pd_selection": obj.pd_selection,
                        "clk_shutter": obj.clk_shutter,
                        "clk_aom": obj.clk_aom,
                        "additional_params": obj.additional_params,
                        "dds_amplitude": obj.dds_amplitude,
                        "dds_phase_update": obj.dds_phase_update,
                        "dds_wait_for_trigger": obj.dds_wait_for_trigger,
                        "dds_digital_out": obj.dds_digital_out,
                    }
                if isinstance(obj, np.bool_):
                    return bool(obj)
                return json.JSONEncoder.default(self, obj)

        return json.dumps(compiled, cls=RFBlockEncoder), all_durations
    else:
        return compiled, all_durations


def scale_frequency(seq: List[RFBlock], offs: float, mult: float = 1.) -> List[RFBlock]:
    """
    Adjusts the freuqency of each element of the sequence by multiplying it by mult and adding offs.
    This function replaces the frequencies in-place and does not copy the sequence.

    Args:
        seq (List[RFBlock]): Sequence of Pulses, Timestamps, etc.
        offs (float): Offset frequency in Hz added to the frequency of every sequence element (after multiplying).
        mult (float): Scale factor for each frequency of the sequence. Defaults to 1.0.
    #Returns:
    #    seq (List[RFBlock]): Sequence of Pulses, Timestamps, etc. with adjusted frequencies.
    """
    for el in seq:
        if hasattr(el, 'frequency') and not el.frequency is None:
            el.frequency = mult * el.frequency + offs
    #return seq


@dataclass
class SequencerMapping:
    """
    Stores the channel mapping (target device name and channel name) for sequence signals
    that may be programmed on Sequencer channels.

    Args:
        pd_setpoint (str): Clock PD channel name
        pd_selection (str): Clock PD selection channel name
        clk_shutter (str): Clock shutter control channel name
        clk_aom (str): Clock AOM control channel name
        dds_trigger (str): Trigger channel for FPGA-DDS
        dds_trigger_duration (float): Duration of DDS trigger
        additional_params (dict): Signal name (as used in the sequence; dict key) and target name (dict value) pairs. Defaults to None.
    """
    pd_setpoint: str = "DACE06@E06"
    pd_selection: str = "AOSense Heater Enable@D14"
    clk_shutter: str = "LR AOM Sweep@C02"
    clk_aom: str = "LR/HR [hi/lo]@C04"
    dds_trigger: str = "LR Demod Sweep@C03"
    dds_trigger_duration: float = 1e-3
    additional_params: dict = None


# the following are some helper-functions and objects for construct_sequencer_sequence()
sequence_searchpath = ''
def set_sequence_searchpath(path):
    global sequence_searchpath
    sequence_searchpath = path


class SequenceNotFoundError(Exception):
    """ Unable to find sequence """


def find_sequencer_sequence_path(seq_name, sequence_searchpath):
    for i in range(365):
        day = datetime.date.today() - datetime.timedelta(i)
        seq_path = os.path.join(sequence_searchpath, day.strftime('%Y%m%d'), seq_name)
        if os.path.exists(seq_path):
            return seq_path
    raise SequenceNotFoundError(seq_name)


def read_sequencer_defaults(seq_file: str, timestep_index: int) -> dict:
    """
    Extracts the output values at a given index for each Sequencer output channel.

    Args:
        seq_file (str): Path to Sequencer sequence file
        timestep_index (int): Index for the timestep within the Sequencer sequence file.

    Returns:
        defaults (dict): Default output values ('vf' for analog channels) for each Sequencer channel.
    """
    with open(seq_file) as f:
        seq = json.load(f)

        defaults = {}
        for ch,timesteps in seq.items():
            if 'out' in timesteps[timestep_index].keys():  # digital channel
                defaults[ch] = {'val': timesteps[timestep_index]['out'],  # digital output value
                                'digital': True}
            else:  # analog channel
                defaults[ch] = {'val': timesteps[timestep_index]['vf'],  # output voltage at the end of the timestep
                                'digital': False}
        return defaults


def build_sequencer_timesteps(durations: List[float], values: List, digital: bool):
    if digital:
        return [{'dt': durations[i], 'out': int(values[i])} for i in range(len(durations))]
    else:
        return [{'dt': durations[i],
                 'type': 'lin',
                 'vf': set_float_or_str(values[i])} for i in range(len(durations))]


def remove_channel(sequencer_channels, element_to_remove):
    try:
        sequencer_channels.remove(element_to_remove)
    except ValueError:
        raise ValueError('{} is not a valid Sequencer channel.'.format(element_to_remove))


def construct_sequencer_sequence(compiled_dds_sequence: List[RFBlock],
                                 sequencer_defaults_sequence_file: str,
                                 default_timestep_index: int = -1,
                                 sequence_searchpth: str = None,
                                 sequencer_mapping: SequencerMapping = SequencerMapping()):
    """
    Constructs a Sequencer sequence JSON string based on the provided DDS sequence in
    combination with the SequencerMapping.
    All Sequencer channels which are not used in the DDS sequence are set to the values
    specified in the timestep index default_timestep_index of the
    sequencer_defaults_sequence. These values are kept fixed throughout the entire sequence.

    Args:
        compiled_dds_sequence (List[RFBlock]): DDS sequence (output of compile_sequence()).
        sequencer_defaults_sequence_file (str): File name of a Sequencer reference sequence for unused Sequencer channel values.
        default_timestep_index (int): Time index in the Sequencer defaults sequence from which to extract the reference values. Defaults to -1.
        sequence_searchpth (str): Path to sequence directory in which to search for the default sequence. Defaults to None, which is replaced by the value of the global variable sequence_searchpath (initialized via :func"`set_sequence_searchpath`).
        sequencer_mapping (:class:`SequencerMapping`): Channel mapping for non-DDS signals. Defaults to SequencerMapping() (the default mapping of the required channels).
    Returns:
        seq_str (str): JSON Sequencer string
    """
    compiled_dds_sequence = compiled_dds_sequence[0]  # extract first programmed channel

    if (compiled_dds_sequence[0].additional_params is not None and sequencer_mapping.additional_params is None) or \
       (compiled_dds_sequence[0].additional_params is None and sequencer_mapping.additional_params is not None):
        raise ValueError("additional_params in the DDS sequence and Sequencer mapping are not both None. They must always have the same keys.")
    if compiled_dds_sequence[0].additional_params is not None and \
       (compiled_dds_sequence[0].additional_params.keys() != sequencer_mapping.additional_params.keys()):
        raise KeyError("Keys of additional_params in DDS sequence does not match the keys of SequencerMapping.additional_params; they must always be the same.  sequence.additional_params.keys(): {},  SequencerMapping.additional_params.keys(): {}".format(
            list(compiled_dds_sequence[0].additional_params.keys()),
            list(sequencer_mapping.additional_params.keys())))

    global sequence_searchpath
    if sequence_searchpth is None:
        sequence_searchpth = sequence_searchpath
    default_seq_path = find_sequencer_sequence_path(sequencer_defaults_sequence_file, sequence_searchpth)
    sequencer_defaults = read_sequencer_defaults(default_seq_path, default_timestep_index)

    compiled_dds_sequence = compiled_dds_sequence[:-1]  # remove DDS sequencer terminator

    # build Sequencer sequence
    seq = {}
    sequencer_channels = list(sequencer_defaults.keys())
    durations = [ts.duration for ts in compiled_dds_sequence]  # these are not the durations but timepoints of value cahnges
    durations = np.diff(durations)  # convert timepoints to durations
    #durations = np.insert(durations, 0, sequencer_mapping.dds_trigger_duration)

    # channels relevant for clock pulses (i.e. mapped in DDS sequence)
    trig_vals = np.full(durations.size, 0, dtype=int)
    trig_vals[durations<=sequencer_mapping.dds_trigger_duration] = 1
    seq[sequencer_mapping.dds_trigger] = build_sequencer_timesteps(durations, trig_vals, digital=True)
    remove_channel(sequencer_channels, sequencer_mapping.dds_trigger)
    seq[sequencer_mapping.pd_setpoint] = build_sequencer_timesteps(durations,
                                                                   [ts.pd_setpoint for ts in compiled_dds_sequence],
                                                                   digital=False)
    remove_channel(sequencer_channels, sequencer_mapping.pd_setpoint)
    seq[sequencer_mapping.pd_selection] = build_sequencer_timesteps(durations,
                                                                    [ts.pd_selection for ts in compiled_dds_sequence],
                                                                    digital=True)
    remove_channel(sequencer_channels, sequencer_mapping.pd_selection)
    seq[sequencer_mapping.clk_shutter] = build_sequencer_timesteps(durations,
                                                                   [ts.clk_shutter for ts in compiled_dds_sequence],
                                                                   digital=True)
    remove_channel(sequencer_channels, sequencer_mapping.clk_shutter)
    seq[sequencer_mapping.clk_aom] = build_sequencer_timesteps(durations,
                                                               [ts.clk_aom for ts in compiled_dds_sequence],
                                                               digital=True)
    remove_channel(sequencer_channels, sequencer_mapping.clk_aom)
    if sequencer_mapping.additional_params is not None:
        for signal,ch in sequencer_mapping.additional_params.items():
            seq[ch] = build_sequencer_timesteps(durations,
                                                [ts.additional_params[signal] for ts in compiled_dds_sequence],
                                                digital=sequencer_defaults[ch]['digital'])
            remove_channel(sequencer_channels, ch)

    # set remaining Sequencer channels to the default values
    for ch in sequencer_channels:
        defaults = sequencer_defaults[ch]
        seq[ch] = build_sequencer_timesteps(durations,
                                            [defaults['val']]*len(durations),
                                            digital=defaults['digital'])

    #return json.dumps(seq)
    return seq


def extract_time_traces(seq: List[RFBlock]):
    """
    Generates a dictionary of number arrays corresponding to the timestamps of a sequence.
    
    Args:
      seq ([FTBlock]): Full FPGA DDS sequence (possibly multiple channels)
    
    Returns:
      traces (dictonary of dictionary of numpy arrays): timestamp traces (just numbers) corresponding to the sequence
    """
    compiled, durations = compile_sequence(seq, output_json=False)
    
    traces = {}
    for channel, seq_channel in compiled.items():
        traces[channel] = {}
        
        times = []
        ampls = []
        phases = []
        freqs = []
        digital = [[] for i in range(dds_settings.N_DIGITAL)]
        trig = 0
        
        for block in seq_channel[:-1]:
            if block.wait_for_trigger:
                traces[channel][trig] = {
                    "time": np.array(times, dtype=np.double),
                    "amplitude": np.array(ampls, dtype=np.double),
                    "phase": np.array(phases, dtype=np.double),
                    "frequency": np.array(freqs, dtype=np.double),
                    "digital": np.array(digital, dtype=int),
                }
                times = []
                ampls = []
                phases = []
                freqs = []
                digital = [[] for i in range(dds_settings.N_DIGITAL)]
                trig += 1
            times.append(block.duration)
            ampls.append(block.amplitude)
            phases.append(block.phase)
            freqs.append(block.frequency)
            for j, b in enumerate(block.digital_out):
                digital[j].append(1 if b else 0)
        traces[channel][trig] = {
            "time": np.array(times, dtype=np.double),
            "amplitude": np.array(ampls, dtype=np.double),
            "phase": np.array(phases, dtype=np.double),
            "frequency": np.array(freqs, dtype=np.double),
            "digital": np.array(digital, dtype=int),
        }
    
    return traces


def timetraces2str(time_traces):
    """
    Creates a JSON string from the time traces.
    
    Args:
      time_traces (dictonary of dictionary of numpy arrays): Time traces of a sequence (generated by :func:'extract_time_traces')
    """
    time_traces_json = {}
    for ch, sequence in time_traces.items():
        time_traces_json[ch] = {}
        for segment, traces in sequence.items():
            time_traces_json[ch][segment] = {}
            for trace, vals in traces.items():
                time_traces_json[ch][segment][trace] = vals.tolist()
    return json.dumps(time_traces_json)


def str2timetraces(json_str):
    """
    Creates a time traces dictionary from a JSON string of the sequence (generated by :func:'timetraces2str')
    
    Args:
      json_str (string): JSON string of time traces of a sequence
      
    Returns:
        time_traces (dictonary of dictionary of numpy arrays): Time traces of a sequence (same format as generated by :func:'extract_time_traces')
    """
    time_traces_json = json.loads(json_str)
    
    time_traces = {}
    for ch, sequence in time_traces_json.items():
        time_traces[ch] = {}
        for segment, traces in sequence.items():
            time_traces[ch][segment] = {}
            for trace, vals in traces.items():
                if trace != 'digital':
                    dtype = np.double
                else:
                    dtype = int
                time_traces[ch][segment][trace] = np.array(vals, dtype=dtype)
    return time_traces


def plot_sequence(seq: List[RFBlock]):
    """
    plot_sequence(seq)

    Plots a sequence using Plotly.

    Args:
        seq ([RFBlock]): The sequence to plot
    """
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots

    compiled, durations = compile_sequence(seq, output_json=False)

    fig = make_subplots(
        rows=3 + dds_settings.N_DIGITAL,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.015,
        row_heights=[0.25, 0.25, 0.25] + [0.2 / dds_settings.N_DIGITAL] * dds_settings.N_DIGITAL,
    )

    plot_data = {}
    for channel, seq_channel in compiled.items():
        times = []
        ampls = []
        phases = []
        freqs = []
        digital = [[] for i in range(dds_settings.N_DIGITAL)]
        i = 0
        for block in seq_channel[:-1]:
            if block.wait_for_trigger:
                plot_data[str((channel, i))] = {
                    "time": times,
                    "amplitude": ampls,
                    "phase": phases,
                    "frequency": freqs,
                    "digital": digital,
                }
                times = []
                ampls = []
                phases = []
                freqs = []
                digital = [[] for i in range(dds_settings.N_DIGITAL)]
                i += 1
            times.append(block.duration)
            ampls.append(block.amplitude)
            phases.append(block.phase)
            freqs.append(block.frequency)
            for j, b in enumerate(block.digital_out):
                digital[j].append(1 if b else 0)
        plot_data[str((channel, i))] = {
            "time": times,
            "amplitude": ampls,
            "phase": phases,
            "frequency": freqs,
            "digital": digital,
        }

    color_i = 0
    colors = px.colors.qualitative.Plotly
    for k, pd in plot_data.items():
        fig.add_trace(
            go.Scatter(
                x=pd["time"],
                y=pd["amplitude"],
                line_shape="hv",
                name="{}".format(k),
                fill="tozeroy",
                legendgroup=k,
                line_color=colors[color_i],
                mode="lines",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=pd["time"],
                y=pd["phase"],
                line_shape="hv",
                name="Phase {}".format(k),
                fill="tozeroy",
                legendgroup=k,
                line_color=colors[color_i],
                showlegend=False,
                mode="lines",
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=pd["time"],
                y=pd["frequency"],
                line_shape="hv",
                name="Frequency {}".format(k),
                legendgroup=k,
                line_color=colors[color_i],
                showlegend=False,
                mode="lines",
            ),
            row=3,
            col=1,
        )
        if k[1] == "0":
            for i in range(dds_settings.N_DIGITAL):
                fig.add_trace(
                    go.Scatter(
                        x=pd["time"],
                        y=pd["digital"][i],
                        line_shape="hv",
                        name="D{} {}".format(i, k),
                        fill="tozeroy",
                        legendgroup=k,
                        line_color=colors[color_i],
                        showlegend=False,
                        mode="lines",
                    ),
                    row=4 + i,
                    col=1,
                )
        color_i += 1

    fig.update_xaxes(
        title_text="Time (s)",
        row=3 + dds_settings.N_DIGITAL,
        col=1,
        rangemode="tozero",
        side="bottom",
    )
    fig.update_yaxes(title_text="Frequency (Hz)", row=3, col=1)
    fig.update_yaxes(title_text="Amplitude", row=1, col=1, range=[0, 1])
    fig.update_yaxes(title_text="Phase (rad)", row=2, col=1)
    for i in range(dds_settings.N_DIGITAL):
        fig.update_yaxes(
            title_text="D{}".format(i),
            row=4 + i,
            col=1,
            range=[0, 1],
            showticklabels=False,
        )
    fig.update_layout(legend={"traceorder": "grouped"})

    fig.show()

    return (compiled, durations, fig)


# def send_seq(seq):
#     if isinstance(seq, List):
#         # for s in seq:
#         #     compile_sequence(s)
#         return [jsonpickle.dumps(s, keys=True) for s in seq]
#     else:
#         # compile_sequence(s)
#         return jsonpickle.dumps(seq, keys=True)
