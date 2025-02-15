# Standard library imports
import os
# Third-party imports
import librosa
import numpy as np
import pandas as pd
# Local imports


def trim_length(time_series, round_by: int = 1000):
  min_len = len(time_series[0])
  for ts in time_series:
    l = len(ts)
    if l < min_len:
      min_len = l

  min_len = min_len - (min_len % round_by)  # cut the data to be divisible by 1000 or the value of round_by
  for i in range(len(time_series)):
    time_series[i] = time_series[i][:min_len]

  return time_series


def convert_audio_data(paths):
  """
  Convert audio data from mp3 files to npy files.

  Parameters:
  paths (List): A list of strings with paths to the files that should be
  converted. "./data/audio/"
  """
  print('log info: converting audio data')
  for path in paths:
    np.save(f"./data/audio/{path}", librosa.load(f"./data/audio/{path}.mp3", sr=None)[0])


def audio(dataset: str, _):
  """
  Load the audio data from npy files.
  """
  print('log info: loading audio data')
  # Collection of files for each dataset
  path_lists = {
    "audio_1": ["ron-minis-cut-1", "ron-minis-cut-2", "ron-minis-cut-0107700",
    "ron-minis-cut-0143300"],
    "audio_drums": ["ron-minis-separated/ron-minis-cut-drums-1017000-30s/drums",
      "ron-minis-separated/ron-minis-cut-drums-1128500-30s/drums"],
    "audio_drums_8k": ["ron-minis-separated/ron-minis-cut-drums-1017000-30s/drums-8k",
      "ron-minis-separated/ron-minis-cut-drums-1128500-30s/drums-8k"]}
  # Activate the following line for the first run after you added new mp3
  # files.
  # convert_audio_data(path_lists[dataset])
  time_series = []
  for path in path_lists[dataset]:
    time_series.append(np.load(f"./data/audio/{path}.npy"))

  min_len = len(time_series[0])
  for ts in time_series:
    l = len(ts)
    if l < min_len:
      min_len = l

  # cut the data to be of same length and divisible by 1000
  actual_len = min_len - (min_len % 1000)
  for i in range(len(time_series)):
    time_series[i] = time_series[i][:actual_len]

  return time_series


def gdrive(dataset: str, m: int = -1):
  """
  Load one of the given datasets: chlorine, gas, random, stock, synthetic.

  Parameters:
  dataset: Choose one of the above datasets.
  m: Number of time series to return.
  """
  print(f"log info: loading {dataset} data")
  # Use raw string to suppress unnecessary warning.
  df = pd.read_csv(f"./data/google-drive/{dataset}.txt", sep=r'\s+', header=None)
  df = df.T   # The data is stored in column major
  m = df.shape[0] if (m == -1) else min(m, df.shape[0])
  return df.head(m)


def load_data(name: str, m: int = -1):
  """
  Load one of the given datasets: chlorine, gas, random, stock, synthetic,
  audio, custom_financial, automated_financial.

  Parameters:
  name: Name of a given dataset.
  m: Number of time series to return.
  """
  datasets = {
    "chlorine": gdrive,
    "gas": gdrive,
    "random": gdrive,
    "stock": gdrive,
    "synthetic": gdrive,
    "audio": audio,
    "audio_drums": audio,
    "audio_drums_8k": audio,
  }
  return datasets[name](name, m)


if __name__ == '__main__':
  gdrive("chlorine")
  gdrive("chlorine", 10)
