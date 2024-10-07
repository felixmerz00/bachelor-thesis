# Standard library imports
# Third-party imports 
import pandas as pd
import pytest
# Local imports
import load_data as ld
import util
from corr_join import corr_join


def test_gdrive_load_limited():
  """
  Test if gdrive returns the requested number of rows.
  """
  m = 2
  result = ld.gdrive("chlorine", m)

  # Assert that the DataFrame has the expected number of rows
  assert result.shape[0] == m, f"Expected {m} rows, but got {result.shape[0]}"


def test_gdrive_data_type():
  """
  Test if gdrive returns a pandas.DataFrame.
  """
  m = 10
  result = ld.gdrive("chlorine", m)

  # Assert that the DataFrame has the expected number of rows
  assert isinstance(result, pd.DataFrame), f"Expected result to be a pandas DataFrame, but got {type(result)}"


def test_gdrive_num_corr_pairs():
  """
  Test if Corr Join yields the same result for gdrive as well as for gdrive_np.
  """
  np_ndarray = ld.load_data("chlorine_np", m=10)
  pd_df = ld.load_data("chlorine", m=10)

  n, h, T, k_s, k_e, k_b = util.get_params("chlorine_params_1")
  num_corr_pairs_np, _ = corr_join(np_ndarray, n, h, T, k_s, k_e, k_b)
  num_corr_pairs_pd, _ = corr_join(pd_df, n, h, T, k_s, k_e, k_b)

  assert num_corr_pairs_np == num_corr_pairs_pd, f"Corr Join reported a different number of correlated window pairs. np ndarray: {num_corr_pairs_np}, pd df: {num_corr_pairs_pd}"


if __name__ == '__main__':
  pytest.main()
