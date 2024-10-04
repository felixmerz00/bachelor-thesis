# Standard library imports
import logging
from time import perf_counter_ns
# Third-party imports
# Local imports
from brute_force_euc_dist import brute_force_euc_dist
from brute_force_p_corr import brute_force_p_corr
from corr_join import corr_join
import load_data as ld
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


def gen_t_runtime_pr_data(perf_logger):
  """
  Generate performance data for the runtime vs. T and pruning rate vs. T
  plots.
  """
  for i in range(7):
    # Chlorine dataset
    corr_join_wrapper("chlorine", f"chlorine_0_run_{i}", perf_logger, m=50)
    corr_join_wrapper("chlorine", f"chlorine_0_run_{i}", perf_logger, m=50, algorithm_1=brute_force_p_corr)
    corr_join_wrapper("chlorine", f"chlorine_0_run_{i}", perf_logger, m=50, algorithm_1=brute_force_euc_dist)
    # Gas dataset, for which I use the same parameters
    corr_join_wrapper("gas", f"chlorine_0_run_{i}", perf_logger, m=50)
    corr_join_wrapper("gas", f"chlorine_0_run_{i}", perf_logger, m=50, algorithm_1=brute_force_p_corr)
    corr_join_wrapper("gas", f"chlorine_0_run_{i}", perf_logger, m=50, algorithm_1=brute_force_euc_dist)


def gen_n_runtime_pr_data(perf_logger):
  """
  Generate performance data for the runtime vs. n and pruning rate vs. n
  plots.
  """
  for i in range(4):
    # Chlorine dataset
    corr_join_wrapper("chlorine", f"chlorine_1_run_{i}", perf_logger, m=50)
    corr_join_wrapper("chlorine", f"chlorine_1_run_{i}", perf_logger, m=50, algorithm_1=brute_force_p_corr)
    corr_join_wrapper("chlorine", f"chlorine_1_run_{i}", perf_logger, m=50, algorithm_1=brute_force_euc_dist)
    # Gas dataset, for which I use the same parameters
    corr_join_wrapper("gas", f"chlorine_1_run_{i}", perf_logger, m=50)
    corr_join_wrapper("gas", f"chlorine_1_run_{i}", perf_logger, m=50, algorithm_1=brute_force_p_corr)
    corr_join_wrapper("gas", f"chlorine_1_run_{i}", perf_logger, m=50, algorithm_1=brute_force_euc_dist)


def gen_h_runtime(perf_logger):
  """
  Generate performance data for the runtime vs. h plots.
  """
  for i in range(5):
    # Chlorine dataset
    corr_join_wrapper("chlorine", f"chlorine_var_h_run_{i}", perf_logger, m=50)
    corr_join_wrapper("chlorine", f"chlorine_var_h_run_{i}", perf_logger, m=50, algorithm_1=brute_force_p_corr)
    corr_join_wrapper("chlorine", f"chlorine_var_h_run_{i}", perf_logger, m=50, algorithm_1=brute_force_euc_dist)


def gen_n_runtime(perf_logger):
  """
  Generate performance data for the runtime vs. n plots.
  """
  for m in util.get_params("synthetic_var_m_0_test"):
    corr_join_wrapper("synthetic", "synthetic_var_m_0", perf_logger, m=m)
    corr_join_wrapper("synthetic", "synthetic_var_m_0", perf_logger, m=m, algorithm_1=brute_force_p_corr)
    corr_join_wrapper("synthetic", "synthetic_var_m_0", perf_logger, m=m, algorithm_1=brute_force_euc_dist)


if __name__ == '__main__':
  # Use the same logger for all runs to avoid duplicate entries
  perf_logger = util.create_csv_logger("performance_logger", logging.INFO,
    "performance_log.csv")
  # gen_t_runtime_pr_data(perf_logger)
  # gen_n_runtime_pr_data(perf_logger)
  # gen_h_runtime(perf_logger)
  # gen_n_runtime(perf_logger)

  # corr_join_wrapper("audio_drums", "audio_params_1", perf_logger)
  # corr_join_wrapper("audio_drums", "audio_params_2", perf_logger)
  # corr_join_wrapper("audio_drums_8k", "audio_params_2", perf_logger)
  corr_join_wrapper("chlorine", "chlorine_params_1", perf_logger, m = 20)
