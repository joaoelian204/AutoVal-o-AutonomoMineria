// Servicio para comunicación con el API Backend
import { API_CONFIG, getApiUrl } from "../config/api";

export interface CarDataSubmit {
  Year: number;
  Present_Price: number;
  Kms_Driven: number;
  Fuel_Type: string;
  Seller_Type: string;
  Transmission: string;
  Owner: number;
}

export interface ValuationResult {
  estimatedPrice: number;
  priceRange?: {
    min: number;
    max: number;
  };
  confidence?: number;
  message?: string;
  details?: {
    vehicleAge: number;
    depreciationFactor: number;
    mileageCategory: string;
  };
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiService {
  /**
   * Verificar estado del servidor
   */
  async checkHealth(): Promise<
    ApiResponse<{ status: string; model_trained: boolean }>
  > {
    try {
      const response = await fetch(getApiUrl("HEALTH"), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return {
        error:
          error instanceof Error
            ? error.message
            : "Error al conectar con el servidor",
      };
    }
  }

  /**
   * Predecir precio del vehículo
   */
  async predictPrice(
    carData: CarDataSubmit,
  ): Promise<ApiResponse<ValuationResult>> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(
        () => controller.abort(),
        API_CONFIG.TIMEOUT,
      );

      const response = await fetch(getApiUrl("PREDICT"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(carData),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      if (error instanceof Error) {
        if (error.name === "AbortError") {
          return {
            error:
              "La solicitud ha excedido el tiempo límite. Intenta nuevamente.",
          };
        }
        return { error: error.message };
      }
      return { error: "Error desconocido al procesar la solicitud" };
    }
  }

  /**
   * Obtener información del modelo
   */
  async getModelInfo(): Promise<ApiResponse<any>> {
    try {
      const response = await fetch(getApiUrl("MODEL_INFO"), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      return {
        error:
          error instanceof Error
            ? error.message
            : "Error al obtener información del modelo",
      };
    }
  }
}

// Exportar instancia singleton
export const apiService = new ApiService();
