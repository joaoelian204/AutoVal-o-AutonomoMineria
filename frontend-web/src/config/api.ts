// Configuración del API Backend
// En producción (Docker), las peticiones van al mismo origen y nginx las redirige
// En desarrollo, apuntan a localhost:5000
const isProduction = import.meta.env.PROD;

export const API_CONFIG = {
  BASE_URL: isProduction
    ? ""
    : import.meta.env.VITE_API_BASE_URL || "http://localhost:5000",
  ENDPOINTS: {
    HEALTH: "/api/health",
    PREDICT: "/api/predict",
    TRAIN: "/api/train",
    MODEL_INFO: "/api/model-info",
    DEPRECIATION: "/api/depreciation-curve",
  },
  TIMEOUT: 30000, // 30 segundos
};

// Helper para construir URLs completas
export const getApiUrl = (
  endpoint: keyof typeof API_CONFIG.ENDPOINTS,
): string => {
  return `${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS[endpoint]}`;
};
