# Standard library imports
import logging
from time import perf_counter_ns
# Third-party imports
# Local imports
from algo_1 import algorithm_1
import load_data as ld
from paa import paa_custom, paa_pyts
import util


def use_audio_data(logger):
  time_series = ld.load_audio_data()
  n, h, T, k_s, k_e, k_b = util.get_params("audio_params_1")

  time_start = perf_counter_ns()
  pruning_rate = algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start

  # Log dataset,m,T,n,h,pruning rate,runtime[s]
  logger.info(
    f"audio,{len(time_series)},{T},{n},{h},{round(pruning_rate, 3)},{round(time_elapsed/1e9, 3)}"
  )


def use_financial_data(logger):
  # time_series = load_automated_financial_data(1000)
  time_series = ld.load_custom_financial_data()
  n, h, T, k_s, k_e, k_b = util.get_params("financial_params_1")

  time_start = perf_counter_ns()
  pruning_rate = algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start

  # Log dataset,m,T,n,h,pruning rate,runtime[s]
  logger.info(
    f"financial_custom,{len(time_series)},{T},{n},{h},{round(pruning_rate, 3)},{round(time_elapsed/1e9, 3)}"
  )


def use_gdrive_data(dataset: str, params: str, logger, m: int = -1):
  """
  Run CorrJoin with a dataset I got from Google Drive.

  Parameters:
  dataset: The name of the dataset to use.
  params: The name of the parameter tuple to use.
  m: The number of time series to include. Defaults to -1, which uses all
  available time series.
  """
  time_series = ld.gdrive(dataset) if (m == -1) else ld.gdrive(dataset, m)
  n, h, T, k_s, k_e, k_b = util.get_params(params)

  time_start = perf_counter_ns()
  pruning_rate = algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start

  # Log dataset,m,T,n,h,pruning rate,runtime[s]
  logger.info(
    f"{dataset},{len(time_series)},{T},{n},{h},{pruning_rate},{round(time_elapsed/1e9, 3)}"
  )


if __name__ == '__main__':
  # Use the same logger for all runs to avoid duplicate entries
  perf_logger = util.create_csv_logger("performance_logger", logging.INFO,
    "performance_log.csv")
  # use_audio_data(perf_logger)
  # use_financial_data(perf_logger)
  use_gdrive_data("chlorine", "chlorine_params_1", perf_logger, 10)
  use_gdrive_data("gas", "chlorine_params_1", perf_logger, 10)
  use_gdrive_data("random", "random_params_1", perf_logger, 50)
  use_gdrive_data("stock", "chlorine_params_1", perf_logger, 10)
  use_gdrive_data("synthetic", "chlorine_params_1", perf_logger, 10)
