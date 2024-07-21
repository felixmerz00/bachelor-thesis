import numpy as np
from math import floor, ceil
import itertools

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

def get_neighbors(bkt_cords, k_b: int, B:int):
  """
  Generate the coordinates for each neighbor of bucket of bkt.
  I start from bkt_cords and generating all moves to an adjacent 
  bucket. The result is the list of moves added to the bkt_cords.

  Parameters:
  bkt_cords (tuple): Coordinates of your bucket.
  B (int): The bound of the array (exclusive).

  Returns:
  list of tuples: A list with the coordinates of all neighbors of bkt.
  """
  all_moves = list(itertools.product([-1,0,1], repeat=k_b))
  all_moves.remove(k_b*(0,))
  # Adding the moves to the current position gives all virtual neighbors
  neighbors =  bkt_cords + np.array(all_moves)
  # ... but we must remove the impossible positions
  neighbors = neighbors[((neighbors>=0)&(neighbors<B)).all(axis=1)]
  return [tuple(row) for row in neighbors]

def bucketing_filter(W_b, k_b: int, eps):
  """
  Parameters:
  W_b (numpy.ndarray): Matrix of windows.
  k_b (int): number of dimensions.
  eps (float): distance threshold ε
  
  Returns:
  C_1 (set of tuples): Candidate set of indices of likely correlated pairs of windows.
  """
  m = len(W_b)
  # C_1 = np.empty((pow(m, 2), 2), dtype=int)
  C_1 = set()
  
  # initialize k_b-dimensional bucketing scheme
  bkt_lwr_bnd = floor_epsilon(np.min(W_b), eps)
  bkt_upr_bnd = ceil_epsilon(np.max(W_b), eps)
  B = (bkt_upr_bnd - bkt_lwr_bnd)/eps  # number of partitions
  BKT_dim = k_b*(int(B),)
  BKT = np.full(BKT_dim, fill_value=None, dtype=object)  # each bucket contains a tuple of time series indices, thus dtype=object

  # assign W_b[p] to a bucket
  for p in range(m):
    bkt = ()
    for w in W_b[p]:
      dim_bkt = floor((w-bkt_lwr_bnd)/eps)
      bkt += (dim_bkt,)
    if BKT[bkt] is None:
      BKT[bkt] = (p,)
    else:
      BKT[bkt] += (p,)

  # check Eucledian distance of W_b[p]s in same and neighboring buckets
  for index, bkt in np.ndenumerate(BKT):
    if not bkt is None:
      # same bucket
      for i in bkt:
        for j in bkt:
          if i < j and np.linalg.norm(W_b[i] - W_b[j]) <= eps:
            C_1.add((i,j))
      # neighboring buckets
      neighbors_idx_lst = get_neighbors(index, k_b, B)
      for nb_idx in neighbors_idx_lst:
        if not BKT[nb_idx] is None:
          for i in bkt:
            for j in BKT[nb_idx]:
              if i < j and np.linalg.norm(W_b[i] - W_b[j]) <= eps:
                C_1.add((i,j))
  
  return C_1
