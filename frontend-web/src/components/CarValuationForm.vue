<template>
  <div class="main-card">
    <div class="card-grid">
      <!-- Formulario -->
      <div class="form-section">
        <h3><Car class="icon-title" /> Valoración de Vehículo</h3>
        <form @submit.prevent="handleSubmit">
          <div class="grid-2">
            <div class="field">
              <label>Año</label>
              <input
                type="number"
                v-model="formData.Year"
                placeholder="2015"
                :min="1990"
                :max="currentYear"
                required
              />
            </div>
            <div class="field">
              <label>Precio de Lista ($)</label>
              <input
                type="number"
                v-model="formData.Present_Price"
                placeholder="15000"
                step="1"
                min="1000"
                max="500000"
                required
              />
              <small class="hint">Precio cuando era nuevo (ej: 15000)</small>
            </div>
          </div>
          <div class="field">
            <label>Kilometraje</label>
            <input
              type="number"
              v-model="formData.Kms_Driven"
              placeholder="6900"
              required
            />
          </div>
          <div class="grid-2">
            <div class="field">
              <label>Combustible</label>
              <select v-model="formData.Fuel_Type" required>
                <option value="">Selecciona</option>
                <option value="Petrol">Gasolina</option>
                <option value="Diesel">Diésel</option>
                <option value="CNG">Gas Natural</option>
              </select>
            </div>
            <div class="field">
              <label>Transmisión</label>
              <select v-model="formData.Transmission" required>
                <option value="">Selecciona</option>
                <option value="Manual">Manual</option>
                <option value="Automatic">Automática</option>
              </select>
            </div>
          </div>
          <div class="grid-2">
            <div class="field">
              <label>Vendedor</label>
              <select v-model="formData.Seller_Type" required>
                <option value="">Selecciona</option>
                <option value="Dealer">Concesionario</option>
                <option value="Individual">Particular</option>
              </select>
            </div>
            <div class="field">
              <label>Dueños Previos</label>
              <select v-model="formData.Owner" required>
                <option value="">Selecciona</option>
                <option :value="0">Ninguno</option>
                <option :value="1">Uno</option>
                <option :value="2">Dos</option>
                <option :value="3">Tres o más</option>
              </select>
            </div>
          </div>
          <button type="submit" class="btn-calc" :disabled="isLoading">
            <Loader2 v-if="isLoading" class="icon-spin" />
            <Calculator v-else class="icon-btn" />
            {{ isLoading ? "Calculando..." : "Calcular Precio" }}
          </button>
        </form>
      </div>

      <!-- Resultado -->
      <div class="result-section">
        <div v-if="result" class="result-box">
          <div class="price-tag">
            <span class="label">Precio Estimado</span>
            <span class="price">${{ formatPrice(result.estimatedPrice) }}</span>
          </div>
          <div class="range" v-if="result.priceRange">
            <span
              ><TrendingDown class="icon-range" /> ${{
                formatPrice(result.priceRange.min)
              }}</span
            >
            <div class="range-bar"></div>
            <span
              ><TrendingUp class="icon-range" /> ${{
                formatPrice(result.priceRange.max)
              }}</span
            >
          </div>
          <div class="confidence" v-if="result.confidence">
            <div
              class="conf-bar"
              :style="{ width: result.confidence + '%' }"
            ></div>
            <span>{{ result.confidence.toFixed(0) }}% confianza</span>
          </div>
          <div class="details">
            <div><strong>Año:</strong> {{ formData.Year }}</div>
            <div>
              <strong>Km:</strong>
              {{ Number(formData.Kms_Driven).toLocaleString() }}
            </div>
            <div>
              <strong>Tipo:</strong> {{ translateFuel(formData.Fuel_Type) }} /
              {{ translateTransmission(formData.Transmission) }}
            </div>
          </div>
        </div>
        <div v-else class="empty-box">
          <BarChart3 class="empty-icon" />
          <p>Completa el formulario para ver la valoración</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  BarChart3,
  Calculator,
  Car,
  Loader2,
  TrendingDown,
  TrendingUp,
} from "lucide-vue-next";
import { reactive, ref } from "vue";
import {
  apiService,
  type CarDataSubmit,
  type ValuationResult,
} from "../services/api.service";

interface CarData {
  Year: string;
  Present_Price: string;
  Kms_Driven: string;
  Fuel_Type: string;
  Seller_Type: string;
  Transmission: string;
  Owner: string;
}

