import pandas as pd
import folium
import sys
import json
from pathlib import Path

def crear_mapa(coordenadas):
    try:
        # Asegurarnos que el directorio public existe
        Path("public").mkdir(exist_ok=True)
        
        # Leer el CSV
        df = pd.read_csv('XVPCA_info_sconco3_2023.csv')

        # Normalizar los guiones
        df['type'] = df['type'].str.replace('–', '-')

        # Diccionario de colores con guión normal
        colores = {
            'U - Urbana': 'red',
            'S - Suburbana': 'blue',
            'R - Rural': 'green',
            'F - Fons': 'purple'
        }

        # Crear un mapa centrado en Cataluña
        mapa = folium.Map(
            location=[41.5912, 1.5206],
            zoom_start=8
        )

        # Añadir marcadores para cada estación
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[float(row['lat']), float(row['lon'])],
                radius=8,
                popup=f"Código: {row['code']}<br>Tipo: {row['type']}",
                color=colores[row['type']],
                fill=True
            ).add_to(mapa)

        # Añadir marcadores para las coordenadas del usuario
        if isinstance(coordenadas, dict):
            coordenadas = [coordenadas]  # Convertir un solo punto en lista
            
        for coord in coordenadas:
            folium.Circle(
                location=[float(coord['lat']), float(coord['lon'])],
                radius=10000,
                popup=f"Lat: {coord['lat']}, Lon: {coord['lon']}",
                color='orange',
                fill=True,
                fill_opacity=0.6
            ).add_to(mapa)

        # Guardar el mapa
        mapa.save('public/mapa_estaciones.html')
        return True, "Mapa creado exitosamente"
        
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    try:
        # Recibir coordenadas como argumento JSON
        coordenadas_json = sys.argv[1]
        coordenadas = json.loads(coordenadas_json)
        success, message = crear_mapa(coordenadas)
        if success:
            print(json.dumps({"status": "success", "message": message}))
            sys.exit(0)
        else:
            print(json.dumps({"status": "error", "message": message}))
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
