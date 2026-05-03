<template>
  <div class="params-panel">
    <div class="edit-sub-tabs">
      <button v-for="tab in subTabs" :key="tab.key"
        :class="['sub-tab-btn', { active: currentTab === tab.key }]"
        @click="$emit('update:subTab', tab.key)">{{ tab.label }}</button>
    </div>

    <ImageUpload
      v-if="currentTab !== 'sketch'"
      v-model="uploadedImage"
      :label="currentTab === 'background' ? '上传透明背景PNG' : '上传图像'"
    />

    <!-- Instruct -->
    <template v-if="currentTab === 'instruct'">
      <div class="panel-section">
        <label>编辑指令</label>
        <textarea v-model="form.prompt" class="input-field" placeholder="描述编辑效果..." rows="4"></textarea>
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
      <button class="btn-primary" @click="$emit('edit', { type: 'instruct', image: uploadedImage, ...form })" :disabled="loading || !uploadedImage">
        <AppIcon v-if="!loading" name="edit" size="18" />
        <span v-if="loading" class="loading-spinner"></span>
        {{ loading ? '处理中...' : '开始编辑' }}
      </button>
    </template>

    <!-- Inpaint -->
    <template v-else-if="currentTab === 'inpaint'">
      <div class="panel-section">
        <label>在原图上涂抹要重绘的区域</label>
        <div class="sketch-canvas-wrap" v-if="uploadedImage">
          <img :src="uploadedImage" class="inpaint-bg-img" />
          <canvas ref="canvas" :width="canvasSize.w" :height="canvasSize.h"
            class="inpaint-canvas"
            @mousedown="startDraw" @mousemove="draw" @mouseup="endDraw" @mouseleave="endDraw"></canvas>
          <button class="sketch-clear-btn" @click="clearCanvas">清除</button>
        </div>
      </div>
      <div class="panel-section">
        <label>重绘内容描述</label>
        <textarea v-model="inpaintPrompt" class="input-field" placeholder="例如：一只戴红色眼镜的猫..." rows="3"></textarea>
      </div>
      <div class="panel-tip">
        <AppIcon name="info" size="14" />
        先上传原图，再在图上涂抹要修改的区域
      </div>
      <button class="btn-primary" @click="submitInpaint" :disabled="loading || !uploadedImage">
        <span v-if="loading" class="loading-spinner"></span>
        <AppIcon v-else name="image" size="18" />
        {{ loading ? '重绘中...' : '开始局部重绘' }}
      </button>
    </template>

    <!-- Background -->
    <template v-else-if="currentTab === 'background'">
      <div class="panel-section">
        <label>背景描述</label>
        <textarea v-model="form.prompt" class="input-field" placeholder="描述想要的背景..." rows="4"></textarea>
      </div>
      <div class="panel-tip">
        <AppIcon name="info" size="14" />
        AI 自动识别主体，生成全新背景（请上传已抠图的透明背景PNG）
      </div>
      <button class="btn-primary" @click="$emit('edit', { type: 'background', image: uploadedImage, prompt: form.prompt })" :disabled="loading || !uploadedImage">
        <span v-if="loading" class="loading-spinner"></span>
        <AppIcon v-else name="image" size="18" />
        {{ loading ? '生成中...' : '生成背景' }}
      </button>
    </template>

    <!-- Style -->
    <template v-else-if="currentTab === 'style'">
      <div class="panel-section">
        <label>选择风格</label>
        <div class="style-grid">
          <div v-for="s in styleOptions" :key="s.index"
            :class="['style-card', { active: selectedStyle === s.index }]"
            @click="selectedStyle = s.index">
            <span class="style-initial">{{ s.label.charAt(0) }}</span>
            <span class="style-name">{{ s.label }}</span>
          </div>
        </div>
      </div>
      <div class="panel-tip">
        <AppIcon name="info" size="14" />
        适合人物照片，AI 将重绘为所选艺术风格
      </div>
      <button class="btn-primary" @click="$emit('edit', { type: 'style', image: uploadedImage, styleIndex: selectedStyle })" :disabled="loading || !uploadedImage">
        <span v-if="loading" class="loading-spinner"></span>
        <AppIcon v-else name="sketch" size="18" />
        {{ loading ? '重绘中...' : '开始重绘' }}
      </button>
    </template>

    <!-- Sketch -->
    <template v-else-if="currentTab === 'sketch'">
      <div class="panel-section">
        <label>涂鸦画布</label>
        <div class="sketch-canvas-wrap">
          <canvas ref="sketchCanvas" width="320" height="320" class="sketch-canvas"
            @mousedown="sketchStart" @mousemove="sketchDraw" @mouseup="sketchEnd" @mouseleave="sketchEnd"></canvas>
          <button class="sketch-clear-btn" @click="clearSketch">清除</button>
        </div>
      </div>
      <div class="panel-section">
        <label>描述画面内容</label>
        <textarea v-model="sketchPrompt" class="input-field" placeholder="例如：一只猫坐在窗边..." rows="3"></textarea>
      </div>
      <button class="btn-primary" @click="submitSketch" :disabled="loading">
        <span v-if="loading" class="loading-spinner"></span>
        <AppIcon v-else name="sketch" size="18" />
        {{ loading ? '生成中...' : '涂鸦生图' }}
      </button>
    </template>
  </div>