const currentYear = new Date().getFullYear();
const isLoading = ref(false);
const result = ref<ValuationResult | null>(null);

const formData = reactive<CarData>({
  Year: "",
  Present_Price: "",
  Kms_Driven: "",
  Fuel_Type: "",
  Seller_Type: "",
  Transmission: "",
  Owner: "",
});

const formatPrice = (price: number): string => {
  return (price * 1000).toLocaleString("en-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });
};

const translateFuel = (fuel: string): string => {
  const map: Record<string, string> = {
    Petrol: "Gasolina",
    Diesel: "Diésel",
    CNG: "Gas Natural",
  };
  return map[fuel] || fuel;
};

const translateTransmission = (trans: string): string => {
  const map: Record<string, string> = {
    Manual: "Manual",
    Automatic: "Automática",
  };
  return map[trans] || trans;
};

const handleSubmit = async () => {
  isLoading.value = true;
  try {
    // El modelo espera Present_Price en miles (ej: 15 para $15,000)
    // El usuario ingresa el valor completo (ej: 15000), lo dividimos entre 1000
    const dataToSend: CarDataSubmit = {
      Year: parseInt(formData.Year),
      Present_Price: parseFloat(formData.Present_Price) / 1000,
      Kms_Driven: parseInt(formData.Kms_Driven),
      Fuel_Type: formData.Fuel_Type,
      Seller_Type: formData.Seller_Type,
      Transmission: formData.Transmission,
      Owner: parseInt(formData.Owner),
    };
    const response = await apiService.predictPrice(dataToSend);
    if (response.error) throw new Error(response.error);
    if (response.data) result.value = response.data;
  } catch (error) {
    console.error("Error:", error);
    alert("Error al calcular. Verifica los datos.");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Estilos de iconos */
.icon-title {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin-right: 6px;
  color: #6366f1;
}

.icon-btn {
  width: 18px;
  height: 18px;
  margin-right: 6px;
}

.icon-spin {
  width: 18px;
  height: 18px;
  margin-right: 6px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.icon-range {
  width: 14px;
  height: 14px;
  vertical-align: middle;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.main-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  max-width: 800px;
  width: 100%;
}

.card-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-section h3 {
  margin: 0 0 12px 0;
  font-size: 1.1rem;
  color: #1e293b;
  display: flex;
  align-items: center;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.field {
  margin-bottom: 8px;
}

.field .hint {
  display: block;
  font-size: 0.65rem;
  color: #94a3b8;
  margin-top: 2px;
}

.field label {
  display: block;
  font-size: 0.7rem;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 3px;
  text-transform: uppercase;
}

.field input,
.field select {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.85rem;
  background: #f8fafc;
  transition: all 0.2s;
  box-sizing: border-box;
}

.field input:focus,
.field select:focus {
  outline: none;
  border-color: #6366f1;
  background: white;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.btn-calc {
  width: 100%;
  padding: 10px;
  margin-top: 8px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-calc:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.btn-calc:disabled {
  opacity: 0.7;
  cursor: wait;
}

/* Resultado */
.result-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.result-box {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 12px;
  color: white;
}

.price-tag {
  text-align: center;
  margin-bottom: 12px;
}

.price-tag .label {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  opacity: 0.9;
}

.price-tag .price {
  display: block;
  font-size: 2rem;
  font-weight: 700;
}

.range {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.75rem;
  margin-bottom: 10px;
  opacity: 0.9;
}

.range-bar {
  flex: 1;
  height: 3px;
  background: rgba(255, 255, 255, 0.3);
  margin: 0 8px;
  border-radius: 2px;
}

.confidence {
  position: relative;
  height: 20px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  margin-bottom: 10px;
  overflow: hidden;
}

.conf-bar {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 10px;
  transition: width 0.5s;
}

.confidence span {
  position: relative;
  z-index: 1;
  display: block;
  text-align: center;
  font-size: 0.7rem;
  line-height: 20px;
  font-weight: 600;
}

.details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4px;
  font-size: 0.7rem;
  background: rgba(0, 0, 0, 0.1);
  padding: 8px;
  border-radius: 6px;
}

.details div:last-child {
  grid-column: span 2;
}

/* Estado vacío */
.empty-box {
  text-align: center;
  padding: 30px 15px;
  color: #94a3b8;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-box p {
  margin: 0;
  font-size: 0.8rem;
}

@media (max-width: 700px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
