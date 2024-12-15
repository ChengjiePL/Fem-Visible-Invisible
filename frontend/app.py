from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from pathlib import Path
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/api/crear-mapa', methods=['POST'])
def crear_mapa():
    try:
        data = request.get_json()
        
        script_path = Path(__file__).parent / 'src' / 'concentracion.py'
        
        # Ejecutar el script de Python con las coordenadas
        proceso = subprocess.run(
            ['python3', str(script_path)],
            input=json.dumps(data),
            text=True,
            capture_output=True
        )
        
        if proceso.returncode == 0:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({
                "status": "error", 
                "message": proceso.stderr,
                "stdout": proceso.stdout
            }), 500
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
