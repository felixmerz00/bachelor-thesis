# Standard library imports
import logging
from time import perf_counter_ns
# Third-party imports
# Local imports
from brute_force_euc_dist import brute_force_euc_dist
from brute_force_p_corr import brute_force_p_corr
from corr_join import corr_join
import load_data as ld
from paa import paa_custom, paa_pyts
import util


def corr_join_wrapper(dataset: str, params: str, logger,
  algorithm_1 = corr_join, m: int = -1):
  """
  Run CorrJoin with the given parameters.

  Parameters:
  dataset: The name of the dataset to use.
  params: The name of the parameter tuple to use.
  algorithm_1: The correlation function to use.
  m: The number of time series to include. Defaults to -1, which uses all
  available time series of the dataset.
  """
  time_series = ld.load_data(dataset, m)
  n, h, T, k_s, k_e, k_b = util.get_params(params)

  time_start = perf_counter_ns()
  pruning_rate = algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start

  logger.info(
    f"{dataset},{len(time_series)},{n},{h},{T},{k_s},{k_e},{k_b},{algorithm_1.__name__},{round(pruning_rate, 3)},{round(time_elapsed/1e9, 3)}"
  )


if __name__ == '__main__':
  # Use the same logger for all runs to avoid duplicate entries
  perf_logger = util.create_csv_logger("performance_logger", logging.INFO,
    "performance_log.csv")
  # Run with CorrJoin
  # corr_join_wrapper("audio", "audio_params_1", perf_logger)
  # corr_join_wrapper("custom_financial", "financial_params_1", perf_logger)
  # corr_join_wrapper("chlorine", "chlorine_params_1", perf_logger, m=10)
  # corr_join_wrapper("gas", "chlorine_params_1", perf_logger, m=10)
  # corr_join_wrapper("random", "random_params_1", perf_logger, m=50)
  # corr_join_wrapper("stock", "chlorine_params_1", perf_logger, m=10)
  # corr_join_wrapper("synthetic", "chlorine_params_1", perf_logger, m=10)

  # Run with brute-force algorithm using the Pearson correlation
  # corr_join_wrapper("audio", "audio_params_1", perf_logger, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("custom_financial", "financial_params_1", perf_logger, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("chlorine", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("gas", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("random", "random_params_1", perf_logger, m=50, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("stock", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("synthetic", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_p_corr)

  # Run with brute-force algorithm using the Euclidean distance
  corr_join_wrapper("audio", "audio_params_1", perf_logger, algorithm_1=brute_force_euc_dist)
  corr_join_wrapper("custom_financial", "financial_params_1", perf_logger, algorithm_1=brute_force_euc_dist)
  corr_join_wrapper("chlorine", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_euc_dist)
  corr_join_wrapper("gas", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_euc_dist)
  corr_join_wrapper("random", "random_params_1", perf_logger, m=50, algorithm_1=brute_force_euc_dist)
  corr_join_wrapper("stock", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_euc_dist)
  corr_join_wrapper("synthetic", "chlorine_params_1", perf_logger, m=10, algorithm_1=brute_force_euc_dist)
