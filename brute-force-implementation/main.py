import librosa  # librosa is not compatible with numpy 2
from paa import paa_custom, paa_pyts

# load the audio file (relative path to from where you run main.py)
print('log info: loading audio file')
data, sample_rate = librosa.load('./library/ron-minis-cut-no-fade.mp3', sr=None)
cut_off = len(data) % 1000  # cut the data to be divisible by 1000
data = data[:-cut_off]

# parameters
m = 1   # number of data streams
n = 500   # window size
h = 0   # ideally a divisor of n
T = -1
k_s = -1
k_e = -1
k_b = -1

# algorithm 1 Alizade Nikoo

# PAA
k = 100   # reduced window size
data_reduced = paa_custom(data, n, k)
data_win_reduced = paa_pyts(data, n, k)

# the first 100 data points in reduced representation (the first 20 elements of reduced data) 
# are identical between my custom solution and the PAA from pyts, but the data has a different
# shape
# print("First 100 data points reduced representation:", data_reduced[0:20], "\n")
# print("First 500 data points reduced representation with pyts:", data_win_reduced, "\n")
