<template>
  <div class="empty-state">
    <div class="empty-icon">
      <AppIcon :name="icon" size="48" />
    </div>
    <h3>{{ title }}</h3>
    <p>{{ description }}</p>
    <button v-if="actionText" @click="$emit('action')">{{ actionText }}</button>
  </div>
</template>

<script>
import AppIcon from './AppIcon.vue'

export default {
  name: 'EmptyState',
  components: { AppIcon },
  props: {
    icon: { type: String, default: 'image' },
    title: { type: String, default: '' },
    description: { type: String, default: '' },
    actionText: { type: String, default: '' }
  },
  emits: ['action']
}
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  width: 96px;
  height: 96px;
  margin: 0 auto 20px;
  background: var(--accent-light);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

h3 {
  font-size: 20px;
  color: var(--text-primary);
  margin: 0 0 8px;
  font-weight: 600;
}

p {
  color: var(--text-muted);
  margin: 0 0 20px;
  font-size: 14px;
}

button {
  padding: 10px 24px;
  background: var(--accent);
  border: none;
  border-radius: var(--radius);
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition);
}

button:hover {
  background: var(--accent-hover);
}
</style>
