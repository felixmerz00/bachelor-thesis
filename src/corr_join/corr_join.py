# Standard library imports
import logging
from math import floor, sqrt
from time import perf_counter_ns
# Third-party imports
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
# Local imports
from bucketing_filter import bucketing_filter, bucketing_filter_unoptimized
from paa import paa_pyts, paa_pyts_unoptimized
from svd import custom_svd
import util


def corr_join(t_series, n: int, h: int, T: float, k_s: int, k_e: int, k_b: int):
  print('log info: running CorrJoin')
  logger_1 = util.create_logger("corr_join_logger", logging.INFO,
    "report-corr_join.log")

  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  m = t_series.shape[0]   # Number of time series

  logger_1.info(f"Threshold Theta: {T}")
  num_corr_pairs = 0
  overall_pr = []   # Store overall pruning rate of each iteration
  len_ts = t_series.shape[1]  # Length of each time series
  max_alpha = floor((len_ts-n)/h)
  # Times for profiling, 6 columns/measurements for max_alpha-1 rows/windows
  p_times = np.empty((max_alpha + 1, 6))

  # Initialize windows
  w = [None for _ in range(m)]
  W = [None for _ in range(m)]
  W_s = np.empty((m, k_s))
  W_e = np.empty((m, k_e))

  alpha = 0   # Window counter
  while alpha*h <= (len_ts-n):  # I assume all time series have the same length
    # logger_2.info(f"Window number {alpha}.")

    # Time before shifting the window (0) for window alpha
    p_times[alpha, 0] = perf_counter_ns()

    # Shift windows
    # WARNING: Contrary to usual python slices, both the start and the stop are included
    w = t_series.loc[:, alpha*h:alpha*h+n-1].to_numpy(dtype='float')
    x_bar = np.mean(w, axis=1)  # np.ndarray of row means, shape (m,)
    # Normalization
    # Subtract x_bar from each row using broadcasting
    w_centered = w - x_bar[:, np.newaxis]
    # Square element-wise, sum each row, compute square root element-wise
    denominator = np.sqrt(np.sum(np.power(w_centered, 2), axis=1))  # np.ndarray of shape (m,)
    W = np.divide(w_centered, denominator[:, np.newaxis]) # np.ndarray of shape (m, n)
    # PAA
    W_s = paa_pyts(W, n, k_s)   # np.ndarray of shape (m, k_s)
    W_e = paa_pyts(W, n, k_e)   # np.ndarray of shape (m, k_e)
    
    # SVD
    p_times[alpha, 1] = perf_counter_ns()   # Time before SVD
    W_b = custom_svd(W_s, k_b)  # np.ndarray of shape (m, k_b)

    # Bucketing filter
    p_times[alpha, 2] = perf_counter_ns()   # Time before bucketing filter
    C_1, _ = bucketing_filter(W_b, k_b, epsilon_1)

    # Eucledian distance filter
    p_times[alpha, 3] = perf_counter_ns()   # Time before Euclidean distance filter
    # Compute the norms for all pairs
    distances = np.linalg.norm(W_e[C_1[:, 0]] - W_e[C_1[:, 1]], axis=1)
    # Create a mask for pairs satisfying the condition
    correlated_pairs_mask = distances <= epsilon_2
    # Filter C_1 based on the mask to create C_2
    C_2 = C_1[correlated_pairs_mask]
    overall_pr.append(1 - C_2.shape[0]/pow(m, 2))
    # logger_2.info(f"The overall pruning rate is {overall_pruning_rate}.")
    
    # Pearson correlation comparison
    p_times[alpha, 4] = perf_counter_ns()   # Time before computing the Pearson correlation
    epsilon = sqrt(2*(1-T))
    distances = np.linalg.norm(W[C_2[:, 0]] - W[C_2[:, 1]], axis=1)
    # Check if each distance satisfies the condition
    correlated_pairs_mask = distances <= epsilon
    correlated_pairs = C_2[correlated_pairs_mask]  # Filter C_2
    num_corr_pairs += correlated_pairs.shape[0]
    # logger_1.info(f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {corrcoef}.")
    p_times[alpha, 5] = perf_counter_ns()   # Time after computing the Pearson correlation
    
    alpha += 1

  # Calculate mean differences between consecutive columns
  section_times = np.round([
    np.mean(p_times[:, 1] - p_times[:, 0]),
    np.mean(p_times[:, 2] - p_times[:, 1]),
    np.mean(p_times[:, 3] - p_times[:, 2]),
    np.mean(p_times[:, 4] - p_times[:, 3]),
    np.mean(p_times[:, 5] - p_times[:, 4])
  ]).astype(int)

  logger_1.info(f"Report: In total the data contains {num_corr_pairs} correlated window pairs.")
  return num_corr_pairs, np.mean(overall_pr), section_times


