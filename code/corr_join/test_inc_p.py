# Standard library imports
import numpy as np
# Third-party imports
# Local imports
from test_setup import get_first_normalized_window_audio_data, get_first_window_audio_data
from inc_p import incp
from util import corr_euc_d


def test_compare_inc_p_euc_d_1():
  """
  Check equation 4 from Alizade Nikoo
  """
  w = get_first_window_audio_data()
  W = get_first_normalized_window_audio_data()
  corr_incp = incp(w[0], w[1], len(w[0]))
  c_euc_d = corr_euc_d(W[0], W[1])
  assert corr_incp - c_euc_d < 1e-6

def test_compare_inc_p_euc_d_2():
  """
  Check equation 4 from Alizade Nikoo but with all normalized data.
  """
  w = get_first_window_audio_data()
  W = get_first_normalized_window_audio_data()
  # Usually, this is not normalized.
  corr_incp = incp(W[0], W[1], len(W[0]))
  c_euc_d = corr_euc_d(W[0], W[1])
  assert corr_incp - c_euc_d < 1e-6

def test_compare_inc_p_euc_d_3():
  """
  Check equation 4 from Alizade Nikoo with data from my overfiltering example
  1.
  """
  win_1_ts_4 = np.array([-0.42769122, -0.37802897, -0.35021811, -0.27671819,
    -0.08402848, 0.2914179, 0.26360724, 0.3490263, 0.35101239, 0.26162115])
  win_1_ts_7 = np.array([0.35475717, 0.34063272, 0.18528659, 0.31803901,
    0.2333033, -0.02090214, -0.18189754, -0.28075432, -0.41915516, -0.52930964
  ])
  # Usually, this is not normalized.
  corr_incp = incp(win_1_ts_4, win_1_ts_7, len(win_1_ts_4))
  c_euc_d = corr_euc_d(win_1_ts_4, win_1_ts_7)
  assert corr_incp - c_euc_d < 1e-6

def test_compare_inc_p_euc_d_4():
  """
  Check equation 4 from Alizade Nikoo with data from my overfiltering example
  1.
  """
  win_1_ts_6 = np.array([-0.22992451, -0.27923477, -0.4202123, -0.18314374,
    -0.1129712, -0.23877507, 0.41932649, 0.40352192, 0.47053406, 0.17087914])
  win_1_ts_7 = np.array([0.35475717, 0.34063272, 0.18528659, 0.31803901,
    0.2333033, -0.02090214, -0.18189754, -0.28075432, -0.41915516, -0.52930964
  ])
  # Usually, this is not normalized.
  corr_incp = incp(win_1_ts_6, win_1_ts_7, len(win_1_ts_6))
  c_euc_d = corr_euc_d(win_1_ts_6, win_1_ts_7)
  assert corr_incp - c_euc_d < 1e-6

def test_compare_inc_p_euc_d_5():
  """
  Check equation 4 from Alizade Nikoo with data from my overfiltering example
  2.
  """
  win_2_ts_3 = np.array([-0.22798765, -0.1889726, -0.22798765, -0.18187973,
    -0.17833294, -0.10739677, -0.14641147, -0.1357711, -0.20316012,
    -0.22798765, -0.15705149, -0.11449035, -0.04355454, 0.10186387,
    0.00964731, -0.00808629, 0.11250388, 0.08412956, 0.05930203, 0.16925324,
    0.23664155, 0.30048413, 0.26501587, 0.44944934, 0.36077957])
  win_2_ts_6 = np.array([0.04219841, 0.20273505, 0.09636938, 0.13788767,
    0.20510736, 0.20273505, 0.26916375, 0.22646001, 0.01610114, 0.01570589,
    0.13472439, 0.23871759, 0.13630635, 0.05722418, 0.11851239, 0.01491491,
    -0.07800695, -0.18555869, -0.18199952, -0.32751102, -0.17844098,
    -0.2243088, -0.22589012, -0.21205106, -0.50109637])
  # Usually, this is not normalized.
  corr_incp = incp(win_2_ts_3, win_2_ts_6, len(win_2_ts_3))
  c_euc_d = corr_euc_d(win_2_ts_3, win_2_ts_6)
  assert corr_incp - c_euc_d < 1e-6

def test_compare_inc_p_euc_d_6():
  """
  Check equation 4 from Alizade Nikoo with data from my overfiltering example
  2.
  """
  win_2_ts_6 = np.array([0.04219841, 0.20273505, 0.09636938, 0.13788767,
    0.20510736, 0.20273505, 0.26916375, 0.22646001, 0.01610114, 0.01570589,
    0.13472439, 0.23871759, 0.13630635, 0.05722418, 0.11851239, 0.01491491,
    -0.07800695, -0.18555869, -0.18199952, -0.32751102, -0.17844098,
    -0.2243088, -0.22589012, -0.21205106, -0.50109637])
  win_2_ts_7 = np.array([-0.2868961, -0.09147876, -0.1553287, -0.13984987,
    -0.19789358, -0.22691718, -0.13211017, -0.01408579, -0.13017495,
    -0.25593903, -0.17854606, -0.16113318, -0.23659093, -0.04310765,
    0.09620004, 0.22389817, 0.24518148, 0.12135262, 0.10393858, 0.078786,
    0.16004939, 0.22583339, 0.30516157, 0.35933659, 0.33031415])
  # Usually, this is not normalized.
  corr_incp = incp(win_2_ts_6, win_2_ts_7, len(win_2_ts_6))
  c_euc_d = corr_euc_d(win_2_ts_6, win_2_ts_7)
  assert corr_incp - c_euc_d < 1e-6
