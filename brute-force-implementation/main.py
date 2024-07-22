import librosa 
from algo_1 import algorithm_1
from paa import paa_custom, paa_pyts
from time import perf_counter_ns

# load the audio files
print('log info: loading audio file')
x_1, sr_1 = librosa.load('./library/ron-minis-cut-1.mp3', sr=None)
# I use this audio file twice, so I will detect a lot of correlation, hopefully.
x_2, sr_2 = librosa.load('./library/ron-minis-cut-1.mp3', sr=None)
x_3, sr_3 = librosa.load('./library/ron-minis-cut-2.mp3', sr=None)
x_4, sr_4 = librosa.load('./library/ron-minis-cut-0107700.mp3', sr=None)
x_5, sr_5 = librosa.load('./library/ron-minis-cut-0143300.mp3', sr=None)
length = min(len(x_1), len(x_2), len(x_3), len(x_4), len(x_5))  # use data of equal length
cut_off = length % 1000  # cut the data to be divisible by 1000
x_1 = x_1[:-cut_off]
x_2 = x_2[:-cut_off]
x_3 = x_3[:-cut_off]
x_4 = x_4[:-cut_off]
x_5 = x_5[:-cut_off]

time_series = [x_1, x_2, x_3, x_4, x_5]

# parameters
m = 1   # number of data streams
n = 500   # window size
h = 10   # ideally a divisor of n
T = 0.75
k_s = 100
k_e = 250
k_b = 2


time_start = perf_counter_ns()
algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
time_elapsed = perf_counter_ns()-time_start
print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")
