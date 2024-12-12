# Standard library imports
# Third-party imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Local imports
import util


# Consult src/corr_join/util.py for the structure of the
# logs


def t_runtime_pr(df, ds_name: str, m: int, params):
  """
  Plot a double plot, where both plots use the correlation threshold (T) as
  the variable paramter. T is plotted against the total runtime in plot one and
  against the pruning rate in plot 2.

  Parameters:
  df (pd.DataFrame): Data from the log file
  ds_name: Name of the dataset to plot
  m: Number of time series
  params (tuple): (n, h, _, k_s, k_e, k_b) for which I want to print the data.
  T is usually at the place of _, but not needed in this function.
  """
  n, h, _, k_s, k_e, k_b = params
  # Filter the DataFrame for the desired parameters
  filtered_df = df[(df['dataset'] == ds_name)
    & (df['m'] == m)
    & (df['n'] == n)
    & (df['h'] == h)
    & (df['k_s'] == k_s)
    & (df['k_e'] == k_e)
    & (df['k_b'] == k_b)]
  # Take the latest available performance measurement for the variable.
  result_df = filtered_df.sort_values(['T', 'algorithm']).groupby(
    ['T', 'algorithm']).last().reset_index()

  # Create the figure with two subplots side by side
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

  # Get unique algorithms from the data
  algorithms = result_df['algorithm'].unique()
  # Generate a color map for the algorithms
  color_map = plt.get_cmap('tab10')(np.linspace(0, 1, max(10, len(algorithms))))

  # Plot 1: Runtime vs. correlation threshold
  for i, algo in enumerate(algorithms):
    algo_df = result_df[result_df['algorithm'] == algo]
    ax1.plot(algo_df['T'], algo_df['runtime [s]'], marker='o', label=algo, color=color_map[i])

  ax1.set_xlabel('Correlation threshold (T)')
  ax1.set_ylabel('Runtime (seconds)')
  ax1.set_title('Runtime vs. correlation threshold')
  ax1.grid(True)
  ax1.legend()

  # Plot 2: Pruning rate vs. correlation threshold
  for i, algo in enumerate(algorithms):
    algo_df = result_df[result_df['algorithm'] == algo]
    ax2.plot(algo_df['T'], algo_df['pruning_rate'], marker='o', label=algo, color=color_map[i])

  ax2.set_xlabel('Correlation threshold (T)')
  ax2.set_ylabel('Pruning rate')
  ax2.set_title('Pruning rate vs. correlation threshold')
  ax2.grid(True)
  ax2.legend()

  # Add description of fixed parameters
  # I need double curly braces because otherwise the f-string thinks it's a
  # variable
  fixed_params = (
      f"Fixed parameters\n"
      f"dataset: {ds_name}, "
      f"m: {m}, "
      f"n: {n}, "
      f"h: {h}, "
      f"$k_{{s}}$: {k_s}, "
      f"$k_{{e}}$: {k_e}, "
      f"$k_{{b}}$: {k_b}"
  )
  fig.text(0.5, 0.08, fixed_params, ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, pad=10))

  # Adjust layout and save the figure
  plt.tight_layout()
  plt.subplots_adjust(bottom=0.25)  # Make room for the description
  plt.savefig(f"./src/corr_join/plots/t_runtime_pr_{ds_name}.png")
  plt.close()


