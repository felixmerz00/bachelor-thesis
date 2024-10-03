# Standard library imports
from math import sqrt
from typing import List
# Third-party imports
import numpy as np
# Local imports
from load_data import load_audio_data


def get_params():
  """
  Returns default values for:
    n - window size,
    h - stride, ideally a divisor of n,
    T - correlation threshold,
    k_s - number for dimensions after SVD,
    k_e - number of dimensions for Euclidean distance filter,
    k_b - number of dimensions for bucketing filter.
  """
  return 500, 10, 0.75, 100, 250, 2

def get_first_normalized_window_audio_data() -> List[np.ndarray]:
  """
  Returns:
    list of np.ndarrays: First normalized window for m data streams of audio
    data.
  """
  # convert_audio_data()  # activate this line when you added new mp3 files
  time_series = load_audio_data()

  # parameters
  m = len(time_series)   # number of time series
  n, h, _, _, _, _ = get_params()

  alpha = 0   # window number

  # initial windows
  w = [np.empty(n) for _ in range(m)]
  W = [np.empty(n) for _ in range(m)]

  for p in range(m):
    w[p] = time_series[p][alpha*h:alpha*h+n]   # shift window
    x_bar = np.mean(w[p])
    W[p] = (w[p] - x_bar) / sqrt(np.sum(pow((w[p]-x_bar), 2)))  # normalization, W[p] is a np.ndarray

  return W

def get_first_window_audio_data():
  """
    Returns:
      list of np.ndarrays: First normalized window for m data streams of audio
      data.
  """
  # convert_audio_data()  # activate this line when you added new mp3 files
  time_series = load_audio_data()

  # parameters
  m = len(time_series)   # number of time series
  n, h, _, _, _, _ = get_params()

  alpha = 0   # window number

  # initial windows
  w = [np.empty(n) for _ in range(m)]

  for p in range(m):
    w[p] = time_series[p][alpha*h:alpha*h+n]   # shift window

  return w
