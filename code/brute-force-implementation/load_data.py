import librosa
import numpy as np
import pandas as pd
import os

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
  


def convert_audio_data():
  # convert the audio data from mp3 files to npy files
  print('log info: converting audio data')
  np.save("./data/audio/ron-minis-cut-1", librosa.load('./data/audio/ron-minis-cut-1.mp3', sr=None)[0])
  np.save("./data/audio/ron-minis-cut-2", librosa.load('./data/audio/ron-minis-cut-2.mp3', sr=None)[0])
  np.save("./data/audio/ron-minis-cut-0107700", librosa.load('./data/audio/ron-minis-cut-0107700.mp3', sr=None)[0])
  np.save("./data/audio/ron-minis-cut-0143300", librosa.load('./data/audio/ron-minis-cut-0143300.mp3', sr=None)[0])


def load_audio_data():
  # load the audio data
  print('log info: loading audio data')
  time_series = []
  time_series.append(np.load("./data/audio/ron-minis-cut-1.npy"))
  time_series.append(np.load("./data/audio/ron-minis-cut-2.npy"))
  time_series.append(np.load("./data/audio/ron-minis-cut-0107700.npy"))
  time_series.append(np.load("./data/audio/ron-minis-cut-0143300.npy"))
  
  min_len = len(time_series[0])
  for ts in time_series:
    l = len(ts)
    if l < min_len:
      min_len = l
  
  cut_off = min_len % 1000  # cut the data to be divisible by 1000
  for i in range(len(time_series)):
    time_series[i] = time_series[i][:-cut_off]

  return time_series

def load_custom_financial_data():
  print('log info: loading financial data')
  time_series = []

  df_amd = pd.read_csv("./data/finance/manual/AMD.csv")
  amd_close_prices = df_amd["Close"].to_numpy()
  time_series.append(amd_close_prices)

  df_avgo = pd.read_csv("./data/finance/manual/AVGO.csv")
  avgo_close_prices = df_avgo["Close"].to_numpy()
  time_series.append(avgo_close_prices)

  df_ge = pd.read_csv("./data/finance/manual/GE.csv")
  ge_close_prices = df_ge["Close"].to_numpy()
  time_series.append(ge_close_prices)

  df_intc = pd.read_csv("./data/finance/manual/INTC.csv")
  intc_close_prices = df_intc["Close"].to_numpy()
  time_series.append(intc_close_prices)

  df_lly = pd.read_csv("./data/finance/manual/LLY.csv")
  lly_close_prices = df_lly["Close"].to_numpy()
  time_series.append(lly_close_prices)

  df_nvda = pd.read_csv("./data/finance/manual/NVDA.csv")
  nvda_close_prices = df_nvda["Close"].to_numpy()
  time_series.append(nvda_close_prices)

  df_v = pd.read_csv("./data/finance/manual/V.csv")
  v_close_prices = df_v["Close"].to_numpy()
  time_series.append(v_close_prices)

  df_wmt = pd.read_csv("./data/finance/manual/WMT.csv")
  wmt_close_prices = df_wmt["Close"].to_numpy()
  time_series.append(wmt_close_prices)

  df_xom = pd.read_csv("./data/finance/manual/XOM.csv")
  xom_close_prices = df_xom["Close"].to_numpy()
  time_series.append(xom_close_prices)
  
  time_series = trim_length(time_series, round_by=100)
  return time_series

def load_automated_financial_data(m: int):
  """
  Load the financial data I scraped from Yahoo Finance.

  Parameters:
  m (int): Number of desired time series.

  Returns:
  list: A list containing time series for m stocks.
  """
  print('log info: loading financial data')
  time_series = []
  scraped_symbols = []

  # List all files in the specified directory
  for filename in os.listdir("data/finance/automated"):
      if filename.endswith('.csv'):
          # Extract the ticker symbol by removing the '.csv' extension
          symbol = filename[:-4]
          scraped_symbols.append(symbol)

  m = min(m, len(scraped_symbols))
  for i in range(m):
    filename = f"./data/finance/automated/{scraped_symbols[i]}.csv"
    df = pd.read_csv(filename)
    close_prices = df["Close"].to_numpy()
    if len(close_prices) >= 2510 and not np.isnan(close_prices).any():
      time_series.append(close_prices)
      # print(f"added {scraped_symbols[i]} to the time_series: {len(time_series[-1])}")
  
  time_series = trim_length(time_series, round_by=100)
  return time_series

def load_weather_data():
  import xarray as xr
  lon=30
  lat=10

  # open the file, select the location and write to new netcdf 
  da=xr.open_dataset('2016_01.nc') 
  ts=da.sel(x=lon, y=lat, method="nearest")
  ts.to_netcdf('timeseries.nc')
