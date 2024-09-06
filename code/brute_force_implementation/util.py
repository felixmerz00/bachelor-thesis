# Standard library imports
import logging
from math import sqrt
import os
from typing import List
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


def create_logger(logger_name: str, loggerlevel, file_name: str, writing_mode = 'w'):
  """
  Format and create a logger.
  """
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  logger = logging.getLogger(logger_name)
  logger.setLevel(loggerlevel)
  main_handler = logging.FileHandler(f"code/brute_force_implementation/logs/{file_name}", mode=writing_mode, encoding='utf-8')
  main_handler.setLevel(loggerlevel)
  main_handler.setFormatter(formatter)
  logger.addHandler(main_handler)

  return logger


def create_csv_logger(logger_name: str, loggerlevel, file_name: str, writing_mode = 'a'):
  """
  Format and create a logger for performance measurements, whose messages have
  their own format and the default writing mode is set to 'a'.
  """
  log_file_path = f"code/brute_force_implementation/logs/{file_name}"
  formatter = logging.Formatter('%(asctime)s,%(message)s', datefmt='%Y-%m-%d,%H:%M:%S')

  logger = logging.getLogger(logger_name)
  logger.setLevel(loggerlevel)
  main_handler = logging.FileHandler(log_file_path, mode=writing_mode, encoding='utf-8')
  main_handler.setLevel(loggerlevel)
  main_handler.setFormatter(formatter)
  logger.addHandler(main_handler)

  # Write header row if file is empty or doesn't exist
  if not os.path.exists(log_file_path) or os.path.getsize(log_file_path) < 2:
    logger.info(f"dataset,m,n,h,T,k_s,k_e,k_b,pruning rate,runtime[s]")

  return logger


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
