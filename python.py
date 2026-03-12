import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Path for the DEM raster file
dem_path = r"C:\Users\njsan\Documents\QGIS work\2014-Bernardo-Fire\RasterVectorClippedTest.tif"

all_elevations = []
window_size = 512

min_elev = None
max_elev = None

sum_elev = 0
count = 0

def calculate_slope(dem_path, window_size):
    all_slopes = []

    with rasterio.open(dem_path) as dem:
        nodata = dem.nodata
        # get pixel size from raster metadata
        xres, yres = dem.res

        '''
        block shape is (1, 74121), only 1 row, 74121 columns, 
        but need at least 2 rows and 2 columns for slope calculation
        need to manually loop
        can't use: for _, window in dem.block_windows(1):
        '''

        # loop through raster
        for row_off in range(0, dem.height, window_size):
            for col_off in range(0, dem.width, window_size):
                win = rasterio.windows.Window(
                    col_off, row_off,
                    min(window_size, dem.width - col_off),
                    min(window_size, dem.height - row_off)
                )

                # elevation for slope
                # converted to float for slope calculation
                data = dem.read(1, window=win).astype("float32")

                # Edge case where numpy needs at least 2x2 array
                # Skip blocks that are too small for slope calculation
                if data.shape[0] < 2 or data.shape[1] < 2:
                    continue

                if nodata is not None:
                    # Set NoData values to NaN for slope calculation
                    # change the -9999... to NaN to be ignored in slope calculation
                    data[data == nodata] = np.nan

                # get gradiants
                dz_dy, dz_dx = np.gradient(data, yres, xres)

                # calculate slope in radians
                slope = np.arctan(np.sqrt(dz_dx**2 + dz_dy**2))
                
                # convert slope to degrees
                slope_degrees = np.degrees(slope)

                # Add valid elevations to the list (no NaN values)
                all_slopes.extend(slope_degrees[~np.isnan(slope_degrees)])

    return np.array(all_slopes)

''' 
raster files are stored in blocks (tiles):
+-----+-----+-----+
| B1  | B2  | B3  |
+-----+-----+-----+
| B4  | B5  | B6  |
+-----+-----+-----+

for _, window in dem.block_windows(1):
    for each block in the raster,
    block 1 process
    block 2 process etc.
    until end

    dem.block_windows(1) 
        returns (block_index, window) for each block in the raster.
        ex. ((0,0), window(...)), 
            ((0,1), window(...)), etc.)
            don't need block_index for this task ((0,0), (0,1)), so we use _ to ignore it.
        get band 1 (elevation) -> dem.block_windows(1)

    data = dem.read(1, window=window)
        reads the data for the current block (window) from band 1 (elevation).
        automatically goes to next block after the current block
        overwrite data variable for each block, so we only keep one block in memory at a time.

    Slope formula for raster terrain analysis:
    slope = arctan(sqrt((dz/dx)^2 + (dz/dy)^2))
    where dz/dx = elevation change in x direction 
    dz/dy = are the elevation changes in y direction
'''
with rasterio.open(dem_path) as dem:
    # Get the NoData value from the raster metadata
    nodata = dem.nodata

    # block shape is (1, 74121), only 1 row, 74121 columns, 
    # but need at least 2 rows and 2 columns for slope calculation
    # print("Block shapes:", dem.block_shapes)

    slopes_degrees = calculate_slope(dem_path, window_size)

    # Read the raster in blocks to handle large files efficiently
    for _, window in dem.block_windows(1):
        # Data is stored in a single 2D numpy array 
        data = dem.read(1, window=window)

        # Remove NoData pixels
        # Runs if nodata is not -9999... (missing data, oceans, etc.) 
        if nodata is not None:
            # keep only valid data points [100, 200] instead of [-999.., 100, 200]
            # now changes to 1D array where data is != -9999...
            data = data[data != nodata]

        # After size is 0, we go to next block
        if data.size == 0:
            continue
        
        # Used for histogram
        all_elevations.extend(data)

        # Update min/max for each block
        wmin = data.min()
        wmax = data.max()

        # Update global min/max
        if min_elev is None or wmin < min_elev:
            min_elev = wmin

        if max_elev is None or wmax > max_elev:
            max_elev = wmax

        # get the sum and count for mean calculation
        sum_elev += data.sum()
        count += data.size

# Calculate mean elevation
mean_elev = sum_elev / count

# :.2f formats the output to 2 decimal places
print(f"Min elevation: {min_elev:.2f} m")
print(f"Max elevation: {max_elev:.2f} m")
print(f"Mean elevation: {mean_elev:.2f} m")

# Plot histogram of elevations
# x-axis: elevation values (meters)
# y-axis: number of pixels with that elevation
# shows terrain distribution, e.g. how many pixels are at 100m, 200m, etc.
plt.hist(all_elevations, bins=50)
plt.title("DEM Elevation Distribution")
plt.xlabel("Elevation (meters)")
plt.ylabel("Number of Pixels")
plt.grid(True)
plt.show()

plt.figure()
plt.hist(slopes_degrees, bins=50)
plt.title("Slope Distribution")
plt.xlabel("Slope (degrees)")
plt.ylabel("Pixel Count")
plt.grid(True)
plt.show()