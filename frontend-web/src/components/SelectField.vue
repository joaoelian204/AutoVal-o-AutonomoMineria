<template>
  <div class="select-field">
    <label :for="id" class="select-label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>
    <div class="select-wrapper">
      <select
        :id="id"
        :value="modelValue"
        @change="
          $emit('update:modelValue', ($event.target as HTMLSelectElement).value)
        "
        :required="required"
        class="select-control"
      >
        <option value="" disabled>{{ placeholder }}</option>
        <option
          v-for="option in options"
          :key="option.value"
          :value="option.value"
        >
          {{ option.label }}
        </option>
      </select>
      <div class="select-arrow">
        <svg width="12" height="8" viewBox="0 0 12 8" fill="none">
          <path
            d="M1 1.5L6 6.5L11 1.5"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>
    </div>
    <span v-if="error" class="error-message">{{ error }}</span>
  </div>
</template>

<script setup lang="ts">
export interface SelectOption {
  value: string | number;
  label: string;
}

defineProps<{
  id: string;
  label: string;
  modelValue: string | number;
  options: SelectOption[];
  placeholder?: string;
  required?: boolean;
  error?: string;
}>();

defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();
</script>

<style scoped>
.select-field {
  margin-bottom: 1rem;
  width: 100%;
}

.select-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.4rem;
}

.required {
  color: #e74c3c;
  margin-left: 0.25rem;
}

.select-wrapper {
  position: relative;
  width: 100%;
}

.select-control {
  width: 100%;
  padding: 0.65rem 2.5rem 0.65rem 0.875rem;
  font-size: 0.95rem;
  border: 2px solid #e0e6ed;
  border-radius: 6px;
  background-color: #ffffff;
  color: #2c3e50;
  cursor: pointer;
  appearance: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.select-control:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.select-control:hover {
  border-color: #cbd5e0;
}

.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  color: #2c3e50;
}

.error-message {
  display: block;
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}
</style>