def n_runtime_pr(df, ds_name: str, m: int, params):
  """
  Plot a double plot, where both plots use the window size (n) as the variable
  paramter. n is plotted against the total runtime in plot one and against the
  pruning rate in plot 2.

  Parameters:
  df (pd.DataFrame): Data from the log file
  ds_name: Name of the dataset to plot
  m: Number of time series
  params (tuple): (_, h, T, k_s, k_e, k_b) for which I want to plot the data.
  n is usually at the place of _, but not needed in this function.
  """
  _, h, T, k_s, k_e, k_b = params
  # Filter the DataFrame for the desired parameters
  filtered_df = df[(df['dataset'] == ds_name)
    & (df['m'] == m)
    & (df['h'] == h)
    & (df['T'] == T)
    & (df['k_s'] == k_s)
    & (df['k_e'] == k_e)
    & (df['k_b'] == k_b)]
  # Take the latest available performance measurement for the variable.
  result_df = filtered_df.sort_values(['n', 'algorithm']).groupby(['n', 'algorithm']).last().reset_index()

  # Create the figure with two subplots side by side
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

  # Get unique algorithms from the data
  algorithms = result_df['algorithm'].unique()
  # Colors for each algorithm
  color_map = plt.get_cmap('tab10')(np.linspace(0, 1, max(10, len(algorithms))))

  # Plot 1: Runtime vs. window size
  for i, algo in enumerate(algorithms):
    algo_df = result_df[result_df['algorithm'] == algo]
    ax1.plot(algo_df['n'], algo_df['runtime [s]'], marker='o', label=algo, color=color_map[i])

  ax1.set_xlabel('Window size (n)')
  ax1.set_ylabel('Runtime (seconds)')
  ax1.set_title('Runtime vs. window size')
  ax1.grid(True)
  ax1.legend()

  # Plot 2: Pruning rate vs. window size
  for i, algo in enumerate(algorithms):
    algo_df = result_df[result_df['algorithm'] == algo]
    ax2.plot(algo_df['n'], algo_df['pruning_rate'], marker='o', label=algo, color=color_map[i])

  ax2.set_xlabel('Window size (n)')
  ax2.set_ylabel('Pruning rate')
  ax2.set_title('Pruning rate vs. window size')
  ax2.grid(True)
  ax2.legend()

  # Add description of fixed parameters
  # I need double curly braces because otherwise the f-string thinks it's a
  # variable
  fixed_params = (
      f"Fixed parameters\n"
      f"dataset: {ds_name}, "
      f"m: {m}, "
      f"h: {h}, "
      f"T: {T}, "
      f"$k_{{s}}$: {k_s}, "
      f"$k_{{e}}$: {k_e}, "
      f"$k_{{b}}$: {k_b}"
  )
  fig.text(0.5, 0.08, fixed_params, ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, pad=10))

  # Adjust layout and save the figure
  plt.tight_layout()
  plt.subplots_adjust(bottom=0.25)  # Make room for the description
  plt.savefig(f"./src/corr_join/plots/n_runtime_pr_{ds_name}.png")
  plt.close()


def h_runtime(df, ds_name: str, m: int, params):
  """
  Plot with the stride (h) as the variable paramter. h is plotted against the
  total runtime.

  Parameters:
  df (pd.DataFrame): Data from the log file
  ds_name: Name of the dataset to plot
  m: Number of time series
  params (tuple): (n, _, T, k_s, k_e, k_b) for which I want to plot the data.
  h is usually at the place of _, but not needed in this function.
  """
  n, _, T, k_s, k_e, k_b = params
  # Filter the DataFrame for the desired parameters
  filtered_df = df[(df['dataset'] == ds_name)
    & (df['m'] == m)
    & (df['n'] == n)
    & (df['T'] == T)
    & (df['k_s'] == k_s)
    & (df['k_e'] == k_e)
    & (df['k_b'] == k_b)]
  # Take the latest available performance measurement for the variable.
  result_df = filtered_df.sort_values(['h', 'algorithm']).groupby(['h', 'algorithm']).last().reset_index()

  # Create a figure (just a plot does not work with my info box)
  fig, ax = plt.subplots()

  # Get unique algorithms from the data
  algorithms = result_df['algorithm'].unique()
  # Colors for each algorithm
  color_map = plt.get_cmap('tab10')(np.linspace(0, 1, max(10, len(algorithms))))

  # Plot: Runtime vs. variable
  for i, algo in enumerate(algorithms):
    algo_df = result_df[result_df['algorithm'] == algo]
    ax.plot(algo_df['h'], algo_df['runtime [s]'], marker='o', label=algo, color=color_map[i])

  ax.set_xlabel('Stride (h)')
  ax.set_ylabel('Runtime (seconds)')
  ax.set_title('Runtime vs. stride')
  ax.grid(True)
  ax.legend()

  # Add description of fixed parameters
  # I need double curly braces because otherwise the f-string thinks it's a
  # variable
  fixed_params = (
      f"Fixed parameters\n"
      f"dataset: {ds_name}, "
      f"m: {m}, "
      f"n: {n}, "
      f"T: {T}, "
      f"$k_{{s}}$: {k_s}, "
      f"$k_{{e}}$: {k_e}, "
      f"$k_{{b}}$: {k_b}"
  )
  fig.text(0.5, 0.08, fixed_params, ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, pad=10))

  # Adjust layout and save the figure
  plt.tight_layout()
  plt.subplots_adjust(bottom=0.25)  # Make room for the description
  plt.savefig(f"./src/corr_join/plots/h_runtime_{ds_name}.png")
  plt.close()


