import librosa  # librosa is not compatible with numpy 2
import numpy as np
# print(np.__version__)   # check if I am using a version of numpy < 2
import logging

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


# PAA custom
print('log info: paa 1')
k = 100   # reduced window size
data_reduced = np.arange(len(data)*(k/n))
i = 0
for i in range(len(data)//n):  # iterate through windows, i is the i-th window
  start_idx_win_i = i*500
  for j in range(k):  # iterate through k equi-length segments
    seg_len = n//k
    start_idx_seg_k = start_idx_win_i + j * seg_len
    idx_reduced = int(i*k+j)
    data_reduced[idx_reduced] = np.mean(data[start_idx_seg_k:start_idx_seg_k+seg_len]) # calculate mean of segment

# PAA with pyts package
print('log info: paa 2')
from pyts.approximation import PiecewiseAggregateApproximation
# window_size in this case is what I call segment size
paa = PiecewiseAggregateApproximation(window_size=n//k)
data_win = data[:500]
data_win_reshaped = data_win.reshape(1, -1)
data_win_reduced = paa.transform(data_win_reshaped)

# the first 100 data points in reduced representation (the first 20 elements of reduced data) 
# are identical between my custom solution and the PAA from pyts, but the data has a different
# shape
print("First 100 data points reduced representation:", data_reduced[0:20], "\n")
print("First 500 data points reduced representation with pyts:", data_win_reduced, "\n")
