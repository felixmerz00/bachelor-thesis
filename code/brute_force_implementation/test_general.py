# Standard library imports
# Third-party imports
import numpy as np
# Local imports
from util import euc_dist_manual
from test_setup import get_first_normalized_window_audio_data


def test_computation_euc_d_1():
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

def test_computation_euc_d_2():
  """
  Test if the Euclidean distance computation by numpy.linalg.norm corresponds
  to the manual Euclidean distance computation by Alizade Nikoo.
  """
  win_1_ts_4 = np.array([-0.42769122, -0.37802897, -0.35021811, -0.27671819,
    -0.08402848, 0.2914179, 0.26360724, 0.3490263, 0.35101239, 0.26162115])
  win_1_ts_7 = np.array([0.35475717, 0.34063272, 0.18528659, 0.31803901,
    0.2333033, -0.02090214, -0.18189754, -0.28075432, -0.41915516, -0.52930964])
  euc_d_np = np.linalg.norm(win_1_ts_4 - win_1_ts_7)
  euc_d_man = euc_dist_manual(win_1_ts_4, win_1_ts_7)
  # Numpy rounds the result to, i.e., 1.4360323, thus I chose a lower
  # precision as my usual 1e-9
  assert abs(euc_d_np-euc_d_man) < 1e-6

def test_computation_euc_d_3():
  """
  Test if the Euclidean distance computation by numpy.linalg.norm corresponds
  to the manual Euclidean distance computation by Alizade Nikoo.
  """
  win_1_ts_6 = np.array([-0.22992451, -0.27923477, -0.4202123, -0.18314374,
    -0.1129712, -0.23877507, 0.41932649, 0.40352192, 0.47053406, 0.17087914])
  win_1_ts_7 = np.array([0.35475717, 0.34063272, 0.18528659, 0.31803901,
    0.2333033, -0.02090214, -0.18189754, -0.28075432, -0.41915516, -0.52930964])
  euc_d_np = np.linalg.norm(win_1_ts_6 - win_1_ts_7)
  euc_d_man = euc_dist_manual(win_1_ts_6, win_1_ts_7)
  # Numpy rounds the result to, i.e., 1.4360323, thus I chose a lower
  # precision as my usual 1e-9
  assert abs(euc_d_np-euc_d_man) < 1e-6
