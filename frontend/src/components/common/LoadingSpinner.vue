<template>
  <div class="generating-state">
    <div class="generating-spinner">
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
    </div>
    <p>{{ text }}</p>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    text: { type: String, default: 'AI创作中...' }
  }
}
</script>

<style scoped>
.generating-state {
  text-align: center;
  padding: 80px 20px;
}

.generating-spinner {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  position: relative;
}

.spinner-ring {
  position: absolute;
  inset: 0;
  border: 3px solid transparent;
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner-ring:nth-child(2) {
  inset: 7px;
  border-top-color: #6366f1;
  animation-delay: -0.35s;
}

.spinner-ring:nth-child(3) {
  inset: 14px;
  border-top-color: #818cf8;
  animation-delay: -0.7s;
}

@keyframes spin { to { transform: rotate(360deg); } }

p {
  color: var(--text-muted);
  font-size: 14px;
}
</style>
