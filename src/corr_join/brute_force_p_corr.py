# Standard library imports
from math import floor, sqrt
import logging
from time import perf_counter_ns
from typing import List
# Third-party imports
import numpy as np
from scipy.stats import pearsonr
# Local imports
from inc_p import incp
import util


def brute_force_p_corr(t_series: List[np.ndarray], n: int, h: int, T: float,
  k_s: int = -1, k_e: int = -1, k_b: int = -1):
  """
  brute_force_p_corr computes the correlated window pairs directly using just
  the Pearson correlation and skips PAA, SVD, the bucketing filter, and the
  Euclidean distance filter.
  """
  print('log info: running brute_force_p_corr')
  logger_1 = util.create_logger("brute_force_p_corr_logger", logging.INFO,
    "report-brute_force_p_corr.log")
  m = t_series.shape[0]   # number of time series
  num_corr_pairs = 0  # Output
  overall_pruning_rate = 0
  logger_1.info(f"Threshold Theta: {T}")
  # Times for profiling, 6 columns/measurements for max_alpha-1 rows/windows
  len_ts = t_series.shape[1]
  max_alpha = floor((len_ts-n)/h)
  p_times = np.empty((max_alpha + 1, 6))

  # initial windows
  w = [None for _ in range(m)]
  W = [None for _ in range(m)]

  alpha = 0
  # I assume all time series have the same length
  while alpha*h <= (len_ts-n):  # I assume all time series have the same length
    # Time before shifting the window (0) for window alpha
    p_times[alpha, 0] = perf_counter_ns()

    # Shift windows
    # WARNING: Contrary to usual python slices, both the start and the stop are included
    w = t_series.loc[:, alpha*h:alpha*h+n-1].to_numpy(dtype='float')
    x_bar = np.mean(w, axis=1)  # np.ndarray of row means, shape (m,)
    # Normalization
    w_centered = w - x_bar[:, np.newaxis]
    denominator = np.sqrt(np.sum(np.power(w_centered, 2), axis=1))  # np.ndarray of shape (m,)
    W = np.divide(w_centered, denominator[:, np.newaxis]) # np.ndarray of shape (m, n)
    # PAA would be here and return W_s, W_e

    # SVD
    p_times[alpha, 1] = perf_counter_ns()   # Time before SVD
    # SVD would be here and return W_b
    
    # Bucketing filter
    p_times[alpha, 2] = p_times[alpha, 1]   # Time before bucketing filter
    # Bucketing filter would be here and return C_1
    
    # Eucledian distance
    p_times[alpha, 3] = p_times[alpha, 1]   # Time before Euclidean distance filter
    # Eucledian distance filter would be here and return C_2
    # Unique pairs of cross product of indices
    C_2 = np.array([(i, j) for i in range(m) for j in range(i + 1, m)])

    # Pearson correlation comparison
    p_times[alpha, 4] = p_times[alpha, 1]   # Time before computing the Pearson correlation
    # Computation of Pearson correlation returns correlated window pairs
    for pair in C_2:
      corrcoef, _ = pearsonr(W[pair[0]], W[pair[1]])
      if corrcoef >= T:
      # if abs(corrcoef) >= T:
        num_corr_pairs += 1
        # logger_1.info(
        #       f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {corrcoef}."
        # )
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

  logger_1.info(
    f"Report: In total the data contains {num_corr_pairs} correlated window pairs."
  )
  return num_corr_pairs, overall_pruning_rate, section_times
