from math import sqrt
import numpy as np
from paa import paa_double_pyts
from svd import custom_svd
from bucketing_filter import bucketing_filter
from inc_p import incp
import logging

# Formatting for loggers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create a logger for reporting correlation
logger = logging.getLogger("main_logger")
logger.setLevel(logging.INFO)
main_handler = logging.FileHandler('code/brute_force_implementation/logs/report.log', mode='w', encoding='utf-8')
main_handler.setLevel(logging.INFO)
main_handler.setFormatter(formatter)
logger.addHandler(main_handler)

# Create a second logger for logging the pruning rates
logger_2 = logging.getLogger('logger_2')
logger_2.setLevel(logging.INFO)
handler_2 = logging.FileHandler('code/brute_force_implementation/logs/pruning-rate.log', mode='w', encoding='utf-8')
handler_2.setLevel(logging.INFO)
handler_2.setFormatter(formatter)
logger_2.addHandler(handler_2)


# algorithm 1 Alizade Nikoo
def algorithm_1(t_series, n: int, h: int, T: float, k_s: int, k_e: int, k_b: int):
  """
  Parameters: t_series (pd.DataFrame)
  """
  print('log info: algorithm 1')
  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  m = t_series.shape[0]   # number of time series
  num_corr_pairs = 0

  # initial windows
  w = [None for _ in range(m)]
  W = [None for _ in range(m)]
  W_s = np.empty((m, k_s))
  W_e = np.empty((m, k_e))

  alpha = 0
  while alpha*h <= (t_series.shape[1]-n):  # I assume all time series have the same length
    # logger_2.info(f"Window number {alpha}.")

    for p in range(m):
      print(f"data type: \n{type(t_series[p][alpha*h:alpha*h+n])}")
      print(f"data: \n{t_series[p][alpha*h:alpha*h+n]}")
      # w[p] has type pandas.core.series.Series
      # TODO: currently this takes the first elements of the first h rows.
      # While it should be taking the first h elements of the first row.
      w[p] = t_series[p][alpha*h:alpha*h+n]   # shift window
      return
      x_bar = np.mean(w[p])
      W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))  # normalization, W[p] is a np.ndarray
      W_s[p], W_e[p] = paa_double_pyts(W[p], n, k_s, k_e)  # PAA

    W_b = custom_svd(W_s, k_b)
    C_1, _ = bucketing_filter(W_b, k_b, epsilon_1, logger_2)
    C_2 = set()

    # Eucledian distance filter
    for pair in C_1:
      # if incp(W_e[pair[0]], W_e[pair[1]], len(W_e[pair[0]])) <= epsilon_2:
      if np.linalg.norm(W_e[pair[0]] - W_e[pair[1]]) <= epsilon_2:
        C_2.add(pair)
    overall_pruning_rate = 1 - len(C_2)/pow(m, 2)
    # logger_2.info(f"The overall pruning rate is {overall_pruning_rate}.")
    # Actual Pearson correlation comparison
    for pair in C_2:
      corrcoef = incp(W[pair[0]], W[pair[1]], n)
      if abs(corrcoef) >= T:
        num_corr_pairs += 1
        logger.info(f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {corrcoef}.")

    alpha += 1

  logger.info(f"Report: In total the data contains {num_corr_pairs} correlated window pairs.")
