<template>
  <div class="panel-section">
    <label>{{ label }}</label>
    <div class="upload-area" @click="$refs.fileInput.click()" @drop.prevent="onDrop" @dragover.prevent>
      <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display:none">
      <div v-if="!modelValue" class="upload-placeholder">
        <AppIcon name="upload" size="36" />
        <p>{{ placeholder }}</p>
      </div>
      <div v-else class="uploaded-preview">
        <img :src="modelValue">
        <button class="remove-btn" @click.stop="clear">
          <AppIcon name="close" size="14" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import AppIcon from './AppIcon.vue'

export default {
  name: 'ImageUpload',
  components: { AppIcon },
  props: {
    modelValue: { type: String, default: null },
    label: { type: String, default: '上传图像' },
    placeholder: { type: String, default: '点击或拖拽上传' }
  },
  emits: ['update:modelValue'],
  methods: {
    readFile(file) {
      if (!file || !file.type.startsWith('image/')) return
      const reader = new FileReader()
      reader.onload = (e) => this.$emit('update:modelValue', e.target.result)
      reader.readAsDataURL(file)
    },
    onFileChange(e) { this.readFile(e.target.files[0]) },
    onDrop(e) { this.readFile(e.dataTransfer.files[0]) },
    clear() { this.$emit('update:modelValue', null) }
  }
}
</script>

<style scoped>
.panel-section { display: flex; flex-direction: column; gap: 6px; }
label { font-weight: 600; font-size: 13px; color: var(--text-primary); }

.upload-area {
  border: 2px dashed var(--border);
  border-radius: var(--radius);
  padding: 32px;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition);
  min-height: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-secondary);
}

.upload-area:hover {
  border-color: var(--accent);
  background: var(--accent-light);
}

.upload-placeholder {
  color: var(--text-muted);
}

.upload-placeholder p {
  color: var(--text-muted);
  margin: 10px 0 0;
  font-size: 13px;
}

.uploaded-preview {
  position: relative;
  width: 100%;
}

.uploaded-preview img {
  width: 100%;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  background: var(--danger);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: background var(--transition);
}

.remove-btn:hover { background: #dc2626; }
</style>
