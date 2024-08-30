# Standard library imports
from time import perf_counter_ns
from typing import Callable
# Third-party imports
import librosa
# Local imports
from algo_1 import algorithm_1
import load_data as ld
from paa import paa_custom, paa_pyts
import util


def use_audio_data():
  # convert_audio_data()  # activate this line when you added new mp3 files
  # time_start = perf_counter_ns()
  time_series = ld.load_audio_data()
  # time_elapsed = perf_counter_ns()-time_start
  # print(f"log info: time for loading audio file from converted file: {time_elapsed/1e9} s")

  # parameters
  m = 1   # number of data streams
  n = 500   # window size
  h = 10   # ideally a divisor of n
  T = 0.75
  k_s = 100
  k_e = 250
  k_b = 2

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")


def use_financial_data():
  # time_series = load_automated_financial_data(1000)
  time_series = ld.load_custom_financial_data()
  n, h, T, k_s, k_e, k_b = util.get_financial_params_1()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)


def use_gdrive_data(dataset: str, get_params: Callable, m: int = -1):
  """
  Run CorrJoin with a dataset I got from Google Drive.

  Parameters:
  dataset: The name of the dataset to use.
  get_params: A function that provides the parameters.
  m: The number of time series to include. Defaults to -1, which uses all
  available time series.
  """
  time_series = ld.gdrive(dataset) if (m == -1) else ld.gdrive(dataset, m)
  n, h, T, k_s, k_e, k_b = get_params()

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")


if __name__ == '__main__':
  # use_audio_data()
  # use_financial_data()
  # use_gdrive_data("chlorine", util.get_chlorine_params_1, 10)
  # use_gdrive_data("gas", util.get_chlorine_params_1, 10)
  # use_gdrive_data("random", util.get_random_params_1, 50)
  # use_gdrive_data("stock", util.get_chlorine_params_1, 10)
  use_gdrive_data("synthetic", util.get_chlorine_params_1, 10)
