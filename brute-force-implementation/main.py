import librosa  # librosa is not compatible with numpy 2
from algo_1 import algorithm_1
from paa import paa_custom, paa_pyts

# load the audio files
print('log info: loading audio file')
x_1, sr_1 = librosa.load('./library/ron-minis-cut-1-no-fade.mp3', sr=None)
cut_off = len(x_1) % 1000  # cut the data to be divisible by 1000
x_1 = x_1[:-cut_off]
# I use this audio file twice, so I will detect a lot of correlation, hopefully.
x_2, sr_2 = librosa.load('./library/ron-minis-cut-1-no-fade.mp3', sr=None)
cut_off = len(x_2) % 1000  # cut the data to be divisible by 1000
x_2 = x_2[:-cut_off]
x_3, sr_3 = librosa.load('./library/ron-minis-cut-2-no-fade.mp3', sr=None)
cut_off = len(x_3) % 1000  # cut the data to be divisible by 1000
x_3 = x_3[:-cut_off]

time_series = [x_1, x_2, x_3]

# parameters
m = 1   # number of data streams
n = 500   # window size
h = -1   # ideally a divisor of n
T = -1
k_s = -1
k_e = -1
k_b = -1


algorithm_1(time_series, n, h, T, k_s, k_e, k_b)


# test PAA
# k = 100   # reduced window size
# x_1_reduced = paa_custom(x_1, n, k)
# x_1_win_pyts = paa_pyts(x_1, n, k)

# the first 100 data points in reduced representation (the first 20 elements of reduced x_1) 
# are identical between my custom solution and the PAA from pyts, but the data has a different
# shape
# print("First 100 data points reduced representation:", x_1_reduced[0:20], "\n")
# print("First 500 data points reduced representation with pyts:", x_1_win_pyts, "\n")
