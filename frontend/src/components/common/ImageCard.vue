<template>
  <div class="image-card" @click="$emit('preview', src)">
    <img :src="src" loading="lazy" />
    <div class="image-overlay">
      <button @click.stop="$emit('download', src, index)" title="下载">
        <AppIcon name="download" size="20" />
      </button>
      <button @click.stop="$emit('preview', src)" title="预览">
        <AppIcon name="search" size="20" />
      </button>
    </div>
  </div>
</template>

<script>
import AppIcon from './AppIcon.vue'

export default {
  name: 'ImageCard',
  components: { AppIcon },
  props: {
    src: { type: String, required: true },
    index: { type: Number, default: 0 }
  },
  emits: ['preview', 'download']
}
</script>

<style scoped>
.image-card {
  position: relative;
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: all var(--transition);
  border: 1px solid var(--border);
  aspect-ratio: 1;
  background: var(--bg-tertiary);
}

.image-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}

.image-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  padding: 16px;
  display: flex;
  gap: 10px;
  justify-content: center;
  opacity: 0;
  transition: opacity var(--transition);
}

.image-card:hover .image-overlay { opacity: 1; }

.image-overlay button {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
}

.image-overlay button:hover {
  transform: scale(1.08);
}
</style>
