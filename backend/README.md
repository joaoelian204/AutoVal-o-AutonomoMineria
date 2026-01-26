# Backend de Valoración de Vehículos Usados

Backend en Flask que utiliza Machine Learning (Random Forest) para predecir el precio de vehículos usados basándose en sus características.

## 🚀 Características

- **API RESTful** con Flask
- **Modelo de Machine Learning** (Random Forest Regressor)
- **Preprocesamiento automático** de datos
- **Optimización de hiperparámetros** con GridSearchCV
- **Persistencia del modelo** entrenado
- **CORS habilitado** para integración con frontend

## 📋 Requisitos

- Python 3.8+
- pip

## 🔧 Instalación

1. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

2. **Preparar datos de entrenamiento:**
   - Coloca tu archivo `car_prediction_data.csv` en la carpeta `data/`
   - El archivo debe contener las siguientes columnas:
     - `Year`: Año del vehículo
     - `Present_Price`: Precio actual del modelo nuevo
     - `Kms_Driven`: Kilometraje
     - `Fuel_Type`: Tipo de combustible (Petrol/Diesel/CNG)
     - `Seller_Type`: Tipo de vendedor (Dealer/Individual)
     - `Transmission`: Tipo de transmisión (Manual/Automatic)
     - `Owner`: Número de dueños previos (0-3)
     - `Selling_Price`: Precio de venta (variable objetivo)

3. **Iniciar el servidor:**

```bash
python app.py
```

El servidor estará disponible en `http://localhost:5000`

## 📡 API Endpoints

### 1. Health Check

```http
GET /api/health
```

Verifica el estado del servidor y del modelo.

**Respuesta:**

```json
{
  "status": "ok",
  "message": "Backend de valoración de vehículos funcionando correctamente",
  "model_trained": true
}
```

### 2. Predecir Precio

```http
POST /api/predict
Content-Type: application/json
```

**Request Body:**

```json
{
  "Year": 2015,
  "Present_Price": 9.85,
  "Kms_Driven": 6900,
  "Fuel_Type": "Petrol",
  "Seller_Type": "Dealer",
  "Transmission": "Manual",
  "Owner": 0
}
```

**Respuesta:**

```json
{
  "estimatedPrice": 8.75,
  "priceRange": {
    "min": 7.88,
    "max": 9.63
  },
  "confidence": 92.5,
  "message": "Estimación muy confiable basada en datos similares",
  "details": {
    "vehicleAge": 11,
    "depreciationFactor": 0.35,
    "mileageCategory": "Bajo - Excelente estado"
  }
}
```

### 3. Entrenar Modelo

```http
POST /api/train
Content-Type: multipart/form-data
```

Sube un archivo CSV para entrenar el modelo.

**Respuesta:**

```json
{
  "message": "Modelo entrenado exitosamente",
  "metrics": {
    "mae": 0.8456,
    "rmse": 1.2345,
    "r2_score": 0.9234,
    "best_params": {
      "n_estimators": 200,
      "max_depth": 20,
      "min_samples_split": 2
    }
  }
}
```

### 4. Información del Modelo

```http
GET /api/model-info
```

**Respuesta:**

```json
{
  "trained": true,
  "info": {
    "algorithm": "Random Forest Regressor",
    "n_features": 9,
    "feature_names": [...],
    "metrics": {...}
  }
}
```

## 🧠 Modelo de Machine Learning

### Pipeline de Procesamiento

1. **Limpieza de datos:**
   - Eliminación de duplicados
   - Remoción de outliers (kilometraje > 400,000 km, precio > 80)

2. **Preprocesamiento:**
   - Estandarización de variables numéricas (StandardScaler)
   - One-Hot Encoding para variables categóricas

3. **Entrenamiento:**
   - Algoritmo: Random Forest Regressor
   - Optimización de hiperparámetros con GridSearchCV
   - Cross-validation con 5 folds
   - División 80/20 (entrenamiento/prueba)

4. **Métricas de evaluación:**
   - MAE (Mean Absolute Error)
   - RMSE (Root Mean Squared Error)
   - R² Score

### Características del Modelo

El modelo utiliza las siguientes características:

- **Numéricas (estandarizadas):**
  - Year (Año)
  - Present_Price (Precio actual)
  - Kms_Driven (Kilometraje)
  - Owner (Número de dueños)

- **Categóricas (one-hot encoded):**
  - Fuel_Type (Petrol, Diesel, CNG)
  - Seller_Type (Dealer, Individual)
  - Transmission (Manual, Automatic)

## 📁 Estructura del Proyecto

```
backend/
├── app.py                          # Aplicación Flask principal
├── model.py                        # Clase del modelo de ML
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
├── data/                          # Datos de entrenamiento
│   └── car_prediction_data.csv
└── models/                        # Modelos entrenados
    ├── car_price_model.pkl
    └── scaler.pkl
```

## 🔒 Validaciones

El backend incluye las siguientes validaciones:

- Año entre 1990 y el año actual
- Precio mayor a 0
- Kilometraje no negativo
- Valores válidos para campos categóricos
- Verificación de campos requeridos
- Validación de tipos de datos

## 🌐 Integración con Frontend

El backend está configurado con CORS para aceptar peticiones desde el frontend Vue.js.

**URL del backend:** `http://localhost:5000`

## 🐛 Manejo de Errores

Todos los endpoints devuelven respuestas de error apropiadas:

- `400 Bad Request`: Datos inválidos o faltantes
- `500 Internal Server Error`: Error en el servidor
- `503 Service Unavailable`: Modelo no entrenado

Ejemplo de respuesta de error:

```json
{
  "error": "Falta el campo requerido: Year"
}
```

## 📊 Persistencia

- El modelo entrenado se guarda automáticamente en `models/`
- Se carga automáticamente al iniciar el servidor si existe
- El scaler también se persiste para mantener consistencia

## 🔄 Flujo de Trabajo

1. **Primera vez:** El servidor entrena el modelo automáticamente si encuentra `data/car_prediction_data.csv`
2. **Predicciones:** Una vez entrenado, el modelo está listo para recibir peticiones
3. **Re-entrenamiento:** Puedes enviar nuevos datos vía `/api/train` para actualizar el modelo

## 💡 Notas Técnicas

- El modelo se persiste usando `pickle`
- Se utiliza `StandardScaler` para normalización
- GridSearchCV optimiza automáticamente los hiperparámetros
- El rango de confianza se ajusta según el R² score del modelo

## 📝 Próximas Mejoras

- [ ] Agregar autenticación
- [ ] Implementar caché de predicciones
- [ ] Agregar logging avanzado
- [ ] Implementar versionado de modelos
- [ ] Agregar más algoritmos de ML
- [ ] Dashboard de monitoreo del modelo
