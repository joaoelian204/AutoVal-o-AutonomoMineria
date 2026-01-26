<template>
  <transition name="slide-fade">
    <div v-if="result" class="result-container">
      <div class="result-header">
        <div class="success-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <path
              d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              stroke="currentColor"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>
        <h3 class="result-title">✨ Valoración Calculada</h3>
      </div>

      <div class="result-content">
        <!-- Precio Principal -->
        <div class="main-price-card">
          <div class="price-icon">💰</div>
          <span class="price-label">PRECIO ESTIMADO</span>
          <div class="price-value">
            <span class="currency">$</span>
            <span class="amount">{{
              formatPrice(result.estimatedPrice * 1000)
            }}</span>
          </div>
          <span class="price-note">Valor de mercado actual</span>
        </div>

        <!-- Rango de Precio -->
        <div v-if="result.priceRange" class="price-range-card">
          <div class="range-header">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                stroke-width="2"
              />
            </svg>
            <span>Rango de Valor</span>
          </div>
          <div class="price-range">
            <div class="range-item min">
              <span class="range-label">📉 Mínimo</span>
              <span class="range-value"
                >${{ formatPrice(result.priceRange.min * 1000) }}</span
              >
            </div>
            <div class="range-separator">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
              >
                <path
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                  stroke-width="2"
                  stroke-linecap="round"
                />
              </svg>
            </div>
            <div class="range-item max">
              <span class="range-label">📈 Máximo</span>
              <span class="range-value"
                >${{ formatPrice(result.priceRange.max * 1000) }}</span
              >
            </div>
          </div>
        </div>

        <!-- Confianza -->
        <div v-if="result.confidence" class="confidence-card">
          <div class="confidence-header">
            <span class="confidence-label">🎯 Nivel de Confianza</span>
            <span class="confidence-percentage"
              >{{ result.confidence.toFixed(1) }}%</span
            >
          </div>
          <div class="confidence-bar">
            <div
              class="confidence-fill"
              :style="{ width: `${result.confidence}%` }"
              :class="getConfidenceClass(result.confidence)"
            ></div>
          </div>
          <span class="confidence-text">{{
            getConfidenceText(result.confidence)
          }}</span>
        </div>

        <!-- Detalles Adicionales -->
        <div v-if="result.details" class="details-grid">
          <div class="detail-item">
            <div class="detail-icon">📅</div>
            <div class="detail-content">
              <span class="detail-label">Edad del Vehículo</span>
              <span class="detail-value"
                >{{ result.details.vehicleAge }} años</span
              >
            </div>
          </div>
          <div class="detail-item">
            <div class="detail-icon">🔧</div>
            <div class="detail-content">
              <span class="detail-label">Depreciación</span>
              <span class="detail-value"
                >{{
                  (result.details.depreciationFactor * 100).toFixed(0)
                }}%</span
              >
            </div>
          </div>
          <div class="detail-item full-width">
            <div class="detail-icon">🚗</div>
            <div class="detail-content">
              <span class="detail-label">Estado por Kilometraje</span>
              <span class="detail-value">{{
                result.details.mileageCategory
              }}</span>
            </div>
          </div>
        </div>

        <!-- Mensaje -->
        <div v-if="result.message" class="result-message">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
          <p>{{ result.message }}</p>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
interface ValuationResult {
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

defineProps<{
  result: ValuationResult | null;
}>();

const formatPrice = (price: number): string => {
  return new Intl.NumberFormat("es-US", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(price);
};

const getConfidenceClass = (confidence: number): string => {
  if (confidence >= 85) return "high";
  if (confidence >= 70) return "medium";
  return "low";
};

const getConfidenceText = (confidence: number): string => {
  if (confidence >= 90) return "Excelente precisión";
  if (confidence >= 80) return "Buena precisión";
  if (confidence >= 70) return "Precisión moderada";
  return "Estimación aproximada";
};
</script>

<style scoped>
.result-container {
  margin-top: 2rem;
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.75rem;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
}

.success-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.success-icon svg {
  stroke: #10b981;
}

.result-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: white;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-content {
  padding: 1.75rem;
}

/* Tarjeta de Precio Principal */
.main-price-card {
  text-align: center;
  padding: 2rem 1.5rem;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border: 2px solid #bbf7d0;
  position: relative;
  overflow: hidden;
}

.main-price-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #10b981, #059669, #10b981);
}

.price-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.price-label {
  display: block;
  font-size: 0.75rem;
  color: #047857;
  font-weight: 700;
  margin-bottom: 0.75rem;
  letter-spacing: 1.5px;
}

.price-value {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0.25rem;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.currency {
  font-size: 1.75rem;
  font-weight: 700;
  color: #059669;
  margin-top: 0.25rem;
}

.amount {
  font-size: 3.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.price-note {
  display: block;
  font-size: 0.8rem;
  color: #065f46;
  font-weight: 500;
}

/* Tarjeta de Rango */
.price-range-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  border: 1px solid #e2e8f0;
}

.range-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: #475569;
  font-weight: 600;
  font-size: 0.9rem;
}

.range-header svg {
  stroke: #6366f1;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.range-item {
  flex: 1;
  text-align: center;
  padding: 1rem;
  border-radius: 8px;
  background: white;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.range-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.range-item.min {
  border-color: #fbbf24;
}

.range-item.max {
  border-color: #34d399;
}

.range-label {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.range-value {
  display: block;
  font-size: 1.35rem;
  font-weight: 800;
  color: #1e293b;
}

.range-separator {
  color: #cbd5e1;
  flex-shrink: 0;
}

/* Tarjeta de Confianza */
.confidence-card {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 12px;
  padding: 1.25rem;
  margin-bottom: 1.5rem;
  border: 2px solid #fbbf24;
}

.confidence-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.confidence-label {
  font-size: 0.9rem;
  color: #92400e;
  font-weight: 700;
}

.confidence-percentage {
  font-size: 1.25rem;
  font-weight: 800;
  color: #78350f;
}

.confidence-bar {
  height: 12px;
  background: #fef3c7;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
  border: 1px solid #fbbf24;
}

.confidence-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 1s ease-out;
}

.confidence-fill.high {
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.confidence-fill.medium {
  background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
}

.confidence-fill.low {
  background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%);
}

.confidence-text {
  display: block;
  text-align: center;
  font-size: 0.8rem;
  color: #92400e;
  font-weight: 600;
}

/* Detalles Grid */
.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
}

.detail-item:hover {
  border-color: #6366f1;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.detail-icon {
  font-size: 1.75rem;
  flex-shrink: 0;
}

.detail-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 600;
}

.detail-value {
  font-size: 1rem;
  color: #1e293b;
  font-weight: 700;
}

/* Mensaje */
.result-message {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: #dbeafe;
  border-left: 4px solid #3b82f6;
  border-radius: 8px;
}

.result-message svg {
  flex-shrink: 0;
  stroke: #2563eb;
  margin-top: 0.125rem;
}

.result-message p {
  margin: 0;
  font-size: 0.9rem;
  color: #1e40af;
  line-height: 1.6;
  font-weight: 500;
}

/* Animaciones */
.slide-fade-enter-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 1, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-15px) scale(0.98);
}

/* Responsive */
@media (max-width: 640px) {
  .result-content {
    padding: 1.25rem;
  }

  .amount {
    font-size: 2.75rem;
  }

  .currency {
    font-size: 1.5rem;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }

  .detail-item.full-width {
    grid-column: 1;
  }

  .price-range {
    flex-direction: column;
  }

  .range-separator {
    transform: rotate(90deg);
  }
}
</style>
