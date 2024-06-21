def cuencaStats(dem0, basins, sizekm2):
    """
    Delimita cuencas y calcula altitud máxima, mínima y media, además de la pendiente media de cuencas.
    Ejemplo de uso:
    morfocuenca.cuencaStats(dem0, basins, sizekm2)
    
    Parameters:
    dem0 (str): ruta a DEM
    basins (str): ruta a archivo de salida GPKG con vector de cuencas y su estadística
    sizekm2 (float): tamaño mínimo de la cuenca en km2
    
    Nota: Guardar función "morfocuenca.py" en librería de OSGeo4w ==> "~\\OSGeo4W\\apps\\Python312\\Lib"
    """
    
    #__________________________________________________________________________#
    # Importando librerías
    import processing
    import geopandas as gpd
    import rasterio as rs
    
    dem = rs.open(dem0)
    s1, s2 = dem.res
    resArea = s1 * s2
    area = (sizekm2 * (10**6)) / resArea

    print('Área calculada correctamente!')
    
    #__________________________________________________________________________#
    # Calculo de pendiente (Archivo temporal)
    slope = processing.run("native:slope", {'INPUT': dem0, 'Z_FACTOR': 1, 'OUTPUT': 'TEMPORARY_OUTPUT', '--overwrite': True})
    print('Pendiente calculada correctamente!')
    
    #__________________________________________________________________________#
    # Delimitación de cuenca (Archivo temporal)
    grass_ws = processing.run("grass7:r.watershed", {
        'elevation': dem0,
        'threshold': area,
        'accumulation': 'TEMPORARY_OUTPUT',
        'drainage': 'TEMPORARY_OUTPUT',
        'basin': 'TEMPORARY_OUTPUT',
        'stream': 'TEMPORARY_OUTPUT',
        'half_basin': 'TEMPORARY_OUTPUT',
        'length_slope': 'TEMPORARY_OUTPUT',
        'slope_steepness': 'TEMPORARY_OUTPUT',
        'tci': 'TEMPORARY_OUTPUT',
        'spi': 'TEMPORARY_OUTPUT',
        'GRASS_REGION_CELLSIZE_PARAMETER': 0,
        '--overwrite': True
    })
    
    #__________________________________________________________________________#
    # Poligonizar cuencas (Archivo temporal)
    basins_vec = processing.run("gdal:polygonize", {
        'INPUT': grass_ws['basin'],
        'BAND': 1,
        'FIELD': 'DN',
        'EIGHT_CONNECTEDNESS': False,
        'OUTPUT': 'TEMPORARY_OUTPUT',
        '--overwrite': True
    })
    print('Poligonización completada correctamente!')
    
    #__________________________________________________________________________#
    # Corrección de geometrías (Archivo temporal)
    fix_geom = processing.run("native:fixgeometries", {
        'INPUT': basins_vec['OUTPUT'],
        'METHOD': 1,
        'OUTPUT': 'TEMPORARY_OUTPUT',
        '--overwrite': True
    })
    print('Corrección de geometrías completada correctamente!')
    
    #__________________________________________________________________________#
    # Estadística de zona (pendiente y altitud)
    stats_height = processing.run("native:zonalstatisticsfb", {
        'INPUT': fix_geom['OUTPUT'],
        'INPUT_RASTER': dem0,
        'RASTER_BAND': 1,
        'COLUMN_PREFIX': 'Altura_',
        'STATISTICS': [2, 5, 6],
        'OUTPUT': 'TEMPORARY_OUTPUT',
        '--overwrite': True
    })
    print('Estadísticas de altitud calculadas correctamente!')
    
    stats_slope = processing.run("native:zonalstatisticsfb", {
        'INPUT': stats_height['OUTPUT'],
        'INPUT_RASTER': slope['OUTPUT'],
        'RASTER_BAND': 1,
        'COLUMN_PREFIX': 'Pendiente_',
        'STATISTICS': [2],
        'OUTPUT': basins,
        '--overwrite': True
    })
    print('Estadísticas de pendiente calculadas correctamente!')
    print('Cuenca Stats ==> Procesamiento completado!')

#__________________________________________________________________________#
#__________________________________________________________________________#
#__________________________________________________________________________#