</template>

<script>
import AppIcon from '../common/AppIcon.vue'
import ImageUpload from '../common/ImageUpload.vue'

export default {
  name: 'EditPanel',
  components: { AppIcon, ImageUpload },
  props: {
    currentTab: { type: String, default: 'instruct' },
    loading: { type: Boolean, default: false }
  },
  emits: ['update:subTab', 'edit', 'update:uploadedImage'],
  data() {
    return {
      uploadedImage: null,
      form: { prompt: '', apiChoice: 'API-1' },
      inpaintPrompt: '',
      selectedStyle: 0,
      sketchPrompt: '',
      sketchDrawing: false,
      sketchLastPos: null,
      inpaintDrawing: false,
      inpaintLastPos: null,
      canvasSize: { w: 512, h: 512 },
      subTabs: [
        { key: 'instruct', label: '指令编辑' },
        { key: 'inpaint', label: '局部重绘' },
        { key: 'background', label: '背景生成' },
        { key: 'style', label: '风格重绘' },
        { key: 'sketch', label: '涂鸦作画' }
      ],
      apiOptions: [
        { value: 'API-1', label: '千问', color: '#c98d5f' },
        { value: 'API-2', label: '通义', color: '#0891b2' },
        { value: 'API-3', label: '模拟', color: '#6b7280' },
        { value: 'API-4', label: '万象Pro', color: '#a0522d' }
      ],
      styleOptions: [
        { index: 0, label: '复古漫画' }, { index: 1, label: '3D童话' },
        { index: 2, label: '二次元' }, { index: 3, label: '小清新' },
        { index: 4, label: '未来科技' }, { index: 5, label: '国画古风' },
        { index: 7, label: '炫彩卡通' }, { index: 30, label: '童话世界' },
        { index: 31, label: '黏土世界' }, { index: 35, label: '3D世界' },
        { index: 36, label: '二次元世界' }, { index: 38, label: '蜡笔世界' },
      ]
    }
  },
  methods: {
    startDraw(e) { this.inpaintDrawing = true; this.setPos(e, 'inpaint') },
    endDraw() { this.inpaintDrawing = false },
    draw(e) {
      if (!this.inpaintDrawing) return
      const c = this.$refs.canvas
      const ctx = c.getContext('2d')
      const { x, y } = this.getPos(e, c)
      ctx.strokeStyle = 'rgba(255,0,0,0.6)'; ctx.lineWidth = 20; ctx.lineCap = 'round'
      ctx.beginPath(); ctx.moveTo(this.inpaintLastPos.x, this.inpaintLastPos.y); ctx.lineTo(x, y); ctx.stroke()
      this.inpaintLastPos = { x, y }
    },
    setPos(e) {
      const c = this.$refs.canvas
      const pos = this.getPos(e, c)
      this.inpaintLastPos = pos
    },
    getPos(e, canvas) {
      const r = canvas.getBoundingClientRect()
      const sx = this.canvasSize.w / r.width
      const sy = this.canvasSize.h / r.height
      return { x: (e.clientX - r.left) * sx, y: (e.clientY - r.top) * sy }
    },
    clearCanvas() {
      const c = this.$refs.canvas
      c.getContext('2d').clearRect(0, 0, c.width, c.height)
    },
    sketchStart(e) {
      this.sketchDrawing = true
      const r = this.$refs.sketchCanvas.getBoundingClientRect()
      this.sketchLastPos = { x: e.clientX - r.left, y: e.clientY - r.top }
    },
    sketchDraw(e) {
      if (!this.sketchDrawing) return
      const c = this.$refs.sketchCanvas
      const ctx = c.getContext('2d')
      const r = c.getBoundingClientRect()
      const x = e.clientX - r.left; const y = e.clientY - r.top
      ctx.strokeStyle = '#000'; ctx.lineWidth = 3; ctx.lineCap = 'round'
      ctx.beginPath(); ctx.moveTo(this.sketchLastPos.x, this.sketchLastPos.y); ctx.lineTo(x, y); ctx.stroke()
      this.sketchLastPos = { x, y }
    },
    sketchEnd() { this.sketchDrawing = false },
    clearSketch() {
      this.$refs.sketchCanvas.getContext('2d').clearRect(0, 0, 320, 320)
    },
    submitSketch() {
      const dataUrl = this.$refs.sketchCanvas.toDataURL('image/png')
      this.$emit('edit', { type: 'sketch', image: dataUrl, prompt: this.sketchPrompt })
    },
    submitInpaint() {
      const c = this.$refs.canvas
      const maskCanvas = document.createElement('canvas')
      maskCanvas.width = c.width; maskCanvas.height = c.height
      const mCtx = maskCanvas.getContext('2d')
      mCtx.fillStyle = 'black'; mCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height)
      const src = c.getContext('2d', { willReadFrequently: true }).getImageData(0, 0, c.width, c.height)
      const dst = mCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height)
      for (let i = 0; i < src.data.length; i += 4) {
        if (src.data[i + 3] > 0) {
          dst.data[i] = 255; dst.data[i+1] = 255; dst.data[i+2] = 255; dst.data[i+3] = 255
        }
      }
      mCtx.putImageData(dst, 0, 0)
      const maskData = maskCanvas.toDataURL('image/png')
      this.$emit('edit', { type: 'inpaint', image: this.uploadedImage, mask: maskData, prompt: this.inpaintPrompt })
    }
  },
  watch: {
    uploadedImage: {
      handler(img) {
        this.$emit('update:uploadedImage', img)
        if (img) {
          const i = new Image()
          i.onload = () => { this.canvasSize = { w: i.width, h: i.height } }
          i.src = img
        }
      },
      immediate: true
    }
  }
}
</script>

