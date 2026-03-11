import rasterio
import numpy as np

# Path for the DEM raster file
dem_path = r"C:\Users\njsan\Documents\QGIS work\2014-Bernardo-Fire\RasterVectorClipped.tif"

min_elev = None
max_elev = None
sum_elev = 0
count = 0

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
        overwrite data variable for each block, so we only keep one block in memory at a time.
'''
with rasterio.open(dem_path) as dem:
    # Get the NoData value from the raster metadata
    nodata = dem.nodata
    # print("Nodata:", nodata)

    # Read the raster in blocks to handle large files efficiently
    for _, window in dem.block_windows(1):
        data = dem.read(1, window=window)

        # Remove NoData pixels
        # Runs if nodata is not -9999... (missing data, oceans, etc.) 
        if nodata is not None:
            # keep only valid data points [100, 200] instead of [-999.., 100, 200]
            data = data[data != nodata]

        if data.size == 0:
            continue

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