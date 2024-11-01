# Standard library imports
import logging
from math import floor, sqrt
from time import perf_counter_ns
# Third-party imports
import numpy as np
# Local imports
from bucketing_filter import bucketing_filter
from inc_p import incp
from paa import paa_double_pyts
from svd import custom_svd
import util


# CorrJoin according to Alizade Nikoo
def corr_join(t_series, n: int, h: int, T: float, k_s: int, k_e: int, k_b: int):
  print('log info: running CorrJoin')
  main_logger = util.create_logger("main_logger", logging.INFO,
    "report-corr-join.log")

  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  m = len(t_series)   # number of time series

  main_logger.info(f"Threshold Theta: {T}")
  num_corr_pairs = 0
  overall_pruning_rate = -1.0
  len_ts = len(t_series[0])
  max_alpha = floor((len_ts-n)/h)
  # Times for profiling, 6 columns/measurements for max_alpha-1 rows/windows
  p_times = np.empty((max_alpha + 1, 6))

  # initial windows
  w = [None for _ in range(m)]
  W = [None for _ in range(m)]
  W_s = np.empty((m, k_s))
  W_e = np.empty((m, k_e))

  alpha = 0   # Window counter
  while alpha*h <= (len(t_series[0])-n):  # I assume all time series have the same length
    # logger_2.info(f"Window number {alpha}.")

    # Time before shifting the window (0) for window alpha
    p_times[alpha, 0] = perf_counter_ns()
    for p in range(m):
      w[p] = t_series[p][alpha*h:alpha*h+n]   # shift window
      x_bar = np.mean(w[p])
      W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))  # normalization, W[p] is a np.ndarray
      W_s[p], W_e[p] = paa_double_pyts(W[p], n, k_s, k_e)  # PAA
    p_times[alpha, 1] = perf_counter_ns()   # Time before SVD
    W_b = custom_svd(W_s, k_b)
    p_times[alpha, 2] = perf_counter_ns()   # Time before bucketing filter
    C_1, _ = bucketing_filter(W_b, k_b, epsilon_1)
    C_2 = set()

    p_times[alpha, 3] = perf_counter_ns()   # Time before Euclidean distance filter
    # Eucledian distance filter
    for pair in C_1:
      # if incp(W_e[pair[0]], W_e[pair[1]], len(W_e[pair[0]])) <= epsilon_2:
      if np.linalg.norm(W_e[pair[0]] - W_e[pair[1]]) <= epsilon_2:
        C_2.add(pair)
    overall_pruning_rate = 1 - len(C_2)/pow(m, 2)
    # logger_2.info(f"The overall pruning rate is {overall_pruning_rate}.")
    p_times[alpha, 4] = perf_counter_ns()   # Time before computing the Pearson correlation
    # Actual Pearson correlation comparison
    for pair in C_2:
      corrcoef = incp(W[pair[0]], W[pair[1]], n)
      if abs(corrcoef) >= T:
        num_corr_pairs += 1
        main_logger.info(f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {corrcoef}.")
    p_times[alpha, 5] = perf_counter_ns()   # Time after computing the Pearson correlation
    alpha += 1

  p_means = np.mean(p_times, axis=1)  # Calculate across columns
  # Calculate mean differences between consecutive columns
  section_times = np.round([
    np.mean(p_times[:, 1] - p_times[:, 0]),
    np.mean(p_times[:, 2] - p_times[:, 1]),
    np.mean(p_times[:, 3] - p_times[:, 2]),
    np.mean(p_times[:, 4] - p_times[:, 3]),
    np.mean(p_times[:, 5] - p_times[:, 4])
  ]).astype(int)

  main_logger.info(f"Report: In total the data contains {num_corr_pairs} correlated window pairs.")
  return overall_pruning_rate, section_times
