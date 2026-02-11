// Configuración del API Backend
// Las URLs se configuran en archivos .env.development y .env.production
// Vite carga automáticamente el archivo correcto según el modo

export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL,
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
