import pandas as pd
import folium
import sys
import json
import os

def crear_mapa(datos):
    try:
        # Extraer lat y lon de los datos
        lat = float(datos['lat'])
        lon = float(datos['lon'])
        
        # Leer el CSV
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, 'XVPCA_info_sconco3_2023.csv')
        df = pd.read_csv(csv_path)

        df['type'] = df['type'].str.replace('–', '-')

        # Diccionario de colores
        colores = {
            'U - Urbana': 'red',
            'S - Suburbana': 'blue',
            'R - Rural': 'green',
            'F - Fons': 'purple'
        }

        # Crear mapa centrado en la ubicación del usuario
        mapa = folium.Map(
            location=[lat, lon],
            zoom_start=10
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

        # Añadir marcador del usuario
        folium.Circle(
            location=[lat, lon],
            radius=10000,
            popup=f"Tu ubicación<br>Lat: {lat}, Lon: {lon}",
            color='orange',
            fill=True,
            fill_opacity=0.6
        ).add_to(mapa)

        # Añadir leyenda
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; 
                    right: 50px; 
                    z-index: 1000;
                    background-color: white;
                    padding: 10px;
                    border: 2px solid grey;
                    border-radius: 5px">
            <p><b>Tipos de estaciones:</b></p>
            <p>
                <i style="background: red; width: 15px; height: 15px; display: inline-block; border-radius: 50%;"></i> U - Urbana<br>
                <i style="background: blue; width: 15px; height: 15px; display: inline-block; border-radius: 50%;"></i> S - Suburbana<br>
                <i style="background: green; width: 15px; height: 15px; display: inline-block; border-radius: 50%;"></i> R - Rural<br>
                <i style="background: purple; width: 15px; height: 15px; display: inline-block; border-radius: 50%;"></i> F - Fons<br>
                <i style="background: orange; width: 15px; height: 15px; display: inline-block; border-radius: 50%;"></i> Tu ubicación
            </p>
        </div>
        '''
        mapa.get_root().html.add_child(folium.Element(legend_html))

        # Guardar el mapa
        mapa.save('public/mapa_estaciones.html')
        return True, "Mapa creado exitosamente"
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    try:
        # Leer datos de la entrada estándar
        input_data = sys.stdin.read()
        datos = json.loads(input_data)
        success, message = crear_mapa(datos)
        if success:
            print(json.dumps({"status": "success", "message": message}))
            sys.exit(0)
        else:
            print(json.dumps({"status": "error", "message": message}))
            sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(1)
