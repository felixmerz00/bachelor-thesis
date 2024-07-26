from math import sqrt
import numpy as np
from paa import paa_double_pyts
from svd import custom_svd
from bucketing_filter import bucketing_filter
from inc_p import incp
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='report.log', filemode='w', encoding='utf-8', level=logging.INFO)

# algorithm 1 Alizade Nikoo
def algorithm_1(t_series, n: int, h: int, T: int, k_s: int, k_e: int, k_b: int):
  print('log info: algorithm 1')
  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  m = len(t_series)   # number of time series

  # initial windows
  w = [None for _ in range(m)]
  W = [None for _ in range(m)]
  W_s = np.empty((m, k_s))
  W_e = np.empty((m, k_e))

  alpha = 0
  while alpha*h <= (len(t_series[0])-n):  # I assume all time series have the same length

    for p in range(m):
      w[p] = t_series[p][alpha*h:alpha*h+n]   # shift window
      W[p] = (w[p] - np.mean(w[p])) / np.std(w[p])  # normalization, W[p] is a np.ndarray
      W_s[p], W_e[p] = paa_double_pyts(W[p], n, k_s, k_e)  # PAA

    W_b = custom_svd(W_s, k_b)
    C_1 = bucketing_filter(W_b, k_b, epsilon_1)
    C_2 = set()

    for pair in C_1:
      if np.linalg.norm(W_e[pair[0]] - W_e[pair[1]]) <= epsilon_2:
        C_2.add(pair)
    overall_pruning_rate = 1 - len(C_2)/pow(m, 2)
    # print("Overall pruning rate:", overall_pruning_rate)
    for pair in C_2:
      corrcoef = incp(W[pair[0]], W[pair[1]], n)
      if abs(corrcoef) >= T:
        logger.info(f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {corrcoef}.")

    alpha += 1
