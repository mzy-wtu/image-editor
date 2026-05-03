<template>
  <div class="params-panel">
    <div class="panel-section">
      <label>提示词</label>
      <textarea v-model="form.prompt" class="input-field" placeholder="描述你想要生成的图像..." rows="6"></textarea>
      <div class="prompt-actions">
        <button class="btn-sm" @click="showTemplates = true">
          <AppIcon name="template" size="14" />模板
        </button>
        <button class="btn-sm" @click="enhancePrompt">
          <AppIcon name="star" size="14" />增强
        </button>
      </div>
    </div>

    <div class="panel-section">
      <label>负面提示词</label>
      <textarea v-model="form.negativePrompt" class="input-field" placeholder="不想要的元素..." rows="2"></textarea>
    </div>

    <div class="panel-section">
      <label>模型选择</label>
      <div class="api-selector">
        <label v-for="api in apiOptions" :key="api.value" class="radio-card" :class="{ active: form.apiChoice === api.value }">
          <input type="radio" :value="api.value" v-model="form.apiChoice">
          <span class="api-dot" :style="{ background: api.color }"></span>
          <span class="api-label">{{ api.label }}</span>
        </label>
      </div>
    </div>

    <div class="panel-section">
      <label>图像尺寸</label>
      <select v-model="form.size" class="input-field">
        <option value="1024*1024">正方形 1024×1024</option>
        <option value="1024*1536">竖版 1024×1536</option>
        <option value="1536*1024">横版 1536×1024</option>
      </select>
    </div>

    <div class="panel-section">
      <label>生成数量: {{ form.count }}</label>
      <div class="range-wrapper">
        <input type="range" v-model.number="form.count" min="1" max="4">
        <div class="range-dots">
          <span v-for="i in 4" :key="i" :class="{ active: i <= form.count }">{{ i }}</span>
        </div>
      </div>
    </div>

    <button class="btn-primary generate-btn" @click="$emit('generate', form)" :disabled="loading || !form.prompt">
      <AppIcon v-if="!loading" name="generate" size="18" />
      <span v-if="loading" class="loading-spinner"></span>
      {{ loading ? '生成中...' : '开始生成' }}
    </button>

    <div v-if="showTemplates" class="modal-overlay" @click="showTemplates = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>提示词模板</h3>
          <button class="modal-close" @click="showTemplates = false">
            <AppIcon name="close" size="20" />
          </button>
        </div>
        <div v-for="t in promptTemplates" :key="t.id" class="template-card" @click="useTemplate(t)">
          <h4>{{ t.title }}</h4>
          <p>{{ t.prompt }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppIcon from '../common/AppIcon.vue'

export default {
  name: 'GeneratePanel',
  components: { AppIcon },
  props: {
    loading: { type: Boolean, default: false }
  },
  emits: ['generate'],
  data() {
    return {
      showTemplates: false,
      form: {
        prompt: '', negativePrompt: '', apiChoice: 'API-1',
        size: '1024*1536', count: 1, seed: null
      },
      apiOptions: [
        { value: 'API-1', label: '千问', color: '#c98d5f' },
        { value: 'API-2', label: '通义', color: '#0891b2' },
        { value: 'API-3', label: '模拟', color: '#6b7280' },
        { value: 'API-4', label: '万象Pro', color: '#a0522d' }
      ],
      promptTemplates: [
        { id: 1, title: '写实风格', prompt: '超高清，写实风格，细节丰富，专业摄影' },
        { id: 2, title: '动漫风格', prompt: '动漫风格，精美插画，色彩鲜艳，高质量' },
        { id: 3, title: '水彩画', prompt: '水彩画风格，柔和色调，艺术感强' },
        { id: 4, title: '赛博朋克', prompt: '赛博朋克风格，霓虹灯，未来科技感，夜景' }
      ]
    }
  },
  methods: {
    enhancePrompt() {
      if (this.form.prompt) { this.form.prompt += ', 高质量, 精美细节, 专业级' }
    },
    useTemplate(t) {
      this.form.prompt = t.prompt
      this.showTemplates = false
    }
  }
}
</script>

<style scoped>
.params-panel { display: flex; flex-direction: column; gap: 18px; }
.panel-section { display: flex; flex-direction: column; gap: 6px; }
.panel-section label { font-weight: 600; font-size: 13px; color: var(--text-primary); }
.prompt-actions { display: flex; gap: 8px; }
.api-selector { display: flex; gap: 8px; }

.radio-card {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 8px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition);
}

.radio-card:hover {
  border-color: var(--accent);
  background: var(--accent-light);
}

.radio-card.active {
  background: var(--accent-light);
  border-color: var(--accent);
}

.radio-card input { display: none; }

.api-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.api-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.range-wrapper { padding: 0 4px; }

.range-dots {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}

.range-dots span {
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tertiary);
  border-radius: 50%;
  font-size: 11px;
  color: var(--text-muted);
  transition: all var(--transition);
}

.range-dots span.active {
  background: var(--accent);
  color: white;
}

.generate-btn { margin-top: 2px; }

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
  color: var(--text-primary);
  font-size: 18px;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 4px;
}

.modal-close:hover { color: var(--text-primary); }

.template-card {
  padding: 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  margin-bottom: 10px;
  cursor: pointer;
  transition: all var(--transition);
}

.template-card:hover {
  background: var(--accent-light);
  border-color: var(--accent);
}

.template-card h4 {
  color: var(--text-primary);
  margin: 0 0 4px;
  font-size: 14px;
}

.template-card p {
  color: var(--text-muted);
  font-size: 13px;
  margin: 0;
}
</style>
