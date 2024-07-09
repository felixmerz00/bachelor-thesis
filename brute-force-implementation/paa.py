import numpy as np
# librosa is not compatible with numpy 2
# check if I am using a version of numpy < 2
# print(np.__version__)
from pyts.approximation import PiecewiseAggregateApproximation

# PAA custom
# does paa on a whole audio file with hundreds of windows and segments
def paa_custom(data, n: int, k: int):
  print('log info: paa 1')
  data_reduced = np.arange(len(data)*(k/n))
  i = 0
  for i in range(len(data)//n):  # iterate through windows, i is the i-th window
    start_idx_win_i = i*500
    for j in range(k):  # iterate through k equi-length segments
      seg_len = n//k
      start_idx_seg_k = start_idx_win_i + j * seg_len
      idx_reduced = int(i*k+j)
      data_reduced[idx_reduced] = np.mean(data[start_idx_seg_k:start_idx_seg_k+seg_len]) # calculate mean of segment
  return data_reduced

# PAA with pyts package
# !!! does only the first window !!!
def paa_pyts(data, n: int, k: int):
  print('log info: paa 2')
  # window_size in this case is what I call segment size
  paa = PiecewiseAggregateApproximation(window_size=n//k)
  data_win = data[:500]
  data_win_reshaped = data_win.reshape(1, -1)
  data_win_reduced = paa.transform(data_win_reshaped)
  return data_win_reduced

