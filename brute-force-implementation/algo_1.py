from math import sqrt
import numpy as np

# algorithm 1 Alizade Nikoo
def algorithm_1(t_series, n: int, h: int, T: int, k_s: int, k_e: int, k_b: int):
  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  # alpha = 1   # only needed when working with data streams
  m = len(t_series)   # number of time series

  # initial windows
  # np.empty((1,500))
  w = [None for _ in range(m)]

  alpha = 0
  while alpha*h <= (len(t_series[0])-n):  # I assume all time series have the same length

    for p in range(m):
      w[p] = t_series[p][alpha*h:alpha*h+n]

    alpha += 1
