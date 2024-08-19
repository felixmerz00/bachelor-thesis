import numpy as np


def get_audio_params_1():
  """
  Returns:
    tuple: My default paramters for running correlation join.
    - n (int): Window size
    - h (int): Stride, ideally a divisor of n
    - T (float): Correlation threshold
    - k_s (int): Number of dimensions for SVD
    - k_e (int): Number of dimensions for Euclidea distance filter
    - k_b (int): Number of dimensions for bucketing filter
  """
  return 500, 10, 0.75, 100, 250, 2

def get_financial_params_1():
  """
  Returns:
    tuple: My default paramters for running correlation join.
    - n (int): Window size
    - h (int): Stride, ideally a divisor of n
    - T (float): Correlation threshold
    - k_s (int): Number of dimensions for SVD
    - k_e (int): Number of dimensions for Euclidea distance filter
    - k_b (int): Number of dimensions for bucketing filter
  """
  return 300, 10, 0.85, 15, 30, 3

def corr_euc_d(norm_x, norm_y):
  """
  Calculate the Pearson correlation between x and y based on the Euclidean
  distance between normalized x and normalized y.

  Parameters:
    norm_x, norm_y (array-like): The normalized version of two vectors x and
    y.

  Returns:
    float: The Pearson correlation between x and y.
  """
  return 1-(1/2)*pow(np.linalg.norm(norm_x - norm_y), 2)
