import geopandas as gpd
from shapely.geometry import Point
import numpy as np

def population_within_radius(latitud, longitud, gdf, radi):
    """
    Calcula la población dentro de un radio específico basado en un archivo shapefile.

    Args:
        latitud (float): Coordenada de latitud del punto central.
        longitud (float): Coordenada de longitud del punto central.
        gdf (GeoDataFrame): GeoDataFrame que contiene los datos del shapefile con geometrías y población.
        radi (float): Radio de búsqueda en metros.

    Returns:
        dict: Un diccionario con el total de población y posibles desgloses.
    """
    # Crear el punto inicial a partir de las coordenadas
    punto = Point(longitud, latitud)

    # Convertir el GeoDataFrame al sistema de coordenadas UTM 31N ETRS89
    gdf = gdf.to_crs(epsg=25831)
    
    # Convertir el punto a UTM
    punto_utm = gpd.GeoSeries([punto], crs="EPSG:4326").to_crs(epsg=25831).iloc[0]

    # Filtrar el GeoDataFrame para que las geometrías sean válidas
    gdf = gdf[gdf.geometry.notnull() & gdf.is_valid & ~gdf.geometry.is_empty]

    # Calcular la distancia de cada geometría al punto
    gdf['distance'] = gdf.geometry.distance(punto_utm)

    # Filtrar las áreas dentro del radio
    gdf_dentro_radio = gdf[gdf['distance'] <= radi]

    # Sumar los valores de población dentro del radio
    poblacion_total = gdf_dentro_radio['TOTAL'].sum()
    desgloses = {
        'HOMES': gdf_dentro_radio['HOMES'].sum(),
        'DONES': gdf_dentro_radio['DONES'].sum(),
        'P_0_14': gdf_dentro_radio['P_0_14'].sum(),
        'P_15_64': gdf_dentro_radio['P_15_64'].sum(),
        'P_65_I_MES': gdf_dentro_radio['P_65_I_MES'].sum(),
        'P_ESPANYOL': gdf_dentro_radio['P_ESPANYOL'].sum(),
        'P_ESTRANGE': gdf_dentro_radio['P_ESTRANGE'].sum(),
    }

    return {
        'poblacion_total': poblacion_total,
        'desgloses': desgloses
    }

def populationOffset(poblacion, p_min, p_max, c_escala):
    """
    Ajusta el nivel de contaminación basado en la población normalizada.

    Args:
        poblacion (int): Cantidad de gente en el área.
        p_min (int): Población mínima esperada.
        p_max (int): Población máxima esperada.
        c_base (float): Nivel base de contaminación.
        c_escala (float): Factor de ajuste de contaminación.

    Returns:
        float: Nivel ajustado de contaminación.
    """
    # Normalizar la población al rango [-1, 1]
    p_norm = 2 * ((poblacion - p_min) / (p_max - p_min)) - 1
    p_norm = max(-1, min(p_norm, 1))  # Asegurar que esté en el rango [-1, 1]

    # Calcular el nivel ajustado de contaminación
    c_ajustado = 0 + (c_escala * p_norm)

    return c_ajustado

def popOffset(lat, long, r, escala, shapefile_path = "../Data/Poblacio/gridpoblacio01012022.shp"):
    # Ruta al shapefile con datos de población
    gdf = gpd.read_file(shapefile_path)

    # Coordenadas del punto central y radio
    latitud = lat
    longitud = long
    radi = r  # Radio en metros

    # Calcular la población dentro del radio
    resultado = population_within_radius(latitud, longitud, gdf, radi)
    poblacion = resultado['poblacion_total']

    # Parámetros para ajustar la contaminación
    p_min = gdf['TOTAL'].min()
    p_max = gdf['TOTAL'].max()
    c_escala = escala  # Factor de aumento de contaminación

    # Ajustar el nivel de contaminación basado en la población
    return populationOffset(poblacion, p_min, p_max, c_escala)