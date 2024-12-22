# Standard library imports
# Third-party imports
import numpy as np
from pyts.approximation import PiecewiseAggregateApproximation
# Local imports$


def paa_pyts(time_series, n: int, k: int):
  """
  Perform PAA on a collection of time series using the pyts package.

  Parameters:
  time_series (np.ndarray): A matrix with time series of length n.
  n (int): The length of the time series.
  k (int): The number of dimensions for the reduced representation. Choose k such that k < n and k divides n.

  Returns:
  np.ndarray: A matrix with time series of length k.
  """
  if n%k != 0 or not k < n:
    raise ValueError(f"Choose k such that k < n and k divides n. You chose n = {n} and k = {k}")
  # window_size in this case is what I call segment size, which is different from n
  transformer = PiecewiseAggregateApproximation(window_size=n//k)
  return transformer.transform(time_series)


def paa_pyts_unoptimized(data, n: int, k: int):
  """
  Perform PAA on a time series using the pyts package.

  Parameters:
  time_series (np.ndarray): A matrix with time series of length n.
  n (int): The length of the time series.
  k (int): The number of dimensions for the reduced representation. Choose k such that k < n and k divides n.

  Returns:
  np.ndarray: A matrix with time series of length k.
  """
  data_reshaped = data.reshape(1, -1)   # reshapes to a 2D array with 1 row and as many columns as needed
  if n%k != 0 or not k < n:
    raise ValueError(f"Choose k such that k < n and k divides n. You chose n = {n} and k = {k}")
  # window_size in this case is what I call segment size, which is different from n
  transformer = PiecewiseAggregateApproximation(window_size=n//k)
  data_reduced = transformer.transform(data_reshaped)
  return data_reduced.flatten()   # Reduce convert 2D array back to 1D


# PAA custom
# does paa on a whole audio file with hundreds of windows and segments
def paa_custom(data, n: int, k: int):
  print('log info: paa 1')
  data_reduced = np.arange(len(data)*(k/n))
  i = 0
  for i in range(len(data)//n):  # iterate through windows, i is the i-th window
    start_idx_win_i = i*500
    for j in range(k):  # iterate through k equi-length segments
      seg_len = n//k
      start_idx_seg_k = start_idx_win_i + j * seg_len
      idx_reduced = int(i*k+j)
      data_reduced[idx_reduced] = np.mean(data[start_idx_seg_k:start_idx_seg_k+seg_len]) # calculate mean of segment
  return data_reduced


# Functions for testing and debugging

# PAA with pyts package
# !!! does only the first window !!!
# This function is for trying out the PAA from pyts
def paa_pyts_experiment(data, n: int, k: int):
  print('log info: paa 2')
  # window_size in this case is what I call segment size
  paa = PiecewiseAggregateApproximation(window_size=n//k)
  data_win = data[:500]
  data_win_reshaped = data_win.reshape(1, -1)
  data_win_reduced = paa.transform(data_win_reshaped)
  return data_win_reduced
