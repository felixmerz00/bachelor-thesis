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
  w = [[] for _ in range(m)]
  # w = [None for _ in range(m)]

  alpha = 0
  while alpha*h <= (len(t_series[0])-n):  # I assume all time series have the same length

    for p in range(m):
      # This is how it is in the pseude code. But I don't think I need to store all windwos, 
      # I just need the current window (see next commit).
      # takes 10 ms
      w[p].append(t_series[p][alpha*h:alpha*h+n])

      # takes 8.2775 ms
      # w[p] = t_series[p][alpha*h:alpha*h+n]

    alpha += 1
