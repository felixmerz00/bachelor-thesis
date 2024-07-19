import numpy as np
from math import floor, ceil

def floor_epsilon(number, eps):
  """
  Round down to the nearest epsilon.
  """
  return floor(number / eps) * eps

def ceil_epsilon(number, eps):
  """
  Round up to the nearest epsilon.
  """
  return ceil(number / eps) * eps

def bucketing_filter(W_b, k_b: int, eps):
  m = len(W_b)
  C_1 = np.empty((pow(m, 2), 2), dtype=int)
  
  # initialize k_b-dimensional bucketing scheme
  bkt_lwr_bnd = floor_epsilon(np.min(W_b), eps)
  bkt_upr_bnd = ceil_epsilon(np.max(W_b), eps)
  B = (bkt_upr_bnd - bkt_lwr_bnd)/eps  # number of partitions
  BKT_dim = k_b*(int(B),)
  BKT = np.full(BKT_dim, fill_value=None, dtype=object)  # each bucket contains a tuple of time series indices, thus dtype=object

  for p in range(m):
    # Assign time series to bucket
    bkt = ()
    for w in W_b[p]:
      dim_bkt = floor((w-bkt_lwr_bnd)/eps)
      bkt += (dim_bkt,)
    if BKT[bkt] is None:
      BKT[bkt] = (p,)
    else:
      BKT[bkt] += (p,)       
