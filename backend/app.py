import os

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from model import CarPricePredictor

app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir peticiones desde el frontend

# Inicializar el predictor
predictor = CarPricePredictor()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el servidor está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'Backend de valoración de vehículos funcionando correctamente',
        'model_trained': predictor.is_trained()
    })


@app.route('/api/train', methods=['POST'])
def train_model():
    """Endpoint para entrenar el modelo con nuevos datos"""
    try:
        # Verificar si se envió un archivo CSV
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó archivo de datos'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Archivo vacío'}), 400

        # Guardar temporalmente el archivo
        filepath = os.path.join('data', 'temp_training_data.csv')
        os.makedirs('data', exist_ok=True)
        file.save(filepath)

        # Entrenar el modelo
        metrics = predictor.train_model(filepath)

        # Limpiar archivo temporal
        os.remove(filepath)

        return jsonify({
            'message': 'Modelo entrenado exitosamente',
            'metrics': metrics
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint principal para predecir el precio de un vehículo"""
    try:
        # Obtener datos del request
        data = request.get_json()

        # Validar que se recibieron todos los campos necesarios
        required_fields = ['Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type',
                           'Seller_Type', 'Transmission', 'Owner']

        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Falta el campo requerido: {field}'}), 400

        # Validar tipos de datos
        try:
            data['Year'] = int(data['Year'])
            data['Present_Price'] = float(data['Present_Price'])
            data['Kms_Driven'] = int(data['Kms_Driven'])
            data['Owner'] = int(data['Owner'])
        except ValueError:
            return jsonify({'error': 'Los datos numéricos tienen formato incorrecto'}), 400

        # Validaciones de negocio
        current_year = pd.Timestamp.now().year
        if data['Year'] < 1990 or data['Year'] > current_year:
            return jsonify({'error': f'El año debe estar entre 1990 y {current_year}'}), 400

        if data['Present_Price'] <= 0:
            return jsonify({'error': 'El precio debe ser mayor a 0'}), 400

        if data['Kms_Driven'] < 0:
            return jsonify({'error': 'El kilometraje no puede ser negativo'}), 400

        if data['Fuel_Type'] not in ['Petrol', 'Diesel', 'CNG']:
            return jsonify({'error': 'Tipo de combustible inválido'}), 400

        if data['Seller_Type'] not in ['Dealer', 'Individual']:
            return jsonify({'error': 'Tipo de vendedor inválido'}), 400

        if data['Transmission'] not in ['Manual', 'Automatic']:
            return jsonify({'error': 'Tipo de transmisión inválido'}), 400

        if data['Owner'] not in [0, 1, 2, 3]:
            return jsonify({'error': 'Número de dueños inválido'}), 400

        # Realizar la predicción
        prediction = predictor.predict(data)

        if prediction is None:
            return jsonify({'error': 'El modelo no está entrenado. Por favor, entrena el modelo primero.'}), 503

        # Calcular rango de confianza (±10%)
        estimated_price = float(prediction)
        confidence = predictor.get_model_confidence()

        # Calcular rango basado en la confianza
        margin = 0.15 if confidence < 0.8 else 0.10  # Más margen si hay baja confianza
        price_min = estimated_price * (1 - margin)
        price_max = estimated_price * (1 + margin)

        # Preparar respuesta
        response = {
            'estimatedPrice': round(estimated_price, 2),
            'priceRange': {
                'min': round(price_min, 2),
                'max': round(price_max, 2)
            },
            'confidence': round(confidence * 100, 2),  # Convertir a porcentaje
            'message': get_confidence_message(confidence),
            'details': {
                'vehicleAge': current_year - data['Year'],
                'depreciationFactor': calculate_depreciation(data['Year'], current_year),
                'mileageCategory': categorize_mileage(data['Kms_Driven'])
            }
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error en predicción: {str(e)}")
        return jsonify({'error': f'Error al procesar la solicitud: {str(e)}'}), 500


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Endpoint para obtener información sobre el modelo entrenado"""
    try:
        if not predictor.is_trained():
            return jsonify({
                'trained': False,
                'message': 'El modelo no ha sido entrenado aún'
            })

        info = predictor.get_model_info()
        return jsonify({
            'trained': True,
            'info': info
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_confidence_message(confidence):
    """Generar mensaje basado en el nivel de confianza"""
    if confidence >= 0.9:
        return "Estimación muy confiable basada en datos similares"
    elif confidence >= 0.8:
        return "Estimación confiable con buena precisión"
    elif confidence >= 0.7:
        return "Estimación moderadamente confiable"
    else:
        return "Estimación aproximada, puede variar según el mercado"


def calculate_depreciation(year, current_year):
    """Calcular factor de depreciación"""
    age = current_year - year
    # Depreciación aproximada del 15% anual
    depreciation = 1 - (0.15 * age)
    return max(0.2, min(1.0, depreciation))  # Entre 20% y 100%


def categorize_mileage(kms):
    """Categorizar el kilometraje"""
    if kms < 30000:
        return "Bajo - Excelente estado"
    elif kms < 80000:
        return "Medio - Buen estado"
    elif kms < 150000:
        return "Alto - Estado aceptable"
    else:
        return "Muy alto - Mayor desgaste"


if __name__ == '__main__':
    # Crear directorio para datos si no existe
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Entrenar el modelo automáticamente si existe un archivo de datos
    data_file = 'data/car_prediction_data.csv'
    if os.path.exists(data_file):
        print("Entrenando modelo con datos existentes...")
        try:
            metrics = predictor.train_model(data_file)
            print(
                f"Modelo entrenado exitosamente. R² Score: {metrics['r2_score']:.4f}")
        except Exception as e:
            print(
                f"Advertencia: No se pudo entrenar el modelo automáticamente: {e}")
    else:
        print(f"Advertencia: No se encontró el archivo {data_file}")
        print("El modelo se entrenará cuando se proporcionen datos.")

    print("\n🚀 Servidor backend iniciado en http://localhost:5000")
    print("📊 Endpoints disponibles:")
    print("  - GET  /api/health       - Verificar estado del servidor")
    print("  - POST /api/predict      - Predecir precio de vehículo")
    print("  - POST /api/train        - Entrenar modelo con nuevos datos")
    print("  - GET  /api/model-info   - Información del modelo")

    # En producción usar debug=False
    is_debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=is_debug, host='0.0.0.0', port=5000)
