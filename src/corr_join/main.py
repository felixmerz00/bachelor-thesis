# Standard library imports
import logging
from time import perf_counter_ns
# Third-party imports
# Local imports
from brute_force_euc_dist import brute_force_euc_dist
from brute_force_p_corr import brute_force_p_corr
from corr_join import corr_join, corr_join_unoptimized
from load_data import load_data
import util


def corr_join_wrapper(dataset: str, params: str, logger,
  algorithm_1 = corr_join, m: int = -1):
  """
  Load the specified data and run CorrJoin with the given parameters.

  Parameters:
  dataset: The name of the dataset to use.
  params: The name of the parameter tuple to use.
  logger (Logger): Logger for logging performance metrics of the run.
  algorithm_1: The correlation function to use.
  m: The number of time series to include. Defaults to -1, which uses all
  available time series of the dataset.
  """
  time_series = load_data(dataset, m)
  n, h, T, k_s, k_e, k_b = util.get_params(params)

  time_start = perf_counter_ns()
  num_corr_pairs, pruning_rate, profiling_times = algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start

  logger.info(
    f"{dataset},{len(time_series)},{n},{h},{T},{k_s},{k_e},{k_b},{algorithm_1.__name__},{round(pruning_rate, 3)},{num_corr_pairs},{round(time_elapsed/1e9, 3)}, {profiling_times[0]}, {profiling_times[1]}, {profiling_times[2]}, {profiling_times[3]}, {profiling_times[4]}"
  )


def corr_join_wrapper_loop(time_series, dataset_name: str, params: str, logger,
  algorithm_1 = corr_join):
  """
  Run CorrJoin with the given parameters. 

  Parameters:
  time_series (pandas.DataFrame): The dataset of time series.
  dataset: The name of the dataset to use.
  params: The name of the parameter tuple to use.
  logger (Logger): Logger for logging performance metrics of the run.
  algorithm_1: The correlation function to use.
  """
  n, h, T, k_s, k_e, k_b = util.get_params(params)

  time_start = perf_counter_ns()
  num_corr_pairs, pruning_rate, profiling_times = algorithm_1(time_series, n, h, T, k_s, k_e, k_b)
  time_elapsed = perf_counter_ns()-time_start

  logger.info(
    f"{dataset_name},{time_series.shape[0]},{n},{h},{T},{k_s},{k_e},{k_b},{algorithm_1.__name__},{round(pruning_rate, 3)},{num_corr_pairs},{round(time_elapsed/1e9, 3)}, {profiling_times[0]}, {profiling_times[1]}, {profiling_times[2]}, {profiling_times[3]}, {profiling_times[4]}"
  )


def gen_t_runtime_pr_data(dataset: str, perf_logger):
  """
  Generate performance data for the runtime vs. T and pruning rate vs. T
  plots.
  """
  print(f"log info: dataset: {dataset}")
  df = load_data(dataset, m=50)
  for i in range(7):
    corr_join_wrapper_loop(df, dataset, f"chlorine_0_run_{i}", perf_logger)
    corr_join_wrapper_loop(df, dataset, f"chlorine_0_run_{i}", perf_logger, algorithm_1=brute_force_euc_dist)


def gen_n_runtime_pr_data(dataset: str, perf_logger):
  """
  Generate performance data for the runtime vs. n and pruning rate vs. n
  plots.
  """
  print(f"log info: dataset: {dataset}")
  df = load_data(dataset, m=50)
  for i in range(4):
    corr_join_wrapper_loop(df, dataset, f"chlorine_1_run_{i}", perf_logger)
    corr_join_wrapper_loop(df, dataset, f"chlorine_1_run_{i}", perf_logger, algorithm_1=brute_force_euc_dist)


def gen_h_runtime(dataset: str, perf_logger):
  """
  Generate performance data for the runtime vs. h plots.
  """
  print(f"log info: dataset: {dataset}")
  df = load_data(dataset, m=50)
  for i in range(5):
    corr_join_wrapper_loop(df, dataset, f"chlorine_var_h_run_{i}", perf_logger)
    corr_join_wrapper_loop(df, dataset, f"chlorine_var_h_run_{i}", perf_logger, algorithm_1=brute_force_euc_dist)


def gen_m_runtime(dataset: str, perf_logger):
  """
  Generate performance data for the runtime vs. n plots.
  """
  for m in util.get_params("synthetic_var_m_0_test"):
    print(f"log info: m: {m}")
    df = load_data(dataset, m=m)
    corr_join_wrapper_loop(df, dataset, "synthetic_var_m_0", perf_logger)
    corr_join_wrapper_loop(df, dataset, "synthetic_var_m_0", perf_logger, algorithm_1=brute_force_euc_dist)


def gen_all(perf_logger):
  """
  Generate performance data for all plots.
  """
  print(f"log info: variable: T")
  gen_t_runtime_pr_data("chlorine", perf_logger)
  gen_t_runtime_pr_data("gas", perf_logger)
  gen_t_runtime_pr_data("synthetic", perf_logger)

  print(f"log info: variable: n")
  gen_n_runtime_pr_data("chlorine", perf_logger)
  gen_n_runtime_pr_data("gas", perf_logger)
  gen_n_runtime_pr_data("synthetic", perf_logger)

  print(f"log info: variable: h")
  gen_h_runtime("chlorine", perf_logger)

  print(f"log info: variable: m")
  gen_m_runtime("synthetic", perf_logger)


if __name__ == '__main__':
  # Use the same logger for all runs to avoid duplicate entries
  perf_logger = util.create_csv_logger("performance_logger", logging.INFO,
    "performance_log.csv")
  # corr_join_wrapper("chlorine", "chlorine_params_2", perf_logger, m=10)
  # corr_join_wrapper("chlorine", "chlorine_params_2", perf_logger, m=10, algorithm_1=brute_force_euc_dist)
  # corr_join_wrapper("chlorine", "chlorine_params_2", perf_logger, m=10, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("chlorine", "chlorine_params_2", perf_logger, m=10, algorithm_1=corr_join_unoptimized)

  # corr_join_wrapper("synthetic", "chlorine_0_run_6", perf_logger, m=50)
  # corr_join_wrapper("synthetic", "chlorine_0_run_6", perf_logger, m=50, algorithm_1=brute_force_euc_dist)
  # corr_join_wrapper("synthetic", "chlorine_0_run_6", perf_logger, m=50, algorithm_1=brute_force_p_corr)
  # corr_join_wrapper("synthetic", "chlorine_0_run_6", perf_logger, m=50, algorithm_1=corr_join_unoptimized)

  gen_all(perf_logger)
