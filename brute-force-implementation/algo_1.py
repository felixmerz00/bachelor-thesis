
# algorithm 1 Alizade Nikoo
def algorithm_1(t_series, n: int, h: int, T: int, k_s: int, k_e: int, k_b: int):
  epsilon_1 = sqrt(2*k_s*(1-T)/n)
  epsilon_2 = sqrt(2*k_e*(1-T)/n)
  # alpha = 1   # only needed when working with data streams

  # I skip the while loop, because my time series are not streams.
  for series, i in enumerate(t_series):
    continue

