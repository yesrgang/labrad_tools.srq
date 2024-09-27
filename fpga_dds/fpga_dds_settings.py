# programmable DDS timestamps
N_CHANNELS = 4      # number of analog output channels
N_ADDRESSES = 2**14 # number of programmable timestamps
N_DIGITAL = 7       # number of TTL output channels

# timing
T_BITS = 48
T_MIN = 1/150e6
T_MAX = 2**T_BITS * T_MIN

# frequency
F_BITS = 36
F_MAX = 150e6

# amplitude
A_BITS = 8

# phase
P_BITS = 16

# TTL channels
N_DIGITAL = 7
