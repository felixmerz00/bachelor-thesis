from load_data import load_audio_data
from time import perf_counter_ns
from math import sqrt
import numpy as np
from inc_p import incp
import logging
from typing import List

# Formatting for loggers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger for reporting correlation
logger = logging.getLogger("main_logger")
logger.setLevel(logging.INFO)
main_handler = logging.FileHandler('code/brute_force_implementation/logs/report-actual-brute-force.log', mode='w', encoding='utf-8')
main_handler.setLevel(logging.INFO)
main_handler.setFormatter(formatter)
logger.addHandler(main_handler)

# Copy from algo_1.py
# I deleted everything related to dimensionality reduction/filtering:
# PAA, SVD, bucketing filter, Eucledian distance filter
def algorithm_1(t_series: List[np.ndarray], n: int, h: int, T: float, k_s: int, k_e: int, k_b: int):
  print('log info: algorithm 1')
  # epsilon_1 = sqrt(2*k_s*(1-T)/n)
  # epsilon_2 = sqrt(2*k_e*(1-T)/n)
  m = len(t_series)   # number of time series
  num_corr_pairs = 0  # Output

  # initial windows
  w = np.empty((m, n))
  W = np.empty((m, n))
  # W_s = np.empty((m, k_s))
  # W_e = np.empty((m, k_e))

  alpha = 0
  while alpha*h <= (len(t_series[0])-n):  # I assume all time series have the same length
    # logger_2.info(f"Window number {alpha}.")

    for p in range(m):
      w[p] = t_series[p][alpha*h:alpha*h+n]   # shift window
      x_bar = np.mean(w[p])
      W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))  # normalization, W[p] is a np.ndarray
      # W_s[p], W_e[p] = paa_double_pyts(W[p], n, k_s, k_e)  # PAA

    # W_b = custom_svd(W_s, k_b)
    # C_1, _ = bucketing_filter(W_b, k_b, epsilon_1, logger_2)
    # C_2 = set()

    # Eucledian distance filter
    # for pair in C_1:
    #   # if incp(W_e[pair[0]], W_e[pair[1]], len(W_e[pair[0]])) <= epsilon_2:
    #   if np.linalg.norm(W_e[pair[0]] - W_e[pair[1]]) <= epsilon_2:
    #     C_2.add(pair)
    # overall_pruning_rate = 1 - len(C_2)/pow(m, 2)
    # logger_2.info(f"The overall pruning rate is {overall_pruning_rate}.")
    # for pair in C_2:
    #   corrcoef = incp(W[pair[0]], W[pair[1]], n)
    #   if abs(corrcoef) >= T:
    #     logger.info(f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {corrcoef}.")
    for i in range(m):
      for j in range(m):
        if i < j:
          # corrcoef = incp(W[i], W[j], n)
          corrcoef = incp(w[i], w[j], n)
          if abs(corrcoef) >= T:
            num_corr_pairs += 1
            logger.info(f"Report ({i}, {j}, {alpha}): Window {alpha} of time series {i} and {i} are correlated with correlation coefficient {corrcoef}.")

    alpha += 1
  logger.info(f"Report: In total the data contains {num_corr_pairs} correlated window pairs.")
  print(f"log info: Report: In total the data contains {num_corr_pairs} correlated window pairs.")

# Copy from main.py
def use_audio_data():
  # convert_audio_data()  # activate this line when you added new mp3 files
  # time_start = perf_counter_ns()
  time_series = load_audio_data()
  # time_elapsed = perf_counter_ns()-time_start
  # print(f"log info: time for loading audio file from converted file: {time_elapsed/1e9} s")

  # parameters
  m = 1   # number of data streams
  n = 500   # window size
  h = 10   # ideally a divisor of n
  T = 0.75
  k_s = 100
  k_e = 250
  k_b = 2

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")

use_audio_data()
