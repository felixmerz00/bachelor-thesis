import numpy as np

def custom_svd(W_s, k_b: int):
  """
  Perform reduced SVD.

  Parameters:
  W_s (array-like): A matrix with m rows.
  k_b: The number of dimensions for the output W_b.

  Returns:
  W_b (ndarray): A matrix consisting of m k_b-dimensional windows.
  """
  try: 
    # u.shape is mxm, s.shape is mx1, v.shape is nxn
    u, s, v = np.linalg.svd(W_s, full_matrices=False)   # specify full_matrices=False to do reduced SVD
  except np.linalg.LinAlgError:
    print("SVD computation does not converge.")
  # from the output of SVD we choose the first kb dimensions for the bucketing, 
  # i.e., reduce the number of columns of U and D to k_b and then compute: U_k*D_k
  u_k = u[:, :k_b]
  d = np.diag(s)
  d_k = d[:k_b, :k_b]
  W_b = np.matmul(u_k, d_k)
  return W_b
