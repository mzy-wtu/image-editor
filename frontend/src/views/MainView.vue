<template>
  <div class="main-app" :class="{ 'dark-theme': isDarkTheme }">
    <header class="top-navbar">
      <div class="navbar-left">
        <h1 class="logo">🎨 AI图像工坊</h1>
      </div>
      <div class="navbar-right">
        <button class="icon-btn" @click="isDarkTheme = !isDarkTheme">{{ isDarkTheme ? '☀️' : '🌙' }}</button>
        <button class="icon-btn" @click="$router.push('/history')">📚</button>
        <button v-if="user?.is_admin" class="icon-btn" @click="$router.push('/admin')">👥</button>
        <div class="user-menu">
          <span>{{ user?.username }}</span>
          <button class="logout-btn" @click="logout">退出</button>
        </div>
      </div>
    </header>
    <div class="main-container">
      <aside class="sidebar">
        <div class="mode-selector">
          <button :class="['mode-btn', { active: activeTab === 'generate' }]" @click="activeTab = 'generate'">✨ 文生图</button>
          <button :class="['mode-btn', { active: activeTab === 'edit' }]" @click="activeTab = 'edit'">🖌️ 图像编辑</button>
        </div>
        <div v-if="activeTab === 'generate'" class="params-panel">
          <div class="panel-section">
            <label>提示词</label>
            <textarea v-model="generateForm.prompt" placeholder="描述你想要生成的图像..." rows="6"></textarea>
            <div class="prompt-actions">
              <button class="small-btn" @click="showTemplates = true">📝 模板</button>
              <button class="small-btn" @click="enhancePrompt">✨ 增强</button>
            </div>
          </div>
          <div class="panel-section">
            <label>负面提示词</label>
            <textarea v-model="generateForm.negativePrompt" placeholder="不想要的元素..." rows="2"></textarea>
          </div>
          <div class="panel-section">
            <label>模型选择</label>
            <div class="api-selector">
              <label v-for="api in apiOptions" :key="api.value" class="radio-card">
                <input type="radio" :value="api.value" v-model="generateForm.apiChoice">
                <span>{{ api.icon }} {{ api.label }}</span>
              </label>
            </div>
          </div>
          <div class="panel-section">
            <label>图像尺寸</label>
            <select v-model="generateForm.size">
              <option value="1024*1024">正方形 1024×1024</option>
              <option value="1024*1536">竖版 1024×1536</option>
              <option value="1536*1024">横版 1536×1024</option>
            </select>
          </div>
          <div class="panel-section">
            <label>生成数量: {{ generateForm.count }}</label>
            <input type="range" v-model="generateForm.count" min="1" max="4">
          </div>
          <button class="generate-btn" @click="generateImage" :disabled="isGenerating || !generateForm.prompt">
            {{ isGenerating ? '⏳ 生成中...' : '🚀 开始生成' }}
          </button>
        </div>
        <div v-else class="params-panel">
          <div class="panel-section">
            <label>上传图像</label>
            <div class="upload-area" @click="$refs.fileInput.click()" @drop.prevent="handleDrop" @dragover.prevent>
              <input ref="fileInput" type="file" accept="image/*" @change="handleImageUpload" style="display:none">
              <div v-if="!uploadedImage" class="upload-placeholder">
                <span>📁</span>
                <p>点击或拖拽上传</p>
              </div>
              <div v-else class="uploaded-preview">
                <img :src="uploadedImage">
                <button class="remove-btn" @click.stop="uploadedImage = null">✕</button>
              </div>
            </div>
          </div>
          <div class="panel-section">
            <label>编辑指令</label>
            <textarea v-model="editForm.prompt" placeholder="描述编辑效果..." rows="5"></textarea>
          </div>
          <div class="panel-section">
            <label>模型选择</label>
            <div class="api-selector">
              <label v-for="api in apiOptions" :key="api.value" class="radio-card">
                <input type="radio" :value="api.value" v-model="editForm.apiChoice">
                <span>{{ api.icon }} {{ api.label }}</span>
              </label>
            </div>
          </div>
          <button class="generate-btn" @click="editImage" :disabled="isEditing || !uploadedImage">
            {{ isEditing ? '⏳ 编辑中...' : '🎨 开始编辑' }}
          </button>
        </div>
      </aside>
      <main class="content-area">
        <div v-if="activeTab === 'generate'">
          <div v-if="!generatedImages.length && !isGenerating" class="empty-state">
            <div class="empty-icon">🎨</div>
            <h3>开始创作</h3>
            <p>在左侧输入提示词生成图像</p>
          </div>
          <div v-if="isGenerating" class="generating-state">
            <div class="loading-spinner"></div>
            <p>AI创作中...</p>
          </div>
          <div v-if="generatedImages.length" class="image-grid">
            <div v-for="(img, i) in generatedImages" :key="i" class="image-card" @click="previewImage = img">
              <img :src="img">
              <div class="image-overlay">
                <button @click.stop="downloadImage(img, i)">💾</button>
                <button @click.stop="previewImage = img">🔍</button>
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <div v-if="!uploadedImage" class="empty-state">
            <div class="empty-icon">🖼️</div>
            <h3>上传图像</h3>
            <p>在左侧上传图像开始编辑</p>
          </div>
          <div v-if="isEditing" class="generating-state">
            <div class="loading-spinner"></div>
            <p>编辑中...</p>
          </div>
          <div v-if="uploadedImage && editedImage" class="comparison-view">
            <div class="comparison-side">
              <h4>原图</h4>
              <img :src="uploadedImage">
            </div>
            <div class="comparison-side">
              <h4>编辑后</h4>
              <img :src="editedImage">
            </div>
          </div>
        </div>
        <div v-if="logs.length" class="logs-panel">
          <div class="logs-header">
            <span>📋 日志</span>
            <button @click="logs = []">✕</button>
          </div>
          <div class="logs-content">
            <div v-for="(log, i) in logs" :key="i">{{ log }}</div>
          </div>
        </div>
      </main>
    </div>
    <div v-if="showTemplates" class="modal-overlay" @click="showTemplates = false">
      <div class="modal-content" @click.stop>
        <h3>提示词模板</h3>
        <button class="close-btn" @click="showTemplates = false">✕</button>
        <div v-for="t in promptTemplates" :key="t.id" class="template-card" @click="useTemplate(t)">
          <h4>{{ t.title }}</h4>
          <p>{{ t.prompt }}</p>
        </div>
      </div>
    </div>
    <div v-if="previewImage" class="modal-overlay" @click="previewImage = null">
      <img :src="previewImage" class="preview-img">
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data() {
    return {
      user: null,
      isDarkTheme: false,
      activeTab: 'generate',
      generateForm: { prompt: '', negativePrompt: '', apiChoice: 'API-1', size: '1024*1536', count: 1 },
      editForm: { prompt: '', apiChoice: 'API-1' },
      uploadedImage: null,
      generatedImages: [],
      editedImage: null,
      isGenerating: false,
      isEditing: false,
      logs: [],
      showTemplates: false,
      previewImage: null,
      apiOptions: [
        { value: 'API-1', label: '千问', icon: '🤖' },
        { value: 'API-2', label: '通义', icon: '🎯' },
        { value: 'API-3', label: '模拟', icon: '🧪' }
      ],
      promptTemplates: [
        { id: 1, title: '写实风格', prompt: '超高清，写实风格，细节丰富，专业摄影' },
        { id: 2, title: '动漫风格', prompt: '动漫风格，精美插画，色彩鲜艳，高质量' },
        { id: 3, title: '水彩画', prompt: '水彩画风格，柔和色调，艺术感强' },
        { id: 4, title: '赛博朋克', prompt: '赛博朋克风格，霓虹灯，未来科技感，夜景' }
      ]
    }
  },
  mounted() {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      this.user = JSON.parse(userStr)
      axios.defaults.withCredentials = true
    } else {
      this.$router.push('/')
    }
  },
  methods: {
    async logout() {
      await axios.get('http://47.121.190.137:5000/api/logout')
      localStorage.removeItem('user')
      this.$router.push('/')
    },
    async generateImage() {
      if (!this.generateForm.prompt) return
      this.isGenerating = true
      this.logs = []
      this.generatedImages = []
      try {
        const response = await axios.post('http://47.121.190.137:5000/api/generate', {
          prompt: this.generateForm.prompt,
          api_choice: this.generateForm.apiChoice
        })
        this.generatedImages = [response.data.image]
        if (response.data.logs) this.logs = response.data.logs
      } catch (error) {
        alert('生成失败: ' + (error.response?.data?.error || error.message))
      } finally {
        this.isGenerating = false
      }
    },
    handleImageUpload(e) {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.uploadedImage = e.target.result
          this.editedImage = null
        }
        reader.readAsDataURL(file)
      }
    },
    handleDrop(e) {
      const file = e.dataTransfer.files[0]
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.uploadedImage = e.target.result
          this.editedImage = null
        }
        reader.readAsDataURL(file)
      }
    },
    async editImage() {
      if (!this.uploadedImage) return
      this.isEditing = true
      this.logs = []
      try {
        const response = await axios.post('http://47.121.190.137:5000/api/edit', {
          image: this.uploadedImage,
          prompt: this.editForm.prompt,
          api_choice: this.editForm.apiChoice
        })
        this.editedImage = response.data.image
        if (response.data.logs) this.logs = response.data.logs
      } catch (error) {
        alert('编辑失败: ' + (error.response?.data?.error || error.message))
      } finally {
        this.isEditing = false
      }
    },
    downloadImage(img, index) {
      const link = document.createElement('a')
      link.href = img
      link.download = `image_${index}_${Date.now()}.png`
      link.click()
    },
    useTemplate(template) {
      this.generateForm.prompt = template.prompt
      this.showTemplates = false
    },
    enhancePrompt() {
      if (this.generateForm.prompt) {
        this.generateForm.prompt += ', 高质量, 精美细节, 专业级'
      }
    }
  }
}
</script>
<style scoped>
.main-app { min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); transition: all 0.3s; }
.dark-theme { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
.top-navbar { background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 20px rgba(0,0,0,0.1); }
.dark-theme .top-navbar { background: rgba(30,30,30,0.95); color: white; }
.logo { font-size: 24px; font-weight: bold; margin: 0; }
.navbar-right { display: flex; gap: 15px; align-items: center; }
.icon-btn { background: none; border: none; font-size: 20px; cursor: pointer; padding: 8px; border-radius: 8px; transition: all 0.2s; }
.icon-btn:hover { background: rgba(0,0,0,0.05); transform: scale(1.1); }
.user-menu { display: flex; gap: 10px; align-items: center; }
.logout-btn { padding: 8px 16px; background: #ff4757; color: white; border: none; border-radius: 8px; cursor: pointer; }
.main-container { display: flex; max-width: 1600px; margin: 20px auto; gap: 20px; padding: 0 20px; }
.sidebar { width: 380px; background: white; border-radius: 16px; padding: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); max-height: calc(100vh - 120px); overflow-y: auto; }
.dark-theme .sidebar { background: rgba(40,40,40,0.95); color: white; }
.mode-selector { display: flex; gap: 10px; margin-bottom: 20px; }
.mode-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; background: white; border-radius: 12px; cursor: pointer; font-size: 14px; transition: all 0.3s; }
.mode-btn.active { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-color: transparent; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
.params-panel { display: flex; flex-direction: column; gap: 20px; }
.panel-section { display: flex; flex-direction: column; gap: 8px; }
.panel-section label { font-weight: 600; font-size: 14px; color: #333; }
.dark-theme .panel-section label { color: #ddd; }
.panel-section textarea, .panel-section select { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 14px; resize: vertical; transition: all 0.3s; }
.panel-section textarea:focus, .panel-section select:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
.prompt-actions { display: flex; gap: 8px; }
.small-btn { padding: 6px 12px; background: #f0f0f0; border: none; border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
.small-btn:hover { background: #e0e0e0; transform: translateY(-1px); }
.api-selector { display: flex; flex-direction: column; gap: 8px; }
.radio-card { display: flex; align-items: center; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; cursor: pointer; transition: all 0.3s; }
.radio-card:hover { border-color: #667eea; background: rgba(102,126,234,0.05); }
.radio-card input { margin-right: 10px; }
.generate-btn { padding: 14px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.generate-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102,126,234,0.4); }
.generate-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.upload-area { border: 2px dashed #ccc; border-radius: 12px; padding: 40px; text-align: center; cursor: pointer; transition: all 0.3s; min-height: 200px; display: flex; align-items: center; justify-content: center; }
.upload-area:hover { border-color: #667eea; background: rgba(102,126,234,0.05); }
.upload-placeholder span { font-size: 48px; display: block; margin-bottom: 10px; }
.uploaded-preview { position: relative; width: 100%; }
.uploaded-preview img { width: 100%; border-radius: 8px; }
.remove-btn { position: absolute; top: 10px; right: 10px; background: rgba(255,0,0,0.8); color: white; border: none; border-radius: 50%; width: 30px; height: 30px; cursor: pointer; }
.content-area { flex: 1; background: white; border-radius: 16px; padding: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); min-height: calc(100vh - 120px); }
.dark-theme .content-area { background: rgba(40,40,40,0.95); color: white; }
.empty-state { text-align: center; padding: 100px 20px; }
.empty-icon { font-size: 80px; margin-bottom: 20px; }
.empty-state h3 { font-size: 24px; margin-bottom: 10px; }
.generating-state { text-align: center; padding: 100px 20px; }
.loading-spinner { width: 60px; height: 60px; border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.image-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.image-card { position: relative; border-radius: 12px; overflow: hidden; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.image-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
.image-card img { width: 100%; display: block; }
.image-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.7), transparent); padding: 15px; display: flex; gap: 10px; justify-content: center; opacity: 0; transition: opacity 0.3s; }
.image-card:hover .image-overlay { opacity: 1; }
.image-overlay button { background: rgba(255,255,255,0.9); border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 16px; }
.comparison-view { display: flex; flex-direction: column; gap: 20px; }
.comparison-side { flex: 1; text-align: center; }
.comparison-side h4 { margin-bottom: 10px; }
.comparison-side img { width: 100%; max-width: 600px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.logs-panel { margin-top: 20px; background: #f9f9f9; border-radius: 12px; padding: 15px; }
.dark-theme .logs-panel { background: rgba(30,30,30,0.8); }
.logs-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: 600; }
.logs-content { max-height: 200px; overflow-y: auto; font-family: monospace; font-size: 12px; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { background: white; border-radius: 16px; padding: 30px; max-width: 600px; max-height: 80vh; overflow-y: auto; position: relative; }
.dark-theme .modal-content { background: #2a2a2a; color: white; }
.close-btn { position: absolute; top: 15px; right: 15px; background: none; border: none; font-size: 24px; cursor: pointer; }
.template-card { padding: 15px; border: 2px solid #e0e0e0; border-radius: 8px; margin-bottom: 10px; cursor: pointer; transition: all 0.3s; }
.template-card:hover { border-color: #667eea; background: rgba(102,126,234,0.05); }
.preview-img { max-width: 90vw; max-height: 90vh; border-radius: 12px; }
</style>
