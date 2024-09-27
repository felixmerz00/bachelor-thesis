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
      "ron-minis-separated/ron-minis-cut-drums-1128500-30s/drums"]}
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


def custom_financial(_, __):
  print('log info: loading financial data')
  time_series = []

  for ticker in ("AMD", "AVGO", "GE", "INTC", "LLY", "NVDA", "V", "WMT", "XOM"):
    df = pd.read_csv(f"./data/finance/manual/{ticker}.csv")
    close_prices = df["Close"].to_numpy()
    time_series.append(close_prices)

  time_series = trim_length(time_series, round_by=100)
  return time_series


def automated_financial(_, m: int):
  """
  When running CorrJoin with this dataset, paa.py, line 22
  data_reduced_s = paa_s.transform(data_reshaped)
  has issues with NaN values somewhere inside their computation, even though
  my data contains no Nan values, so don't use this dataset.

  Load the financial data I scraped from Yahoo Finance.

  Parameters:
  m (int): Number of desired time series.

  Returns:
  list: A list containing time series for m stocks.
  """
  print('log info: loading financial data')
  raise NotImplementedError
  time_series = []
  scraped_symbols = []

  # List all files in the specified directory
  for filename in os.listdir("data/finance/automated"):
    if filename.endswith('.csv'):
      # Extract the ticker symbol by removing the '.csv' extension
      symbol = filename[:-4]
      scraped_symbols.append(symbol)

  m = len(scraped_symbols) if m == -1 else min(m, len(scraped_symbols))
  i = 0
  while len(time_series) < m and i < len(scraped_symbols):
    filename = f"./data/finance/automated/{scraped_symbols[i]}.csv"
    df = pd.read_csv(filename)
    close_prices = df["Close"].to_numpy()
    if len(close_prices) >= 2510 and not np.isnan(close_prices).any():
      time_series.append(close_prices)
      # print(f"added {scraped_symbols[i]} to the time_series: {len(time_series[-1])}")
    i += 1

  time_series = trim_length(time_series, round_by=100)
  return time_series


def weather():
  raise NotImplementedError
  import xarray as xr
  lon=30
  lat=10

  # open the file, select the location and write to new netcdf
  da=xr.open_dataset('2016_01.nc')
  ts=da.sel(x=lon, y=lat, method="nearest")
  ts.to_netcdf('timeseries.nc')


def gdrive(dataset: str, m: int = -1):
  """
  Load one of the given datasets: chlorine, gas, random, stock, synthetic.

  Parameters:
  dataset: Choose one of the above datasets.
  m: Number of time series to return.
  """
  print(f"log info: loading {dataset} data")
  time_series = []
  # Use raw string to suppress unnecessary warning.
  df = pd.read_csv(f"./data/google-drive/{dataset}.txt", sep=r'\s+', header=None)
  m = df.shape[0] if (m == -1) else min(m, df.shape[0])
  for i in range(m):
    time_series.append(df.loc[i].to_numpy())
  return time_series


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
    "custom_financial": custom_financial,
    "automated_financial": automated_financial,
  }
  return datasets[name](name, m)


# I don't use the following functions in my acutal correlation join algorithm.
# They are used for comparisons and tests.

def load_short_custom_financial_data(length: int):
  print('log info: loading financial data')
  time_series = []

  for ticker in ("AMD", "AVGO", "GE", "INTC", "LLY", "NVDA", "V", "WMT", "XOM"):
    df = pd.read_csv(f"./data/finance/manual/{ticker}.csv")
    close_prices = df["Close"].to_numpy()
    time_series.append(close_prices)

  for m in range(len(time_series)):
    time_series[m] = time_series[m][:length]
  return time_series


if __name__ == '__main__':
  gdrive("chlorine")
  gdrive("chlorine", 10)
