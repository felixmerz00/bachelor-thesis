# Standard library imports
import logging
from math import sqrt
# Third-party imports
import numpy as np
import pandas as pd
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
  print(f"Information about t_sereis")
  print(f"type(t_series): {type(t_series)}")
  print(f"type(t_series[0]): {type(t_series[0])}")
  print(f"t_series.shape: {t_series.shape}")
  # print(f"t_series.size: {t_series.size}")
  # print(f"t_series.ndim: {t_series.ndim}")
  # print(f"t_series.dtypes: {t_series.dtypes}")
  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  m = t_series.shape[0]   # number of time series
  main_logger.info(f"Threshold Theta: {T}")
  num_corr_pairs = 0
  overall_pruning_rate = -1.0

  # initial windows
  # TODO: Change these declarations to the correct type or to None.
  w = [None for _ in range(m)]  # List of pandas.core.series.Series
  W = [None for _ in range(m)]
  W_s = np.empty((m, k_s))
  W_e = np.empty((m, k_e))

  alpha = 0
  while alpha*h <= (t_series.shape[1]-n):  # I assume all time series have the same length
    # logger_2.info(f"Window number {alpha}.")

    for p in range(m):
      w[p] = t_series.iloc[p, alpha*h:alpha*h+n]   # shift window
      # x_bar = np.mean(w[p])
      x_bar = w[p].mean()
      # W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))  # normalization, W[p] is a np.ndarray
      # TODO: Convert this calculation to work with pandas series
      W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))
      print(type(W[p]))
      # W_s[p], W_e[p] = paa_double_pyts(W[p], n, k_s, k_e)  # PAA

  #   W_b = custom_svd(W_s, k_b)
  #   C_1, _ = bucketing_filter(W_b, k_b, epsilon_1)
  #   C_2 = set()

  #   # Eucledian distance filter
  #   for pair in C_1:
  #     # if incp(W_e[pair[0]], W_e[pair[1]], len(W_e[pair[0]])) <= epsilon_2:
  #     if np.linalg.norm(W_e[pair[0]] - W_e[pair[1]]) <= epsilon_2:
  #       C_2.add(pair)
  #   overall_pruning_rate = 1 - len(C_2)/pow(m, 2)
  #   # logger_2.info(f"The overall pruning rate is {overall_pruning_rate}.")
  #   # Actual Pearson correlation comparison
  #   for pair in C_2:
  #     corrcoef = incp(W[pair[0]], W[pair[1]], n)
  #     if abs(corrcoef) >= T:
  #       num_corr_pairs += 1
  #       main_logger.info(f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {corrcoef}.")

    # if alpha == 1:
    #   break
    # alpha += 1
    break

  # main_logger.info(f"Report: In total the data contains {num_corr_pairs} correlated window pairs.")
  # return num_corr_pairs, overall_pruning_rate
  return -1, -1
