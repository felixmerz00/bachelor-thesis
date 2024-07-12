import numpy as np
from pyts.approximation import PiecewiseAggregateApproximation

# PAA for two numbers of dimensions with pyts package
def paa_double_pyts(data, k_s, k_e):
  data_reshaped = data.reshape(1, -1)   # reshapes to a 2D array with 1 row and as many columns as needed
  # window_size in this case is what I call segment size
  paa_s = PiecewiseAggregateApproximation(window_size=k_s)
  data_reduced_s = paa_s.transform(data_reshaped)
  paa_e = PiecewiseAggregateApproximation(window_size=k_e)
  data_reduced_e = paa_e.transform(data_reshaped)
  return data_reduced_s, data_reduced_e


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