<style scoped>
.params-panel { display: flex; flex-direction: column; gap: 18px; }

.edit-sub-tabs { display: flex; gap: 4px; margin-bottom: 0; }

.sub-tab-btn {
  flex: 1;
  padding: 8px 4px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 12px;
  color: var(--text-muted);
  transition: all var(--transition);
  white-space: nowrap;
}

.sub-tab-btn:hover {
  color: var(--text-primary);
  border-color: var(--accent);
}

.sub-tab-btn.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.panel-section { display: flex; flex-direction: column; gap: 6px; }
.panel-section label { font-weight: 600; font-size: 13px; color: var(--text-primary); }

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
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.style-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 12px 6px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all var(--transition);
}

.style-card:hover {
  border-color: var(--accent);
  background: var(--accent-light);
}

.style-card.active {
  background: var(--accent-light);
  border-color: var(--accent);
}

.style-initial {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
}

.style-name {
  font-size: 12px;
  color: var(--text-secondary);
}

.panel-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: var(--accent-light);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--text-secondary);
}

.sketch-canvas-wrap { position: relative; display: inline-block; width: 100%; min-height: 320px; }
.sketch-canvas { width: 100%; height: 320px; background: white; border: 1px solid var(--border); border-radius: var(--radius); cursor: crosshair; display: block; }

.sketch-clear-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 5px 10px;
  background: var(--danger);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 12px;
  transition: background var(--transition);
}

.sketch-clear-btn:hover { background: #dc2626; }

.inpaint-bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: var(--radius);
  pointer-events: none;
}

.inpaint-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  cursor: crosshair;
  border-radius: var(--radius);
}
</style>
