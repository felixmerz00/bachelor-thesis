# Standard library imports
from time import perf_counter_ns
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


def use_gdrive_chlorine_data():
  time_series = ld.load_gdrive_chlorine(10)
  n, h, T, k_s, k_e, k_b = util.get_chlorine_params_1()

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")


def use_gdrive_gas_data():
  time_series = ld.load_gdrive_gas(10)
  n, h, T, k_s, k_e, k_b = util.get_chlorine_params_1()

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")


def use_gdrive_random_data():
  time_series = ld.load_gdrive_random(50)
  n, h, T, k_s, k_e, k_b = util.get_random_params_1()

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")


def use_gdrive_stock_data():
  time_series = ld.load_gdrive_stock(50)
  n, h, T, k_s, k_e, k_b = util.get_chlorine_params_1()

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")


def use_gdrive_synthetic_data():
  time_series = ld.load_gdrive_synthetic(50)
  n, h, T, k_s, k_e, k_b = util.get_chlorine_params_1()

  time_start = perf_counter_ns()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start
  print(f"log info: time for algorithm 1: {time_elapsed/1e9} s")


if __name__ == '__main__':
  # use_audio_data()
  # use_financial_data()
  # use_gdrive_chlorine_data()
  # use_gdrive_gas_data()
  # use_gdrive_random_data()
  # use_gdrive_stock_data()
  use_gdrive_synthetic_data()
