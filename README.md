# Sistema de Valoración de Vehículos Usados

Sistema completo con Machine Learning para predecir precios de vehículos usados.

## 🚀 Stack Tecnológico

- **Backend:** Python + Flask + Scikit-learn (Machine Learning)
- **Frontend:** Vue 3 + TypeScript + Vite
- **ML:** Random Forest Regressor con optimización de hiperparámetros

## ⚡ Inicio Rápido

### 1. Instalar dependencias

**Frontend:**

```bash
npm run install:all
```

**Backend:**

```bash
npm run install:backend
```

O manualmente:

```bash
cd backend
pip install -r requirements.txt
```

### 2. Preparar datos

Coloca el archivo `car_prediction_data.csv` en `backend/data/`

### 3. Ejecutar el sistema

**Opción A - Todo desde la raíz:**

```bash
# Backend (Terminal 1)
npm run dev:backend

# Frontend (Terminal 2)
npm run dev:frontend
```

**Opción B - Manualmente:**

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend-web
npm run dev
```

### 4. Acceder a la aplicación

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health

## 📁 Estructura del Proyecto

```
AutonomoMineria/
├── backend/                    # Backend Flask + ML
│   ├── app.py                 # Servidor Flask
│   ├── model.py              # Modelo Machine Learning
│   ├── requirements.txt      # Dependencias Python
│   ├── data/                 # Datos de entrenamiento
│   │   └── car_prediction_data.csv
│   └── models/               # Modelos entrenados (generados)
│       ├── car_price_model.pkl
│       └── scaler.pkl
│
├── frontend-web/              # Frontend Vue
│   ├── src/
│   │   ├── components/       # Componentes Vue
│   │   ├── config/          # Configuración API
│   │   └── services/        # Servicios API
│   ├── package.json
│   └── vite.config.ts
│
└── package.json              # Scripts raíz
```

## 🔌 Endpoints API

### GET /api/health

Verificar estado del servidor

```bash
curl http://localhost:5000/api/health
```

### POST /api/predict

Predecir precio de vehículo

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Year": 2015,
    "Present_Price": 9.85,
    "Kms_Driven": 6900,
    "Fuel_Type": "Petrol",
    "Seller_Type": "Dealer",
    "Transmission": "Manual",
    "Owner": 0
  }'
```

### GET /api/model-info

Obtener información del modelo

```bash
curl http://localhost:5000/api/model-info
```

## 📊 Resultados del Modelo

- **R² Score:** 0.8732 (87.32% de precisión)
- **MAE:** 0.8841
- **RMSE:** 1.9593
- **Algoritmo:** Random Forest Regressor
- **Optimización:** GridSearchCV con 5-fold cross-validation

## 🛠️ Scripts Disponibles

Desde la raíz del proyecto:

| Script                    | Descripción                        |
| ------------------------- | ---------------------------------- |
| `npm run install:all`     | Instalar dependencias del frontend |
| `npm run install:backend` | Instalar dependencias del backend  |
| `npm run dev:backend`     | Iniciar servidor backend           |
| `npm run dev:frontend`    | Iniciar servidor frontend          |
| `npm run build:frontend`  | Build del frontend para producción |

## 🔧 Configuración

### Backend (Python)

- Puerto: 5000
- CORS: Habilitado
- Auto-entrenamiento: Si existe `data/car_prediction_data.csv`

### Frontend (Vue)

- Puerto: 5173
- Proxy API: Configurado en `vite.config.ts`
- Variables de entorno: `.env.development`

## 📝 Flujo de Trabajo

1. **Usuario ingresa datos** del vehículo en el formulario
2. **Frontend valida** los datos localmente
3. **Frontend envía** petición POST a `/api/predict`
4. **Backend procesa** con modelo ML entrenado
5. **Backend responde** con precio estimado + confianza
6. **Frontend muestra** resultados con visualización

## 🎯 Características del Sistema

### Backend

- ✅ API RESTful con Flask
- ✅ Modelo ML persistente
- ✅ Preprocesamiento automático
- ✅ Validaciones robustas
- ✅ Manejo de errores

### Frontend

- ✅ Interfaz moderna y responsive
- ✅ Validación en tiempo real
- ✅ TypeScript para type safety
- ✅ Integración con API
- ✅ Diseño adaptativo

## 🚨 Troubleshooting

### Backend no inicia

```bash
# Verificar Python
python --version

# Reinstalar dependencias
cd backend
pip install -r requirements.txt
```

### Frontend no inicia

```bash
# Verificar Node
node --version

# Reinstalar dependencias
cd frontend-web
npm install
```

### Error de conexión

1. Verifica que el backend esté corriendo en puerto 5000
2. Verifica que el frontend esté en puerto 5173
3. Revisa los logs en ambas consolas

## 📚 Documentación Adicional

- [Backend README](backend/README.md)
- [Frontend CONEXION](frontend-web/CONEXION.md)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch
3. Commit tus cambios
4. Push al branch
5. Abre un Pull Request

## 📄 Licencia

MIT

---

**¡Hecho con ❤️ y Machine Learning!** 🚗💨
