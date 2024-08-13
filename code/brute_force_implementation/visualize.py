import matplotlib.pyplot as plt
import librosa.display

def plot_audio(arr, title: str):
  plt.figure().set_figwidth(12)
  plt.title(title)
  librosa.display.waveshow(arr, sr=44100)
  plt.show()

def plot_financial(arr, title: str):
  fig, ax = plt.subplots()             # Create a figure containing a single Axes.
  ax.plot(arr)  # Plot some data on the Axes.
  plt.title(title)
  plt.show()                           # Show the figure.
