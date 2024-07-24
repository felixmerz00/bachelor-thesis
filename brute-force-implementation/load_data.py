import librosa
import numpy as np
import pandas as pd

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
  np.save("./library/ron-minis-cut-1", librosa.load('./library/ron-minis-cut-1.mp3', sr=None)[0])
  np.save("./library/ron-minis-cut-2", librosa.load('./library/ron-minis-cut-2.mp3', sr=None)[0])
  np.save("./library/ron-minis-cut-0107700", librosa.load('./library/ron-minis-cut-0107700.mp3', sr=None)[0])
  np.save("./library/ron-minis-cut-0143300", librosa.load('./library/ron-minis-cut-0143300.mp3', sr=None)[0])


def load_audio_data():
  # load the audio data
  print('log info: loading audio data')
  time_series = []
  time_series.append(np.load("./library/ron-minis-cut-1.npy"))
  # I load this twice to get some correlation
  time_series.append(np.load("./library/ron-minis-cut-1.npy"))
  time_series.append(np.load("./library/ron-minis-cut-2.npy"))
  time_series.append(np.load("./library/ron-minis-cut-0107700.npy"))
  time_series.append(np.load("./library/ron-minis-cut-0143300.npy"))
  
  min_len = len(time_series[0])
  for ts in time_series:
    l = len(ts)
    if l < min_len:
      min_len = l
  
  cut_off = min_len % 1000  # cut the data to be divisible by 1000
  for i in range(len(time_series)):
    time_series[i] = time_series[i][:-cut_off]

  return time_series

def load_financial_data():
  print('log info: loading financial data')
  time_series = []

  df_1 = pd.read_csv("./financial-data/AMD.csv")
  amd_close_prices = df_1["Close"].to_numpy()
  time_series.append(amd_close_prices)
  df_2 = pd.read_csv("./financial-data/INTC.csv")
  intc_close_prices = df_2["Close"].to_numpy()
  time_series.append(intc_close_prices)
  df_3 = pd.read_csv("./financial-data/LLY.csv")
  lly_close_prices = df_3["Close"].to_numpy()
  time_series.append(lly_close_prices)
  time_series.append(lly_close_prices)  # duplicate data to find correlation
  
  time_series = trim_length(time_series, round_by=100)
  return time_series
