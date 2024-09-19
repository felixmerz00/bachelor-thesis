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
  Note: Alizade Nikoo recommends these parameters: n = 300, h = 10, T = 0.85,
  k_s = 15, k_e = 30, k_b = 3.

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
    "random_params_1": (512, 64, 0.75, 16, 32, 2),
    # Params for runtime vs. T and pruning rate vs. T plots
    "chlorine_0_plot_0": (512, 64, -1, 16, 32, 2),
    "chlorine_0_run_0": (512, 64, 0.84, 16, 32, 2),
    "chlorine_0_run_1": (512, 64, 0.865, 16, 32, 2),
    "chlorine_0_run_2": (512, 64, 0.89, 16, 32, 2),
    "chlorine_0_run_3": (512, 64, 0.915, 16, 32, 2),
    "chlorine_0_run_4": (512, 64, 0.94, 16, 32, 2),
    "chlorine_0_run_5": (512, 64, 0.965, 16, 32, 2),
    "chlorine_0_run_6": (512, 64, 0.99, 16, 32, 2),
    # Params for runtime vs. n and pruning rate vs. n plots
    "chlorine_1_plot_0": (-1, 30, 0.9, 15, 30, 2),
    "chlorine_1_run_0": (30, 30, 0.9, 15, 30, 2),
    "chlorine_1_run_1": (510, 30, 0.9, 15, 30, 2),
    "chlorine_1_run_2": (990, 30, 0.9, 15, 30, 2),
    "chlorine_1_run_3": (1500, 30, 0.9, 15, 30, 2),
    # Params for runtime vs. h plots
    "chlorine_var_h_plot": (300, -1, 0.85, 15, 30, 3),
    "chlorine_var_h_run_0": (300, 100, 0.85, 15, 30, 3),
    "chlorine_var_h_run_1": (300, 200, 0.85, 15, 30, 3),
    "chlorine_var_h_run_2": (300, 300, 0.85, 15, 30, 3),
    "chlorine_var_h_run_3": (300, 400, 0.85, 15, 30, 3),
    "chlorine_var_h_run_4": (300, 500, 0.85, 15, 30, 3)
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
    logger.info(f"dataset,m,n,h,T,k_s,k_e,k_b,algorithm,pruning_rate,runtime")

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