# CorrJoin true to the pseudo code by Alizade Nikoo et al.
def corr_join_unoptimized(t_series, n: int, h: int, T: float, k_s: int, k_e: int, k_b: int):
  print('log info: running CorrJoin unoptimized')
  logger_1 = util.create_logger("corr_join_unoptimized_logger", logging.INFO,
    "report-corr_join_unoptimized.log")

  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  m = t_series.shape[0]   # Number of time series

  logger_1.info(f"Threshold Theta: {T}")
  num_corr_pairs = 0
  overall_pr = []   # Store overall pruning rate of each iteration
  join_pr = []  # Store join pruning rate of each iteration
  len_ts = t_series.shape[1]  # Length of each time series
  max_alpha = floor((len_ts-n)/h)
  # Times for profiling, 6 columns/measurements for max_alpha-1 rows/windows
  p_times = np.empty((max_alpha + 1, 6))

  # Initialize windows
  w = [None for _ in range(m)]
  W = [None for _ in range(m)]
  W_s = np.empty((m, k_s))
  W_e = np.empty((m, k_e))

  alpha = 0   # Window counter
  while alpha*h <= (len_ts-n):  # I assume all time series have the same length
    # Time before shifting the window (0) for window alpha
    p_times[alpha, 0] = perf_counter_ns()
    for p in range(m):
      # WARNING: Contrary to usual python slices, both the start and the stop are included
      w[p] = t_series.loc[p, alpha*h:alpha*h+n-1].to_numpy(dtype='float')
      x_bar = np.mean(w[p])
      W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))  # normalization, W[p] is a np.ndarray
      W_s[p] = paa_pyts_unoptimized(W[p], n, k_s)  # PAA
      W_e[p] = paa_pyts_unoptimized(W[p], n, k_e)  # PAA

    # SVD
    p_times[alpha, 1] = perf_counter_ns()   # Time before SVD
    W_b = custom_svd(W_s, k_b)  # np.ndarray of shape (m, k_b)

    # Bucketing filter
    p_times[alpha, 2] = perf_counter_ns()   # Time before bucketing filter
    C_1, pr_1 = bucketing_filter_unoptimized(W_b, k_b, epsilon_1)
    join_pr.append(pr_1)
    C_2 = []

    # Eucledian distance filter
    p_times[alpha, 3] = perf_counter_ns()   # Time before Euclidean distance filter
    for pair in C_1:
      if np.linalg.norm(W_e[pair[0]] - W_e[pair[1]]) <= epsilon_2:
        C_2.append(pair)
    overall_pr.append(1 - len(C_2)/pow(m, 2))
    
    # Pearson correlation comparison
    p_times[alpha, 4] = perf_counter_ns()   # Time before computing the Pearson correlation
    epsilon = sqrt(2*(1-T))
    for pair in C_2:
      if np.linalg.norm(W[pair[0]] - W[pair[1]]) <= epsilon:
        num_corr_pairs += 1
        # logger_1.info(f"Report ({pair[0]}, {pair[1]}, {alpha}): Window {alpha} of time series {pair[0]} and {pair[1]} are correlated with correlation coefficient {np.linalg.norm(W[pair[0]] - W[pair[1]])}.")
    p_times[alpha, 5] = perf_counter_ns()   # Time after computing the Pearson correlation
    
    alpha += 1

  # Calculate mean differences between consecutive columns
  section_times = np.round([
    np.mean(p_times[:, 1] - p_times[:, 0]),
    np.mean(p_times[:, 2] - p_times[:, 1]),
    np.mean(p_times[:, 3] - p_times[:, 2]),
    np.mean(p_times[:, 4] - p_times[:, 3]),
    np.mean(p_times[:, 5] - p_times[:, 4])
  ]).astype(int)

  logger_1.info(f"Report: In total the data contains {num_corr_pairs} correlated window pairs.")
  return num_corr_pairs, np.mean(overall_pr), section_times

