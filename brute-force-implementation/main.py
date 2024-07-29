import librosa 
from algo_1 import algorithm_1
from paa import paa_custom, paa_pyts
from time import perf_counter_ns
from load_data import convert_audio_data, load_audio_data, load_automated_financial_data

def use_audio_data():
  # convert_audio_data()  # activate this line when you added new mp3 files
  # time_start = perf_counter_ns()
  time_series = load_audio_data()
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
  time_series = load_automated_financial_data(1000)
  # print(len(time_series), len(time_series[0]))
  # parameters
  n = 300   # window size
  h = 10   # ideally a divisor of n
  T = 0.85
  # TODO: handle if h, k_s, k_e, k_b are not divisors of n
  k_s = 15  # dimensions for svd
  k_e = 30  # dimensions for which I calculate the Eucledian distance
  k_b = 3
  
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)

# use_audio_data()
use_financial_data()