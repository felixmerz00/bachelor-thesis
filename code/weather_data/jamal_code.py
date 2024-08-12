import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import glob
from statsmodels.tsa.seasonal import seasonal_decompose

def read_nc_file(file_path: str, lon_point: float, lat_point: float):
  """
  Read a NetCDF file and extract data for a specific point.

  Parameters:
    file_path: Path to the NetCDF file.
    lon_point, lat_point: Coordinates of the specific point.

  Returns:
    np.ma.core.MaskedArray: A list of time entries (as np.float32), i.e., [11688. 11689. 11690. ...].
    np.ndarray: A list containing the precipitation data (as np.float32).
  """
  # Open the NetCDF file
  dataset = nc.Dataset(file_path, 'r')

  # Extract the variables
  time = dataset.variables['time'][:]
  lon = dataset.variables['lon'][:]
  lat = dataset.variables['lat'][:]
  pr = dataset.variables['pr'][:]

  # Find the nearest index for the given longitude and latitude
  lon_idx = np.abs(lon - lon_point).argmin()
  lat_idx = np.abs(lat - lat_point).argmin()
  print("lon:",lon_idx,"lat:", lat_idx)

  # Extract precipitation data for the specific point
  pr_point = pr[:, lat_idx, lon_idx]

  # Replace values greater than 10^5 or missing with NaN
  pr_point = np.where(pr_point > 1e5, np.nan, pr_point)
  pr_point = np.where(pr_point == dataset.variables['pr']._FillValue, np.nan, pr_point)

  # Replace NaN values with the previous valid value
  for i in range(1, len(pr_point)):
      if np.isnan(pr_point[i]):
          pr_point[i] = pr_point[i - 1]

  # Close the dataset
  dataset.close()

  # Return the time and precipitation data for the point
  return time, pr_point

def read_nc_file_grid(file_path: str):
  """
  Function to read a NetCDF file and extract data for the entire grid.

  Parameters:
    file_path: Path to the NetCDF file.

  Returns:
    np.ma.core.MaskedArray: A time grid.
    np.ma.core.MaskedArray: A longitude grid.
    np.ma.core.MaskedArray: A latitude grid.
    np.ndarray: A grid containing the precipitation data.
  """
  # Open the NetCDF file
  dataset = nc.Dataset(file_path, 'r')

  # Extract the variables
  time = dataset.variables['time'][:]
  lon = dataset.variables['lon'][:]
  lat = dataset.variables['lat'][:]
  pr = dataset.variables['pr'][:]

  # Replace values greater than 10^5 or missing with NaN
  pr = np.where(pr > 1e5, np.nan, pr)
  pr = np.where(pr == dataset.variables['pr']._FillValue, np.nan, pr)

  # Replace NaN values with the previous valid value
  for t in range(pr.shape[0]):
      for i in range(pr.shape[1]):
          for j in range(pr.shape[2]):
              if np.isnan(pr[t, i, j]) and t > 0:
                  pr[t, i, j] = pr[t-1, i, j]

  # Close the dataset
  dataset.close()

  # Return the time, longitude, latitude, and precipitation data
  return time, lon, lat, pr

# Path to the folder containing .nc files
folder_path = 'data/weather/precipitation-dataset-insitu-gridded-observations-global-and-regional-bcbbce6d-9ad0-4602-b2e4-d54f6f0e3bea'
# Specify the longitude and latitude of the point you are interested in
lon_point = -75.0  # Example longitude
lat_point = 40.0   # Example latitude

# List all .nc files in the folder, each file contains data for one year
nc_files = glob.glob(os.path.join(folder_path, '*.nc'))

# Initialize lists to store time and precipitation over all files, i.e. over all years
all_times = []
all_pr_points = []

# Initialize lists to store aggregated time and precipitation data for the grid
all_times_grid = []
all_pr_grid = []

# Read data from each .nc file
for file_path in nc_files:
  time, pr_point = read_nc_file(file_path, lon_point, lat_point)
  all_times.append(time)
  all_pr_points.append(pr_point)

  time_grid, lon_grid, lat_grid, pr_grid = read_nc_file_grid(file_path)
  all_times_grid.append(time_grid)
  all_pr_grid.append(pr_grid)

# Concatenate all times and precipitation data
all_times = np.concatenate(all_times)
all_pr_points = np.concatenate(all_pr_points)

all_times_grid = np.concatenate(all_times_grid)
all_pr_grid = np.concatenate(all_pr_grid, axis=0)

# Sort the data by time
sorted_indices = np.argsort(all_times)
all_times = all_times[sorted_indices]
all_pr_points = all_pr_points[sorted_indices]

sorted_indices_grid = np.argsort(all_times_grid)
all_times_grid = all_times_grid[sorted_indices_grid]
all_pr_grid = all_pr_grid[sorted_indices_grid, :, :]

# Save the data points to a CSV file
data = {
    'Time': all_times,
    'Precipitation': all_pr_points
}
df = pd.DataFrame(data)
df.to_csv('data/weather/pr_lon109_lat39.csv', index=False)

# Decompose the time series data for the point
decomposition = seasonal_decompose(all_pr_points, period=365, model='additive')

# Plotting the aggregated precipitation data over time for the specified point
plt.figure(figsize=(10, 6))
plt.plot(all_times, all_pr_points, marker='o', linestyle='-')
plt.xlabel('Time (days since 1948-01-01)')
plt.ylabel('Precipitation (mm/day)')
plt.title(f'Precipitation Time Series at Lon {lon_point}, Lat {lat_point}')
plt.grid(True)
plt.savefig('data/weather/precipitation_time_series.png')
plt.show()

# Plotting the decomposed components
plt.figure(figsize=(12, 8))

plt.subplot(411)
plt.plot(all_times, decomposition.observed, label='Observed')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(all_times, decomposition.trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(all_times, decomposition.seasonal, label='Seasonal')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(all_times, decomposition.resid, label='Residual')
plt.legend(loc='best')

plt.tight_layout()
plt.savefig('data/weather/decomposed_time_series.png')
plt.show()

# Calculate the time-averaged precipitation for the grid
avg_pr_grid = np.nanmean(all_pr_grid, axis=0)

# Plotting the heatmap of the time-averaged precipitation data
plt.figure(figsize=(12, 8))
plt.contourf(lon_grid, lat_grid, avg_pr_grid, cmap='viridis', levels=100)
plt.colorbar(label='Precipitation (mm/day)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.title('Time-Averaged Daily Precipitation Heatmap')
plt.savefig('data/weather/time_averaged_precipitation_heatmap.png')
plt.show()
