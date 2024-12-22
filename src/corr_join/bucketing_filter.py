# Standard library imports
from math import floor, ceil
from itertools import product
# Third-party imports
import numpy as np
# Local imports


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
  all_moves = list(product([-1,0,1], repeat=k_b))
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
  C_1 (np.ndarray): Candidate set of indices of likely correlated pairs of windows. 
  Each row contains one candidate pair, i.e. the matrix has two columns.
  join_pruning_rate (float): The pruning rate from the bucketing filter.
  """
  m = len(W_b)
  # Initialize C_1 as an empty array, because otherwise it might never be intialized
  C_1 = []  # Array of ndarrays with shape: (n, 2)

  # Initialize k_b-dimensional bucketing scheme
  bkt_lwr_bnd = floor_epsilon(np.min(W_b), eps)
  bkt_upr_bnd = ceil_epsilon(np.max(W_b), eps)
  B = round((bkt_upr_bnd - bkt_lwr_bnd)/eps)  # number of partitions
  BKT_dim = k_b*(int(B),)
  BKT = np.full(BKT_dim, fill_value=None, dtype=object)  # Each bucket contains a list of time series indices, thus dtype=object

  # Assign time series in W_b to a bucket
  # Compute the bucket indices for all time series
  bkt_indices = np.floor_divide(np.subtract(W_b, bkt_lwr_bnd), eps).astype(int)
  for p, bkt in enumerate(bkt_indices):
    bkt_tuple = tuple(bkt)
    if BKT[bkt_tuple] is None:
      BKT[bkt_tuple] = [p]
    else:
      BKT[bkt_tuple].append(p)

  # Compare time series in buckets
  for index, bkt in np.ndenumerate(BKT):
    if bkt is None:
      continue
    bkt = np.array(bkt)  # Convert to NumPy array for vectorization

    if len(bkt) > 1:
      # Same bucket comparisons
      i, j = np.triu_indices(len(bkt), k=1)   # Get indices for upper triangle of matrix with offset k = 1
      # Store distance for every comparison
      dist_matrix = np.linalg.norm(W_b[bkt[i]] - W_b[bkt[j]], axis=1)
      # If the distance of a pair bkt[i], bkt[j] is <= eps, return bkt[i] in a new array. 
      # Do the same with j.
      # Stacking the arrays on top of each other and taking the transpose puts 
      # each candidate pair into a row.
      C_1.append(np.vstack((bkt[i][dist_matrix <= eps], bkt[j][dist_matrix <= eps])).T)
    
    if len(bkt) > 0:
      # Neighboring bucket comparisons
      neighbors = get_neighbors(np.array(index), k_b, B)
      C_1_neighbors = [[], []]
      for neighbor in neighbors:
        neighbor_bkt = BKT[neighbor]
        if neighbor_bkt is None:
          continue
        neighbor_bkt = np.array(neighbor_bkt)

        # Calculate all pairwise distances between bkt and neighbor_bkt
        distances = np.linalg.norm(W_b[bkt[:, None]] - W_b[neighbor_bkt], axis=2)  # Shape: (len(bkt), len(neighbor_bkt))
        # Create a mask for pairs within the epsilon distance
        mask = distances <= eps  # Shape: (len(bkt), len(neighbor_bkt))
        i_vals, j_vals = np.where(mask)  # Indices where the condition is met
        # Map the indices back to the original values in bkt and neighbor_bkt
        i_vals = bkt[i_vals]
        j_vals = neighbor_bkt[j_vals]
        # Keep only pairs where i < j
        valid_pairs_mask = i_vals < j_vals
        i_vals = i_vals[valid_pairs_mask]
        j_vals = j_vals[valid_pairs_mask]
        # Add the valid pairs as new columns to `C_1`
        C_1.append(np.vstack((i_vals, j_vals)).T)

  join_pruning_rate = 0
  if C_1:
    C_1 = np.vstack(C_1)
    join_pruning_rate = 1 - C_1.shape[0]/((pow(m, 2)-m)/2)
  else:
    C_1 = np.empty((0, 2), dtype=int)
  return C_1, join_pruning_rate


# Bucketing filter true to the pseudo code by Alizade Nikoo et al.
def bucketing_filter_unoptimized(W_b, k_b: int, eps):
  """
  Parameters:
  W_b (numpy.ndarray): Matrix of windows.
  k_b (int): number of dimensions.
  eps (float): distance threshold ε

  Returns:
  C_1 (np.ndarray): Candidate set of indices of likely correlated pairs of windows. 
  Each row contains one candidate pair, i.e. the matrix has two columns.
  join_pruning_rate (float): The pruning rate from the bucketing filter.
  """
  m = len(W_b)
  # Initialize C_1 as an empty array, because otherwise it might never be intialized
  # C_1 = np.empty((0, 2), dtype=int)
  C_1 = []

  # Initialize k_b-dimensional bucketing scheme
  bkt_lwr_bnd = floor_epsilon(np.min(W_b), eps)
  bkt_upr_bnd = ceil_epsilon(np.max(W_b), eps)
  B = round((bkt_upr_bnd - bkt_lwr_bnd)/eps)  # number of partitions
  BKT_dim = k_b*(int(B),)
  BKT = np.full(BKT_dim, fill_value=None, dtype=object)  # Each bucket contains a list of time series indices, thus dtype=object

  # Assign time series in W_b to a bucket
  # Compute the bucket indices for all time series
  bkt_indices = np.floor_divide(np.subtract(W_b, bkt_lwr_bnd), eps).astype(int)
  for p, bkt in enumerate(bkt_indices):
    bkt_tuple = tuple(bkt)
    if BKT[bkt_tuple] is None:
      BKT[bkt_tuple] = [p]
    else:
      BKT[bkt_tuple].append(p)

  # Compare time series in buckets
  for index, bkt in np.ndenumerate(BKT):
    if bkt is None:
      continue
    # Same bucket
    for i in bkt:
      for j in bkt:
        if i < j and np.linalg.norm(W_b[i] - W_b[j]) <= eps:
          C_1.append([i,j])
    # Neighboring buckets
    neighbors_idx_lst = get_neighbors(index, k_b, B)
    for nb_idx in neighbors_idx_lst:
      if BKT[nb_idx] is None:
        continue
      for i in bkt:
        for j in BKT[nb_idx]:
          if i < j and np.linalg.norm(W_b[i] - W_b[j]) <= eps:
            C_1.append([i,j])
  
  join_pruning_rate = 0
  if C_1:
    C_1 = np.array(C_1)
    join_pruning_rate = 1 - C_1.shape[0]/((pow(m, 2)-m)/2)
  else:
    C_1 = np.empty((0, 2), dtype=int)

  return C_1, join_pruning_rate
