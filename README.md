# GIS-Analyzing-2007-Fire

This project analyzes terrain within the 4S Ranch and Rancho Bernardo wildfire perimeter from the 2007 Witch Creek Fire through analysis of a Digital Elevation Model (DEM) in Python. Elevation and slope distributions are computed and visualized to examine how terrain characteristics may influence wildfire behavior.

## Terrain Metrics Computed

### Elevation statistics
Minimum elevation <br>
Maximum elevation <br>
Mean elevation <br>
Elevation Distribution histogram

### Slope statistics
Mean slope <br>
Maximum slope <br>
Slope Distribution histogram

Slope is calculated using the terrain gradient: <br>
slope = arctan( $\sqrt((($\frac{dz}{dx}$) )^2 + (dz/dy)^2)$)

Where: <br>
dz/dx = elevation change in x direction <br>
dz/dy = elevation change in y direction <br>

The result is then converted from radians to degrees.

### How to run this project:
1. Clone the repository: <br>
   **```https://github.com/njsandburg/GIS-Analyzing-2007-Fire.git```**
   
2. Install rasterio: <br>
   **```pip install rasterio numpy matplotlib```**
   
3. Run the python code: <br>
   **```python python.py```**

The python code will compute terrain statistics and generate elevation and slope distribution graphs.
