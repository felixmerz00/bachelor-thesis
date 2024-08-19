# Standard library imports
# Third-party imports
import numpy as np
# Local imports
from util import euc_dist_manual
from test_setup import get_first_normalized_window_audio_data


def test_computation_euc_d():
  """
  Test if the Euclidean distance computation by numpy.linalg.norm corresponds
  to the manual Euclidean distance computation by Alizade Nikoo.
  """
  W = get_first_normalized_window_audio_data()
  euc_d_np = np.linalg.norm(W[0] - W[1])
  euc_d_man = euc_dist_manual(W[0], W[1])
  # Numpy rounds the result to, i.e., 1.4360323, thus I chose a lower
  # precision as my usual 1e-9
  assert abs(euc_d_np-euc_d_man) < 1e-6
