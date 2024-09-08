# Standard library imports
# Third-party imports
import matplotlib.pyplot as plt
import pandas as pd
# Local imports
import util


# Consult code/brute_force_implementation/util.py for the structure of the
# logs


def runtime_t_pr_t(df, ds_name: str):
  """
  Plot a double plot, where both plots use the correlation threshold (T) as
  the variable paramter. T is plotted against the total runtime in plot one and
  against the pruning rate in plot 2.

  Parameters:
  df (pd.DataFrame): Data from the log file
  ds_name: Name of the dataset to plot
  """
  # Filter the DataFrame for the desired parameters
  filtered_df = df[(df['dataset'] == ds_name)
    & (df['m'] == 10)
    & (df['n'] == 512)
    & (df['h'] == 64)
    & (df['k_s'] == 16)
    & (df['k_e'] == 32)
    & (df['k_b'] == 2)]

  # Take the latest available performance measurement for each T value.
  result_df = filtered_df.sort_values('T').groupby('T').last().reset_index()

  # Create the figure with two subplots side by side
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
  # fig, (ax1, ax2) = plt.subplots(1, 2)

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
      f"m: 10, "
      f"n: 512, "
      f"h: 64, "
      f"$k_{{s}}$: 16, "
      f"$k_{{e}}$: 32, "
      f"$k_{{b}}$: 2"
  )
  fig.text(0.5, 0.08, fixed_params, ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.5, pad=10))

  # Adjust layout and save the figure
  plt.tight_layout()
  plt.subplots_adjust(bottom=0.25)  # Make room for the description
  plt.savefig(f"./code/brute_force_implementation/plots/runtime_t_pr_t_{ds_name}.png")
  plt.close()


def main():
  df = pd.read_csv('./code/brute_force_implementation/logs/performance_log.csv')
  runtime_t_pr_t(df, "chlorine")
  runtime_t_pr_t(df, "gas")


if __name__ == '__main__':
  main()
