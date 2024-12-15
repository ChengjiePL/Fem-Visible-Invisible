import React, { useState } from "react";
import "../styles/Datos.css";

function Datos() {
  const [latitud, setLatitud] = useState("");
  const [longitud, setLongitud] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [mostrarMapa, setMostrarMapa] = useState(false);
  const [coordenadas, setCoordenadas] = useState([
    { lat: "", lon: "" },
    { lat: "", lon: "" },
    { lat: "", lon: "" },
    { lat: "", lon: "" },
  ]);
  const [mapaUrl, setMapaUrl] = useState("../../public/mapa_estaciones.html");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!latitud || !longitud) {
      setMensaje("Por favor, ingrese ambas coordenadas");
      return;
    }

    const lat = parseFloat(latitud);
    const lon = parseFloat(longitud);

    if (
      isNaN(lat) ||
      isNaN(lon) ||
      lat < -90 ||
      lat > 90 ||
      lon < -180 ||
      lon > 180
    ) {
      setMensaje("Por favor, ingrese coordenadas válidas");
      return;
    }

    try {
      const response = await fetch("/api/crear-mapa", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          lat: lat,
          lon: lon,
        }),
      });

      if (response.ok) {
        setMostrarMapa(true);
        // setMensaje("Mapa creado exitosamente");
        // Forzar recarga del iframe
        const timestamp = Date.now();
        setMapaUrl(`/mapa_estaciones.html?t=${timestamp}`);
      } else {
        setMensaje("Error al crear el mapa");
      }
    } catch (error) {
      console.error("Error:", error);
      setMensaje("Error de conexión al servidor");
    }
  };

  return (
    <div className="coordenadas-container">
      <div className="coordenadas-card">
        <h2>Ingresar Coordenadas</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="latitud">Latitud</label>
            <input
              id="latitud"
              type="text"
              value={latitud}
              onChange={(e) => setLatitud(e.target.value)}
              placeholder="Ej: 41.40338"
            />
          </div>
          <div className="input-group">
            <label htmlFor="longitud">Longitud</label>
            <input
              id="longitud"
              type="text"
              value={longitud}
              onChange={(e) => setLongitud(e.target.value)}
              placeholder="Ej: 2.17403"
            />
          </div>
          <button type="submit">Buscar</button>
        </form>
        {mensaje && <div className="mensaje">{mensaje}</div>}
        <div className="mapa-container">
          {mostrarMapa ? (
            <div className="mapa-container">
              <iframe
                src={mapaUrl}
                style={{ width: "100%", height: "500px", border: "none" }}
                title="Mapa de estaciones"
              />
            </div>
          ) : (
            <iframe
              src={"../../public/mapa.html"}
              style={{ width: "100%", height: "500px", border: "none" }}
              title="Mapa de estaciones"
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default Datos;
