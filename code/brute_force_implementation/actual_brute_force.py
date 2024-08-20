# Standard library imports
from time import perf_counter_ns
from math import sqrt
import logging
from typing import List
# Third-party imports
import numpy as np
# Local imports
from load_data import load_audio_data, load_custom_financial_data, load_short_custom_financial_data
from inc_p import incp
from util import get_audio_params_1, get_financial_params_1, corr_euc_d


# Formatting for loggers
formatter = logging.Formatter(
  '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger for reporting correlation
logger = logging.getLogger("main_logger")
logger.setLevel(logging.INFO)
main_handler = logging.FileHandler(
  'code/brute_force_implementation/logs/report-actual-brute-force.log',
  mode='w', encoding='utf-8')
main_handler.setLevel(logging.INFO)
main_handler.setFormatter(formatter)
logger.addHandler(main_handler)

# Copy from algo_1.py
# I deleted everything related to dimensionality reduction/filtering:
# PAA, SVD, bucketing filter, Eucledian distance filter
def algorithm_1(t_series: List[np.ndarray], n: int, h: int, T: float,
  k_s: int, k_e: int, k_b: int):
  print('log info: algorithm 1')
  m = len(t_series)   # Number of time series
  num_corr_pairs = 0  # Output
  logger.info(f"Threshold Theta: {T}")

  # initial windows
  w = np.empty((m, n))
  W = np.empty((m, n))

  alpha = 0
  # I assume all time series have the same length
  while alpha*h <= (len(t_series[0])-n):
    # logger_2.info(f"Window number {alpha}.")

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
          # corrcoef = incp(w[i], w[j], n)
          # corrcoef = corr_euc_d(W[i], W[j])
          if abs(corrcoef) >= T:
            num_corr_pairs += 1
            logger.info(
              f"Report ({i}, {j}, {alpha}): Window {alpha} of time series {i} and {j} are correlated with correlation coefficient {corrcoef}."
            )
    alpha += 1

  logger.info(
    f"Report: In total the data contains {num_corr_pairs} correlated window pairs."
  )
  print(
    f"log info: Report: In total the data contains {num_corr_pairs} correlated window pairs."
  )

# Copy from main.py
def use_audio_data():
  # Convert_audio_data()  # activate this line when you added new mp3 files
  time_series = load_audio_data()
  n, h, T, k_s, k_e, k_b = get_audio_params_1()

  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)

# Copy from main.py (adjusted)
def use_financial_data():
  # time_series = load_automated_financial_data(1000)
  time_series = load_custom_financial_data()
  n, h, T, k_s, k_e, k_b = get_financial_params_1()

  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)

def use_short_financial_data(data_len: int, n: int, h: int, T:float=0.75):
  """
  Parameters:
    data_len: The length of the time series.
    n: The length of a window.
    h: The stride.
    T: The threshold theta for the correlation.
  """
  time_series = load_short_custom_financial_data(data_len)
  algorithm_1(time_series, n, h, T, -1, -1, -1)

# use_audio_data()
# use_financial_data()
# use_short_financial_data(10, 10, 10)  # Params 1
use_short_financial_data(20, 10, 5)  # Params 2
