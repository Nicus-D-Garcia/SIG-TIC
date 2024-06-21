A library is created to estimate morphometric parameters of a given basin using a Digital Elevation Model (DEM). 
The library "morfocuenca" contains two functions. The first function, "cuencaStats," determines the basins from the DEM and then estimates parameters such as maximum, minimum, and average height, as well as slope. The second function, "cuencaIndex," includes the aforementioned parameters and also calculates 7 indices as outlined in the research by Karalis et al. (2014). For more information on the output indices of "cuencaIndex," it is suggested to review the script or type "help(morfocuenca)" in the Python console.

Note: The script only works with the SAGA plugin and library installed in QGIS; it is recommended to ensure this requirement is met.
