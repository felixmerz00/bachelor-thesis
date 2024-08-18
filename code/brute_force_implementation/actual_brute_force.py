from load_data import load_audio_data
from time import perf_counter_ns
from math import sqrt
import numpy as np
from inc_p import incp
import logging
from typing import List

# Formatting for loggers
formatter = logging.Formatter(
  '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
          # corrcoef = incp(W[i], W[j], n)
          corrcoef = incp(w[i], w[j], n)
          if abs(corrcoef) >= T:
            num_corr_pairs += 1
            logger.info(
              f"Report ({i}, {j}, {alpha}): Window {alpha} of time series {i} and {i} are correlated with correlation coefficient {corrcoef}."
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

  # Parameters
  m = 1   # Number of data streams
  n = 500   # Window size
  h = 10   # Ideally a divisor of n
  T = 0.75
  k_s = 100
  k_e = 250
  k_b = 2

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")

use_audio_data()
