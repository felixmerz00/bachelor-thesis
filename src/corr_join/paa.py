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