def cuencaIndex(dem0, basins, sizekm2, threshold):
    """
    IMPORTANTE!: Se necesita que SAGA este correctamente instalado para utilizar sus herramientas en QGIS. Se recomienda revisar mediante OSGeo4W su instalación y además instalar complemento (Processing Saga NextGen Provider).
    
    Delimita cuencas y calcula altitud máxima, mínima y media, además de la pendiente media de cuencas.
    Además, agrega parámetros de Karalis et al. (2014):
    
    1) Área (km**2)
    2) Perímetro (km)
    3) Relieve (m)
    4) Factor de Compresión (adimensional)
    5) Circularidad de la cuenca (adimensional)
    6) Número de rugosidad de Melton (adimensional)
    7) Largo total de canales (km)
    8) Densidad de canales (adimensional)
    
    #%%
    Ejemplo de uso:
    dem0 = ruta de dem 
    basins = ruta de archivo de salida
    sizekm2 = 10
    threshold = 5
    
    morfocuenca.cuencaIndex(dem0, basins, sizekm2, threshold)
    #%%
    
    Parametros:
    dem0 (str): ruta a DEM
    basins (str): ruta a archivo de salida GPKG con vector de cuencas y estadísticos de Karalis et al., (2014).
    sizekm2 (float): tamaño mínimo de la cuenca en km2
    threshold (int): Umbral de detección para algoritmo Strahler order
    
    Nota: Guardar función "morfocuenca.py" en librería de OSGeo4w ==> "~\\OSGeo4W\\apps\\Python312\\Lib"
    
    Referencia: Karalis, S., et al. (2014). Assessment of the relationships among catchments’ morphometric parameters and hydrologic indices. International Journal of Geosciences, 5(13), 1571-1583.
    """
    
    #__________________________________________________________________________#
    # Importando librerías
    import processing
    import geopandas as gpd
    import rasterio as rs
    
    dem = rs.open(dem0)
    s1, s2 = dem.res
    resArea = s1 * s2
    area = (sizekm2 * (10**6)) / resArea

    print('Area calculada correctamente!')
    
    #__________________________________________________________________________#
    # Calculo de pendiente (Archivo temporal)
    slope = processing.run("native:slope", {
        'INPUT': dem0,
        'Z_FACTOR': 1, 
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    
    print('Pendiente calculada correctamente!')
    
    #__________________________________________________________________________#
    # Delimitación de cuenca (Archivo temporal)
    grass_ws = processing.run("grass7:r.watershed", {
        'elevation': dem0,
        'threshold': area,
        'accumulation': 'TEMPORARY_OUTPUT',
        'drainage': 'TEMPORARY_OUTPUT',
        'basin': 'TEMPORARY_OUTPUT',
        'stream': 'TEMPORARY_OUTPUT',
        'half_basin': 'TEMPORARY_OUTPUT',
        'length_slope': 'TEMPORARY_OUTPUT',
        'slope_steepness': 'TEMPORARY_OUTPUT',
        'tci': 'TEMPORARY_OUTPUT',
        'spi': 'TEMPORARY_OUTPUT',
        'GRASS_REGION_CELLSIZE_PARAMETER': 0,
        '--overwrite': True
    })
    
    #__________________________________________________________________________#
    # Poligonizar cuencas (Archivo temporal)
    basins_vec = processing.run("gdal:polygonize", {
        'INPUT': grass_ws['basin'],
        'BAND': 1,
        'FIELD': 'DN',
        'EIGHT_CONNECTEDNESS': False,
        'OUTPUT': 'TEMPORARY_OUTPUT',
        '--overwrite': True
    })
    print('Poligonización completada correctamente!')
    
    #__________________________________________________________________________#
    # Corrección de geometrías (Archivo temporal)
    fix_geom = processing.run("native:fixgeometries", {
        'INPUT': basins_vec['OUTPUT'],
        'METHOD': 1,
        'OUTPUT': 'TEMPORARY_OUTPUT',
        '--overwrite': True
    })
    print('Corrección de geometrías completada correctamente!')
    
    #__________________________________________________________________________#
    # Estadística de zona (pendiente y altitud)
    stats_height = processing.run("native:zonalstatisticsfb", {
        'INPUT': fix_geom['OUTPUT'],
        'INPUT_RASTER': dem0,
        'RASTER_BAND': 1,
        'COLUMN_PREFIX': 'Altura_',
        'STATISTICS': [2, 5, 6],
        'OUTPUT': 'TEMPORARY_OUTPUT',
        '--overwrite': True
    })
    print('Estadísticas de altitud calculadas correctamente!')
    
    stats_slope = processing.run("native:zonalstatisticsfb", {
        'INPUT': stats_height['OUTPUT'],
        'INPUT_RASTER': slope['OUTPUT'],
        'RASTER_BAND': 1,
        'COLUMN_PREFIX': 'Pendiente_',
        'STATISTICS': [2],
        'OUTPUT': 'TEMPORARY_OUTPUT',
        '--overwrite': True
    })
    print('Estadísticas de pendiente calculadas correctamente!')
    
    #__________________________________________________________________________#
    # Parámetros de Karalis et al., (2014)
    
    # Area
    area_calc = processing.run("native:fieldcalculator", {
        'INPUT': stats_slope['OUTPUT'],
        'FIELD_NAME': 'Area',
        'FIELD_TYPE': 0,
        'FORMULA': '$area / 1e6',
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    print('Área calculada correctamente!')
    
    #__________________________________________________________________________#
    # Perimetro
    perimeter = processing.run("native:fieldcalculator", {
        'INPUT': area_calc['OUTPUT'],
        'FIELD_NAME': 'Perimetro',
        'FIELD_TYPE': 0,
        'FORMULA': '$perimeter',
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    print('Perímetro calculado correctamente!')
    
    #__________________________________________________________________________#
    # Relieve
    relief = processing.run("native:fieldcalculator", {
        'INPUT': perimeter['OUTPUT'],
        'FIELD_NAME': 'Relief',
        'FIELD_TYPE': 0,
        'FORMULA': '(Altura_max) - (Altura_min)',
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    print('Relieve calculado correctamente!')
    
    #__________________________________________________________________________#
    # Compactamiento
    compact = processing.run("native:fieldcalculator", {
        'INPUT': relief['OUTPUT'],
        'FIELD_NAME': 'Compactness_factor',
        'FIELD_TYPE': 0,
        'FORMULA': 'Perimetro / (2 * sqrt(pi() * Area))',
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    print('Factor de compresión calculado correctamente!')
    
    #__________________________________________________________________________#
    # Circularidad
    circularity = processing.run("native:fieldcalculator", {
        'INPUT': compact['OUTPUT'],
        'FIELD_NAME': 'Circularity',
        'FIELD_TYPE': 0,
        'FORMULA': '(4 * pi() * Area) / (Perimetro ^ 2)',
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    print('Circularidad calculada correctamente!')
    
    #__________________________________________________________________________#
    # Rugosidad de Melton
    melton = processing.run("native:fieldcalculator", {
        'INPUT': circularity['OUTPUT'],
        'FIELD_NAME': 'Meltons_ruggedness',
        'FIELD_TYPE': 0,
        'FORMULA': 'Relief * (Area ^ -0.5)',
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    print('Número de rugosidad de Melton calculado correctamente!')
    
    #__________________________________________________________________________#
    # Longitud total de canales dentro de la cuenca
    channel = processing.run("sagang:channelnetworkanddrainagebasins", {
        'DEM':dem0,
        'DIRECTION':
        'TEMPORARY_OUTPUT',
        'CONNECTION':'TEMPORARY_OUTPUT',
        'ORDER':'TEMPORARY_OUTPUT',
        'BASIN':'TEMPORARY_OUTPUT',
        'SEGMENTS':'TEMPORARY_OUTPUT',
        'BASINS':'TEMPORARY_OUTPUT',
        'NODES':'TEMPORARY_OUTPUT',
        'THRESHOLD':threshold,
        'SUBBASINS':True, 
        '--overwrite': True
    })
    
    #__________________________________________________________________________#
    # Largo de canales
    channel_length = processing.run("native:fieldcalculator", {
        'INPUT': channel['SEGMENTS'],
        'FIELD_NAME':'Total_length_channels',
        'FIELD_TYPE':0,
        'FIELD_LENGTH':0,
        'FIELD_PRECISION':0,
        'FORMULA':'sum( "LENGTH" )',
        'OUTPUT': 'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    
    print('Canales obtenidos correctamente!')
    
    #__________________________________________________________________________#
    # Sumar longitud de líneas || Esto permite fucionar las líneas de los ríos que se ubican dentro de las subcuencas || Además se obtiene el largo y número de ríos por subcuenca
    aux =  processing.run("native:sumlinelengths", {
        'POLYGONS': melton['OUTPUT'],
        'LINES': channel_length['OUTPUT'],
        'LEN_FIELD':'LENGTH',
        'COUNT_FIELD':'COUNT',
        'OUTPUT':'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    
    #__________________________________________________________________________#
    # Calculadora de campos || Se realiza la suma total, es decir, considerando todos los ríos para toda el área de estudio (todas las subcuencas)
    aux2 = processing.run("native:fieldcalculator", {
        'INPUT': aux['OUTPUT'],
        'FIELD_NAME':'Total_length_channel',
        'FIELD_TYPE':0,
        'FIELD_LENGTH':0,
        'FIELD_PRECISION':0,
        'FORMULA':'sum(LENGTH)',
        'OUTPUT':'TEMPORARY_OUTPUT', 
        '--overwrite': True
    })
    
    print('Calculo de largos de canales obtenidos correctamente!')

    #__________________________________________________________________________#
    # Densidad de drenaje
    aux3 = processing.run("native:fieldcalculator", {
        'INPUT':aux2['OUTPUT'],
        'FIELD_NAME':'Drainage_density',
        'FIELD_TYPE':0,
        'FIELD_LENGTH':0,
        'FIELD_PRECISION':0,
        'FORMULA':'(Total_length_channel)/(Area)',
        'OUTPUT':basins, 
        '--overwrite': True
    })
    
    print('Densidad de drenaje obtenida correctamente!')

    print('Cuenca Index ==> Procesamiento completado!')
