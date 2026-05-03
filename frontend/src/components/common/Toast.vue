<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-container">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="['toast', `toast-${toast.type}`]"
      >
        <AppIcon :name="toast.type === 'error' ? 'alert' : 'check'" size="18" />
        <span>{{ toast.message }}</span>
        <button @click="remove(toast.id)">
          <AppIcon name="close" size="14" />
        </button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script>
import { ref } from 'vue'
import AppIcon from './AppIcon.vue'

const toasts = ref([])
let nextId = 0

export function useToast() {
  const show = (message, type = 'info', duration = 4000) => {
    const id = ++nextId
    toasts.value.push({ id, message, type })
    if (duration > 0) setTimeout(() => remove(id), duration)
  }
  return { show }
}

function remove(id) {
  const i = toasts.value.findIndex(t => t.id === id)
  if (i !== -1) toasts.value.splice(i, 1)
}

export default {
  name: 'Toast',
  components: { AppIcon },
  setup() {
    return { toasts, remove }
  }
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: var(--radius);
  min-width: 280px;
  max-width: 420px;
  box-shadow: var(--shadow-lg);
  pointer-events: auto;
  font-size: 14px;
  border: 1px solid;
}

.toast button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  margin-left: auto;
  opacity: 0.5;
  color: inherit;
}

.toast button:hover { opacity: 1; }

.toast-error {
  background: #fef2f2;
  color: #991b1b;
  border-color: #fecaca;
}

.toast-success {
  background: #f0fdf4;
  color: #166534;
  border-color: #bbf7d0;
}

.toast-info {
  background: #fdf6f0;
  color: #9a5c2e;
  border-color: #f5d5b8;
}

.toast-enter-active { transition: all 0.3s ease; }
.toast-leave-active { transition: all 0.2s ease; }
.toast-enter-from { opacity: 0; transform: translateX(30px); }
.toast-leave-to { opacity: 0; transform: translateX(30px); }
</style>
