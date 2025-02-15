# Standard library imports
# Third-party imports 
import pandas as pd
import pytest
# Local imports
import load_data as ld
import util
from corr_join import corr_join


def test_gdrive_m():
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


if __name__ == '__main__':
  pytest.main()