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
  k (int): The number of dimensions for the reduced representation.

  Returns:
  np.ndarray: A matrix with time series of length k.
  """
  transformer = PiecewiseAggregateApproximation(window_size=n//k)
  return transformer.transform(time_series)


def paa_double_pyts(data, n: int, k_s: int, k_e: int):
  """
  Perform PAA on a time series using the pyts package for two different dimensions.

  Parameters:
  data (array-like): A time series of length n.
  n (int): The length of the time series.
  k_s (int): The number of dimensions for the first reduced representation.
  k_e (int): The number of dimensions for the second reduced representation.

  Returns:
  tuple: A tuple containing two reduced representations of the data:
      - The first with `k_s` dimensions.
      - The second with `k_e` dimensions.
  """
  data_reshaped = data.reshape(1, -1)   # reshapes to a 2D array with 1 row and as many columns as needed
  # window_size in this case is what I call segment size
  paa_s = PiecewiseAggregateApproximation(window_size=n//k_s)
  data_reduced_s = paa_s.transform(data_reshaped)
  paa_e = PiecewiseAggregateApproximation(window_size=n//k_e)
  data_reduced_e = paa_e.transform(data_reshaped)
  return data_reduced_s.flatten(), data_reduced_e.flatten()   # Reduce convert 2D array back to 1D


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
