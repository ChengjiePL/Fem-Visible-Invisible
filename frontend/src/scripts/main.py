from no2_prediction import predict_no2_concentration
from no2_utils import plot_concentration_vs_time
def main():
    try:
        lat = float(input("Inserte la latitud: "))
        lon = float(input("Inserte la longitud: "))

        if not (-90 <= lat <= 90):
            print("Error: La latitud ha de estar en el rang [-90, 90].")
            return
        if not (-180 <= lon <= 180):
            print("Error: La longitud ha de estar en el rang [-180, 180].")
            return

        result = predict_no2_concentration(lat, lon)
        
        plot_concentration_vs_time(result)

        print(f"Condentracio de No2 predita: {result} µg/m³")

    except ValueError:
        print("Error: Entrada inválida. Asegúrate de introducir números válidos para latitud y longitud.")

if __name__ == "__main__":
    main()
