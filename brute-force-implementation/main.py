import librosa  # librosa is not compatible with numpy 2
from algo_1 import algorithm_1
from paa import paa_custom, paa_pyts
from time import perf_counter_ns

# load the audio files
print('log info: loading audio file')
x_1, sr_1 = librosa.load('./library/ron-minis-cut-1-no-fade.mp3', sr=None)
# I use this audio file twice, so I will detect a lot of correlation, hopefully.
x_2, sr_2 = librosa.load('./library/ron-minis-cut-1-no-fade.mp3', sr=None)
x_3, sr_3 = librosa.load('./library/ron-minis-cut-2-no-fade.mp3', sr=None)
length = min(len(x_1), len(x_2), len(x_3))  # use data of equal length
cut_off = length % 1000  # cut the data to be divisible by 1000
x_1 = x_1[:-cut_off]
x_2 = x_2[:-cut_off]
x_3 = x_3[:-cut_off]

time_series = [x_1, x_2, x_3]

# parameters
m = 1   # number of data streams
n = 500   # window size
h = 10   # ideally a divisor of n
T = 0.75
k_s = 100
k_e = 250
k_b = 50


print('log info: start algorithm 1')
# time_start = perf_counter_ns()
algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
# time_elapsed = perf_counter_ns()-time_start
# print(f"log info: time for algorithm 1: {time_elapsed/1e6} ms")


# test PAA
# k = 100   # reduced window size
# x_1_reduced = paa_custom(x_1, n, k)
# x_1_win_pyts = paa_pyts(x_1, n, k)

# the first 100 data points in reduced representation (the first 20 elements of reduced x_1) 
# are identical between my custom solution and the PAA from pyts, but the data has a different
# shape
# print("First 100 data points reduced representation:", x_1_reduced[0:20], "\n")
# print("First 500 data points reduced representation with pyts:", x_1_win_pyts, "\n")
