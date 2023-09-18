from flask import Flask, request, jsonify

app = Flask(__name__)

# Ruta para cargar datos desde un archivo CSV
@app.route('/cargar-csv', methods=['POST'])
def cargar_csv():
    try:
        # Obtener el archivo CSV desde la solicitud
        archivo = request.files['archivo_csv']

        if not archivo:
            return jsonify({'error': 'No se proporcionó un archivo CSV'}), 400
        import pandas as pd
        df = pd.read_csv(archivo)

        # Devolver una respuesta exitosa
        return jsonify({'mensaje': 'Archivo CSV cargado exitosamente'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
