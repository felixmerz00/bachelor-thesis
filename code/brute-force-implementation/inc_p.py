import numpy as np
from math import sqrt

def incp(x, y, n):
  """
  Calculate the Pearson correlation using the incremental Pearson approach from Alizade Nikoo. 
  For my test x and y the computed correlation was identical to numpy.corrcoef(x, y).

  Parameters:
  x (numpy.ndarray): A time series.
  y (numpy.ndarray): A time series.
  n (int): Length of x and y.

  Return:
  The Persion correlation between x and y.
  """
  s_1 = np.sum(x)
  s_2 = np.sum(np.square(x))
  s_3 = np.sum(y)
  s_4 = np.sum(np.square(y))
  s_5 = np.sum(np.multiply(x, y))
  inc_p = (n*s_5 - s_1*s_3) / sqrt((n*s_2-pow(s_1,2)) * (n*s_4-pow(s_3, 2)))
  return inc_p