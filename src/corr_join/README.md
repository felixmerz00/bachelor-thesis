
# Customize Parameters
Define new parameter sets in `get_params` in [util.py](https://github.com/felixmerz00/bachelor-thesis/blob/main/src/corr_join/util.py) and pass the name of your parameter set when calling corr_join in [main.py](https://github.com/felixmerz00/bachelor-thesis/blob/main/src/corr_join/main.py).


# Running Tests
```
conda activate conda-env-ba
pytest src/corr_join/test_load_data.py
```
Replace `test_load_data.py` if you want to run a different test file.
