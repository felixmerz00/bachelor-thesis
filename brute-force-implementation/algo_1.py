from math import sqrt
import numpy as np
from paa import paa_double_pyts

# algorithm 1 Alizade Nikoo
def algorithm_1(t_series, n: int, h: int, T: int, k_s: int, k_e: int, k_b: int):
  print('log info: algorithm 1')
  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  # alpha = 1   # only needed when working with data streams
  m = len(t_series)   # number of time series

  # initial windows
  # np.empty((1,500))
  w = [None for _ in range(m)]
  W = [None for _ in range(m)]
  W_s = [None for _ in range(m)]
  W_e = [None for _ in range(m)]

  alpha = 0
  while alpha*h <= (len(t_series[0])-n):  # I assume all time series have the same length

    for p in range(m):
      w[p] = t_series[p][alpha*h:alpha*h+n]   # shift window
      W[p] = (w[p] - np.mean(w[p])) / np.std(w[p])  # normalization, W[p] is a np.ndarray
      W_s, W_e = paa_double_pyts(W[p], k_s, k_e)  # PAA


    alpha += 1
