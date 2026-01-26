# Frontend - Valoración de Vehículos Usados

Aplicación web desarrollada con Vue 3, TypeScript y Vite para la valoración de vehículos usados usando Machine Learning.

## 🚀 Características

- **Interfaz moderna** con Vue 3 Composition API
- **TypeScript** para tipado estático
- **Integración con API Backend** Flask + ML
- **Validación de formularios** en tiempo real
- **Diseño responsive** para móviles y desktop
- **Manejo de errores** robusto

## 📋 Requisitos

- Node.js 18+
- npm o yarn
- Backend corriendo en `http://localhost:5000`

## 🔧 Instalación

1. **Instalar dependencias:**

```bash
npm install
```

2. **Configurar variables de entorno:**

El archivo `.env.development` ya está configurado con:

```env
VITE_API_BASE_URL=http://localhost:5000
```

Para producción, edita `.env.production` con la URL de tu servidor.

3. **Iniciar servidor de desarrollo:**

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## 📦 Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye para producción
- `npm run preview` - Preview del build de producción

## 🔌 Conexión con Backend

### Arquitectura

```
Frontend (Vue + Vite)         Backend (Flask + ML)
     localhost:5173    <--->      localhost:5000
         │                              │
         ├─ UI/Forms                    ├─ API REST
         ├─ Validación                  ├─ Modelo ML
         └─ Display                     └─ Procesamiento
```

### Servicios API

El frontend se comunica con el backend mediante el servicio `api.service.ts`:

#### 1. Health Check

```typescript
await apiService.checkHealth();
```

#### 2. Predicción de Precio

```typescript
await apiService.predictPrice({
  Year: 2015,
  Present_Price: 9.85,
  Kms_Driven: 6900,
  Fuel_Type: "Petrol",
  Seller_Type: "Dealer",
  Transmission: "Manual",
  Owner: 0,
});
```

#### 3. Información del Modelo

```typescript
await apiService.getModelInfo();
```

### Configuración

La configuración de la API se encuentra en [src/config/api.ts](src/config/api.ts):

```typescript
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || "http://localhost:5000",
  ENDPOINTS: {
    HEALTH: "/api/health",
    PREDICT: "/api/predict",
    TRAIN: "/api/train",
    MODEL_INFO: "/api/model-info",
  },
  TIMEOUT: 30000,
};
```

### Proxy de Desarrollo

Vite está configurado con un proxy para evitar problemas de CORS:

```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
    },
  },
}
```

## 📁 Estructura del Proyecto

```
frontend-web/
├── src/
│   ├── components/          # Componentes Vue
│   │   ├── CarValuationForm.vue    # Formulario principal
│   │   ├── InputField.vue          # Campo de entrada
│   │   ├── SelectField.vue         # Campo selector
│   │   └── ResultDisplay.vue       # Resultados
│   ├── config/             # Configuración
│   │   └── api.ts         # Config API
│   ├── services/          # Servicios
│   │   └── api.service.ts # Servicio API
│   ├── App.vue           # Componente raíz
│   └── main.ts          # Entry point
├── .env.development     # Variables desarrollo
├── .env.production     # Variables producción
├── vite.config.ts     # Config Vite
└── package.json      # Dependencias

```

## 🎨 Componentes

### CarValuationForm

Componente principal que maneja:

- Formulario de entrada de datos
- Validación de campos
- Comunicación con API
- Visualización de resultados

### InputField

Campo de entrada reutilizable con:

- Validación en tiempo real
- Mensajes de error
- Soporte para diferentes tipos

### SelectField

Campo selector con:

- Opciones personalizables
- Validación
- Placeholder dinámico

### ResultDisplay

Muestra los resultados con:

- Precio estimado
- Rango de confianza
- Detalles del vehículo
- Indicadores visuales

## 🔒 Validaciones Frontend

- **Año:** Entre 1990 y año actual
- **Precio:** Mayor a 0
- **Kilometraje:** No negativo
- **Campos categóricos:** Valores predefinidos
- **Campos requeridos:** Todos los campos son obligatorios

## 🚀 Deployment

### Build para Producción

```bash
npm run build
```

Los archivos generados estarán en `dist/`

### Configuración de Producción

1. Actualiza `.env.production` con la URL del backend en producción
2. Ejecuta el build
3. Despliega la carpeta `dist/` en tu servidor

### Opciones de Hosting

- **Vercel:** `vercel deploy`
- **Netlify:** `netlify deploy`
- **GitHub Pages:** Configurar con GitHub Actions
- **Servidor propio:** Servir carpeta `dist/` con nginx/apache

## 🐛 Troubleshooting

### Error de conexión con backend

1. Verifica que el backend esté corriendo:

   ```bash
   curl http://localhost:5000/api/health
   ```

2. Verifica las variables de entorno en `.env.development`

3. Revisa la consola del navegador para errores CORS

### Problemas de CORS

El backend ya tiene CORS habilitado. Si persisten problemas:

- Verifica que el proxy de Vite esté configurado
- Asegúrate de usar la URL correcta

### Puerto ocupado

Si el puerto 5173 está ocupado:

```bash
npm run dev -- --port 3000
```

## 🔄 Flujo de Trabajo Completo

1. **Inicio:**
   - Usuario abre el frontend
   - Frontend verifica conexión con backend (`/api/health`)

2. **Entrada de datos:**
   - Usuario completa el formulario
   - Validación en tiempo real

3. **Predicción:**
   - Frontend envía datos a `/api/predict`
   - Backend procesa con modelo ML
   - Frontend recibe y muestra resultados

4. **Visualización:**
   - Precio estimado con rango
   - Nivel de confianza
   - Detalles adicionales

## 💡 Próximas Mejoras

- [ ] Agregar gráficos de tendencias
- [ ] Histórico de búsquedas
- [ ] Comparador de vehículos
- [ ] Exportar resultados PDF
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)
- [ ] Tests unitarios
- [ ] Tests E2E

## 📝 Notas de Desarrollo

- El frontend usa Vue 3 Composition API
- TypeScript para type safety
- Vite para desarrollo rápido
- CSS Scoped para estilos encapsulados
- Fetch API nativa (sin axios)

## 🤝 Integración Backend

Asegúrate de que el backend esté corriendo antes de iniciar el frontend:

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend-web
npm run dev
```

## 📞 Soporte

Si tienes problemas:

1. Verifica que backend y frontend estén en los puertos correctos
2. Revisa las variables de entorno
3. Consulta los logs en la consola del navegador
4. Verifica los logs del backend

---

**Happy Coding! 🚗💨**
