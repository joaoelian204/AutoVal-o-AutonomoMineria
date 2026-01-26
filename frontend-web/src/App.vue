<script setup lang="ts">
import { Car } from "lucide-vue-next";
import CarValuationForm from "./components/CarValuationForm.vue";
</script>

<template>
  <div class="app-wrapper">
    <nav class="navbar">
      <Car class="nav-icon" />
      <span>AutoValúo</span>
    </nav>

    <main class="app-container">
      <CarValuationForm />
    </main>

    <footer class="footer">Minería de Datos 2026</footer>
  </div>
</template>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #134e4a 100%);
  position: relative;
  overflow: hidden;
}

.app-wrapper::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background:
    radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 50%),
    radial-gradient(
      circle at 80% 20%,
      rgba(99, 102, 241, 0.15) 0%,
      transparent 40%
    );
  animation: float 20s ease-in-out infinite;
  pointer-events: none;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 10;
}

.navbar span {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
}

.nav-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
}

.app-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  position: relative;
  z-index: 1;
}

.footer {
  padding: 16px 24px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.85rem;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 10;
}

@keyframes float {
  0%,
  100% {
    transform: translate(0, 0) rotate(0deg);
  }
  50% {
    transform: translate(-2%, 2%) rotate(1deg);
  }
}
</style>
