import numpy as np
import scipy.signal

from math import cos, pi 
from numba import jit

@jit(nopython=True)
def sinwave_gen(frequency, RATE, theta, G):
    gain = 0.5 * 2**15
    om1 = 2.0 * pi * frequency / RATE
    data = int(G * gain * cos(theta))
    theta = theta + om1

    while theta > pi:
        theta = theta - 2.0 * pi
        
    return data, theta


@jit(nopython=True)
def sawtooth_gen(frequency, RATE, prev_data, G):
    gain = 0.5 * 2**15
    slope = 2.0 * frequency / RATE

    sawtooth_data =  prev_data + slope
    data = int(G * gain * sawtooth_data)

    if sawtooth_data > 1:
        sawtooth_data = -1

    return data, sawtooth_data


@jit(nopython=True)
def square_gen(frequency, RATE, prev_idx, positive_side, G):
    gain = 0.5 * 2**15
    N = RATE / frequency    # samples per cycle
    idx = prev_idx + 1

    if positive_side:
        data = int(G * gain * 1)
    else:
        data = int(G * gain * -1)

    if idx >= N:
        idx = 0
        positive_side = False if positive_side else True

    return data, idx, positive_side


@jit(nopython=True)
def triangle_gen(frequency, RATE, prev_data, increase_slope, G):
    gain = 0.5 * 2**15
    slope = 2.0 * 2.0 * frequency / RATE

    if increase_slope:
        triangle_data = prev_data + slope
        if triangle_data >= 1:
            triangle_data = 1
            increase_slope = False
    else:
        triangle_data = prev_data - slope
        if triangle_data <= -1:
            triangle_data = -1
            increase_slope = True

    data = int(G * gain * triangle_data)

    return data, triangle_data, increase_slope
