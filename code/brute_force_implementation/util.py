# Standard library imports
from typing import List
from math import sqrt
# Third-party imports
import numpy as np
# Local imports

def get_params(params_name: str):
  """
  Provide the requested parameters for running correlation join.

  Parameters:
  params_name : The name of the parameter tuple.

  Returns:
  tuple: Paramters for running correlation join.
    - n (int): Window size
    - h (int): Stride, ideally a divisor of n
    - T (float): Correlation threshold
    - k_s (int): Number of dimensions for SVD
    - k_e (int): Number of dimensions for Euclidea distance filter
    - k_b (int): Number of dimensions for bucketing filter
  """
  parameters = {
    "audio_params_1": (500, 10, 0.75, 100, 250, 2),
    "financial_params_1": (300, 10, 0.85, 15, 30, 3),
    "chlorine_params_1": (512, 64, 0.9, 16, 32, 2),
    "random_params_1": (512, 64, 0.75, 16, 32, 2)
  }
  return parameters[params_name]


# I don't use the following functions in my acutal correlation join algorithm.
# They are used for comparisons and tests.

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


def euc_dist_manual(x: np.ndarray, y: np.ndarray):
  """
  Calculate Euclidean distance manually according to Alizade Nikoo.

  Parameters:
    x, y: Two vectors of same length to compare to each other.

  Returns:
    The euclidean distance between x and y.
  """
  diff = np.subtract(x, y)   # Subtract arguments, element-wise.
  sq = diff ** 2  # Square each element
  s = np.sum(sq)
  return sqrt(s)
