# Standard library imports
from math import sqrt
import logging
from typing import List
# Third-party imports
import numpy as np
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
  bf_logger = util.create_logger("p_corr_brute_force_logger", logging.INFO,
    "report-brute-force-p-corr.log")
  m = len(t_series)   # Number of time series
  num_corr_pairs = 0  # Output
  bf_logger.info(f"Threshold Theta: {T}")

  # initial windows
  w = np.empty((m, n))
  W = np.empty((m, n))

  alpha = 0
  # I assume all time series have the same length
  while alpha*h <= (len(t_series[0])-n):
    for p in range(m):
      w[p] = t_series[p][alpha*h:alpha*h+n]   # Shift window
      x_bar = np.mean(w[p])
      # Normalization, W[p] is a np.ndarray
      W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))
      # PAA would be here and return W_s[p], W_e[p]

    # SVD would be here and return W_b
    # Bucketing filter would be here and return C_1

    # Eucledian distance filter would be here and return C_2
    # Computation of Pearson correlation returns correlated window pairs
    for i in range(m):
      for j in range(m):
        if i < j:
          corrcoef = incp(W[i], W[j], n)
          # corrcoef = corr_euc_d(W[i], W[j])
          if corrcoef >= T:
            num_corr_pairs += 1
            bf_logger.info(
              f"Report ({i}, {j}, {alpha}): Window {alpha} of time series {i} and {j} are correlated with correlation coefficient {corrcoef}."
            )
    alpha += 1

  bf_logger.info(
    f"Report: In total the data contains {num_corr_pairs} correlated window pairs."
  )
  return 0
