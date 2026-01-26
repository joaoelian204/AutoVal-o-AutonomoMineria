<template>
  <div class="input-field">
    <label :for="id" class="input-label">
      {{ label }}
      <span v-if="required" class="required">*</span>
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      @input="
        $emit('update:modelValue', ($event.target as HTMLInputElement).value)
      "
      :placeholder="placeholder"
      :min="min"
      :max="max"
      :step="step"
      :required="required"
      class="input-control"
    />
    <span v-if="error" class="error-message">{{ error }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  id: string;
  label: string;
  modelValue: string | number;
  type?: string;
  placeholder?: string;
  min?: number;
  max?: number;
  step?: number;
  required?: boolean;
  error?: string;
}>();

defineEmits<{
  (e: "update:modelValue", value: string): void;
}>();
</script>

<style scoped>
.input-field {
  margin-bottom: 1rem;
  width: 100%;
}

.input-label {
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

.input-control {
  width: 100%;
  padding: 0.65rem 0.875rem;
  font-size: 0.95rem;
  border: 2px solid #e0e6ed;
  border-radius: 6px;
  background-color: #ffffff;
  color: #2c3e50;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.input-control:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.input-control:hover {
  border-color: #cbd5e0;
}

.error-message {
  display: block;
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}
</style>
