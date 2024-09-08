# Standard library imports
# Third-party imports
import matplotlib.pyplot as plt
import pandas as pd
# Local imports
import util


# Consult code/brute_force_implementation/util.py for the structure of the
# logs


def runtime_t_pr_t(df):
  """
  Plot a double plot, where both plots use the correlation threshold (T) as
  the variable paramter. T is plotted against the total runtime in plot one and
  against the pruning rate in plot 2.

  Parameters: Set the fixed parameters.
  df (pd.DataFrame): Data from the log file
  m: Number of time series
  n: Window size
  h: Stride
  """
  # Filter the DataFrame for the desired parameters
  filtered_df = df[(df['dataset'] == 'chlorine')
    & (df['m'] == 10)
    & (df['n'] == 512)
    & (df['h'] == 64)
    & (df['k_s'] == 16)
    & (df['k_e'] == 32)
    & (df['k_b'] == 2)]

  # Take the latest available performance measurement for each T value.
  result_df = filtered_df.sort_values('T').groupby('T').last().reset_index()

  # Create the plot
  plt.figure(figsize=(10, 6))
  plt.plot(result_df['T'], result_df['runtime'], marker='o')
  plt.xlabel('Correlation Threshold (T)')
  plt.ylabel('Runtime (seconds)')
  plt.title('Runtime vs. Correlation Threshold')
  plt.grid(True)
  plt.show()



def main():
  df = pd.read_csv('./code/brute_force_implementation/logs/performance_log.csv')
  runtime_t_pr_t(df)


if __name__ == '__main__':
  main()
