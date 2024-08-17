import

from code.brute_force_implementation.inc_p import incp

def compare_inc_p_euc_d():
  """
  Check equation 4 from Alizade Nikoo
  """
  assert inc_p.incp([1, 2, 3], [4, 5, 6], 3) == 1.0
