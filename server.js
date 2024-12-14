const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Endpoint para crear el mapa
app.post("/api/crear-mapa", (req, res) => {
  const coordenadas = req.body;

  const pythonProcess = spawn("python3", [
    path.join(__dirname, "src", "concentracion.py"),
    JSON.stringify(coordenadas),
  ]);

  // Añade manejo de errores
  pythonProcess.stderr.on("data", (data) => {
    console.error(`Error en Python: ${data}`);
  });

  pythonProcess.stdout.on("data", (data) => {
    console.log(`Salida de Python: ${data}`);
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Servidor corriendo en puerto ${PORT}`);
});
