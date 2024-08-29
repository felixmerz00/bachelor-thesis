# Standard library imports
from time import perf_counter_ns
# Third-party imports
import librosa
# Local imports
from algo_1 import algorithm_1
import load_data as ld
from paa import paa_custom, paa_pyts
from util import get_financial_params_1


def use_gdrive_data():
  time_series = ld.load_gdrive_chlorine()
  n, h, T, k_s, k_e, k_b = get_financial_params_1()
  algorithm_1(time_series, n, h, T, k_s, k_e, k_b)


if __name__ == '__main__':
  # use_audio_data()
  # use_financial_data()
  use_gdrive_data()
