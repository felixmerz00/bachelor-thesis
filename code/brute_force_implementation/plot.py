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

  Parameters:
  df (pd.DataFrame): Data from the log file
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

  # Create the figure with two subplots side by side
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

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

  # Adjust layout and save the figure
  plt.tight_layout()
  plt.savefig('./code/brute_force_implementation/plots/runtime_t_pr_t.png')
  plt.close()


def main():
  df = pd.read_csv('./code/brute_force_implementation/logs/performance_log.csv')
  runtime_t_pr_t(df)


if __name__ == '__main__':
  main()
