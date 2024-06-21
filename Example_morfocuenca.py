
# Importing libraries
import morfocuenca

### Objective: perform random sampling of raster data within a polygon ###


##-----------------------------------------------------------------##
##-------------------------- INPUTS -------------------------------##
##-----------------------------------------------------------------##


# Path to input files || The same DEM to test both functions
# You choose the DEM that you want to process.

# Example:
# dem = r'E:\Respaldo\UACh\S1\SIGYTIC\31Mayo\Semana_11\Datos_semana_11\DEM_Area1.tif'

dem = 'DEM_Area1.tif''

##-----------------------------------------------------------------##
##-----------------------------------------------------------------##
##-----------------------------------------------------------------##

# Output to use function 1 from the library (cuencaStats)

# Example

# bas_path = r'E:\Respaldo\UACh\S1\SIGYTIC\P6\Output_cuencaStats.gpkg'
bas_path = 'Output_cuencaStats.gpkg'

output = morfocuenca.cuencaStats(dem, bas_path, 10)

##-----------------------------------------------------------------##
##-----------------------------------------------------------------##
##-----------------------------------------------------------------##

# Output to use function 2 from the library (cuencaIndex)

# Example
# basin_path = r'E:\Respaldo\UACh\S1\SIGYTIC\P6\Output_cuencaIndex.gpkg'
basin_path = 'Output_cuencaIndex.gpkg'

output2 = morfocuenca.cuencaIndex(dem, basin_path, 10)

print('Done II')
