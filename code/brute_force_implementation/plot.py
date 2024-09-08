# Standard library imports
# Third-party imports
import matplotlib.pyplot as plt
import pandas as pd
# Local imports
import util


# Consult code/brute_force_implementation/util.py for the structure of the
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
  params (tuple): (n, h, _, k_s, k_e, k_b) I want to print the data for. T is
  usually at the place of _
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
  # Take the latest available performance measurement for each T value.
  result_df = filtered_df.sort_values('T').groupby('T').last().reset_index()

  # Create the figure with two subplots side by side
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

  # Plot 1: Runtime vs. Correlation Threshold
  ax1.plot(result_df['T'], result_df['runtime'], marker='o')
  ax1.set_xlabel('Correlation Threshold (T)')
  ax1.set_ylabel('Runtime (seconds)')
  ax1.set_title('Runtime vs. Correlation Threshold')
  ax1.grid(True)

  # Plot 2: Pruning Rate vs. Correlation Threshold
  ax2.plot(result_df['T'], result_df['pruning_rate'], marker='o', color='green')
  ax2.set_xlabel('Correlation Threshold (T)')
  ax2.set_ylabel('Pruning Rate')
  ax2.set_title('Pruning Rate vs. Correlation Threshold')
  ax2.grid(True)

  # Add description of fixed parameters
  # I need double curly braces because otherwise the f-string things it's a
  # variable
  fixed_params = (
      f"Fixed Parameters\n"
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
  plt.savefig(f"./code/brute_force_implementation/plots/t_runtime_pr_{ds_name}.png")
  plt.close()


def n_runtime_pr(df, ds_name: str, m: int, params):
  """
  Plot a double plot, where both plots use the window size (n) as the variable
  paramter. T is plotted against the total runtime in plot one and against the
  pruning rate in plot 2.

  Parameters:
  df (pd.DataFrame): Data from the log file
  ds_name: Name of the dataset to plot
  m: Number of time series
  params (tuple): (_, h, T, k_s, k_e, k_b) I want to print the data for. n is
  usually at the place of _
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
  # Take the latest available performance measurement for each T value.
  result_df = filtered_df.sort_values('n').groupby('n').last().reset_index()

  # Create the figure with two subplots side by side
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

  # Plot 1: Runtime vs. Correlation Threshold
  ax1.plot(result_df['n'], result_df['runtime'], marker='o')
  ax1.set_xlabel('Window Size (n)')
  ax1.set_ylabel('Runtime (seconds)')
  ax1.set_title('Runtime vs. Window Size')
  ax1.grid(True)

  # Plot 2: Pruning Rate vs. Correlation Threshold
  ax2.plot(result_df['n'], result_df['pruning_rate'], marker='o', color='green')
  ax2.set_xlabel('Window Size (n)')
  ax2.set_ylabel('Pruning Rate')
  ax2.set_title('Pruning Rate vs. Window Size')
  ax2.grid(True)

  # Add description of fixed parameters
  # I need double curly braces because otherwise the f-string things it's a
  # variable
  fixed_params = (
      f"Fixed Parameters\n"
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
  plt.savefig(f"./code/brute_force_implementation/plots/n_runtime_pr_{ds_name}.png")
  plt.close()


def main():
  df = pd.read_csv('./code/brute_force_implementation/logs/performance_log.csv')
  t_runtime_pr(df, "chlorine", 10, util.get_params("chlorine_params_1"))
  t_runtime_pr(df, "gas", 10, util.get_params("chlorine_params_1"))
  n_runtime_pr(df, "chlorine", 10, util.get_params("chlorine_params_1"))
  n_runtime_pr(df, "gas", 10, util.get_params("chlorine_params_1"))


if __name__ == '__main__':
  main()