def m_runtime(df, ds_name: str, params):
  """
  Plot with the number of time series (m) as the variable paramter. m is
  plotted against the total runtime.

  Parameters:
  df (pd.DataFrame): Data from the log file
  ds_name: Name of the dataset to plot
  params (tuple): (n, h, T, k_s, k_e, k_b) for which I want to plot the data.
  h is usually at the place of _, but not needed in this function.
  """
  n, h, T, k_s, k_e, k_b = params
  m = util.get_params("synthetic_var_m_0_test")
  # Filter the DataFrame for the desired parameters
  filtered_df = df[(df['dataset'] == ds_name)
    & (df['n'] == n)
    & (df['h'] == h)
    & (df['T'] == T)
    & (df['k_s'] == k_s)
    & (df['k_e'] == k_e)
    & (df['k_b'] == k_b)]
  # Take the latest available performance measurement for the variable.
  result_df = filtered_df.sort_values(['m', 'algorithm']).groupby(['m', 'algorithm']).last().reset_index()

  # Create a figure (just a plot does not work with my info box)
  fig, ax = plt.subplots()

  # Get unique algorithms from the data
  algorithms = result_df['algorithm'].unique()
  # Colors for each algorithm
  color_map = plt.get_cmap('tab10')(np.linspace(0, 1, max(10, len(algorithms))))

  # Plot: Runtime vs. the variable
  for i, algo in enumerate(algorithms):
    algo_df = result_df[result_df['algorithm'] == algo]
    ax.plot(algo_df['m'], algo_df['runtime [s]'], marker='o', label=algo, color=color_map[i])

  ax.set_xlabel('Number of time series (m)')
  ax.set_ylabel('Runtime (seconds)')
  ax.set_title('Runtime vs. number of time series')
  ax.grid(True)
  ax.legend()

  # Add description of fixed parameters
  # I need double curly braces because otherwise the f-string thinks it's a
  # variable
  fixed_params = (
      f"Fixed parameters\n"
      f"dataset: {ds_name}, "
      f"n: {n}, "
      f"h: {h}, "
      f"T: {T}, "
      f"$k_{{s}}$: {k_s}, "
      f"$k_{{e}}$: {k_e}, "
      f"$k_{{b}}$: {k_b}"
  )
  fig.text(0.5, 0.08, fixed_params, ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, pad=10))

  # Adjust layout and save the figure
  plt.tight_layout()
  plt.subplots_adjust(bottom=0.25)  # Make room for the description
  plt.savefig(f"./src/corr_join/plots/m_runtime_{ds_name}.png")
  plt.close()


def main():
  df = pd.read_csv('./src/corr_join/logs/performance_log.csv')
  t_runtime_pr(df, "chlorine", 50, util.get_params("chlorine_0_plot_0"))
  t_runtime_pr(df, "gas", 50, util.get_params("chlorine_0_plot_0"))
  n_runtime_pr(df, "chlorine", 50, util.get_params("chlorine_1_plot_0"))
  n_runtime_pr(df, "gas", 50, util.get_params("chlorine_1_plot_0"))
  h_runtime(df, "chlorine", 50, util.get_params("chlorine_var_h_plot"))
  m_runtime(df, "synthetic", util.get_params("synthetic_var_m_0"))


if __name__ == '__main__':
  main()
