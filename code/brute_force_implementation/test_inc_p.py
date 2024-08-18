from test_setup import get_first_normalized_window_audio_data, get_first_window_audio_data
from inc_p import incp
from util import corr_euc_d


def test_compare_inc_p_euc_d():
  """
  Check equation 4 from Alizade Nikoo
  """
  w = get_first_window_audio_data()
  W = get_first_normalized_window_audio_data()
  corr_incp = incp(w[0], w[0], len(w[0]))
  c_euc_d = corr_euc_d(W[0], W[0])
  assert corr_incp - c_euc_d < 1e-9

def test_compare_inc_p_euc_d_2():
  """
  Check equation 4 from Alizade Nikoo but with all normalized data.
  """
  w = get_first_window_audio_data()
  W = get_first_normalized_window_audio_data()
  # Usually, this is not normalized.
  corr_incp = incp(W[0], W[0], len(W[0]))
  c_euc_d = corr_euc_d(W[0], W[0])
  assert corr_incp - c_euc_d < 1e-9
