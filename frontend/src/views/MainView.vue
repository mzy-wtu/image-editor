<template>
  <div class="main-app">
    <header class="top-navbar">
      <div class="navbar-left">
        <div class="logo-icon">
          <AppIcon name="image" size="22" />
        </div>
        <h1 class="logo">AI图像工坊</h1>
      </div>
      <div class="navbar-right">
        <button class="icon-btn" @click="toggleTheme" :title="isDarkTheme ? '浅色模式' : '深色模式'">
          <AppIcon :name="isDarkTheme ? 'sun' : 'moon'" size="18" />
        </button>
        <button class="icon-btn" @click="$router.push('/history')" title="历史记录">
          <AppIcon name="history" size="18" />
        </button>
        <button v-if="user?.is_admin" class="icon-btn" @click="$router.push('/admin')" title="用户管理">
          <AppIcon name="admin" size="18" />
        </button>
        <div class="user-menu">
          <span class="username">{{ user?.username }}</span>
          <button class="logout-btn" @click="logout">
            <AppIcon name="logout" size="16" />
          </button>
        </div>
      </div>
    </header>

    <div class="main-container">
      <aside class="sidebar">
        <div class="mode-selector">
          <button :class="['mode-btn', { active: activeTab === 'generate' }]" @click="activeTab = 'generate'">
            <AppIcon name="plus" size="16" />文生图
          </button>
          <button :class="['mode-btn', { active: activeTab === 'edit' }]" @click="activeTab = 'edit'">
            <AppIcon name="edit" size="16" />图像编辑
          </button>
        </div>

        <GeneratePanel
          v-if="activeTab === 'generate'"
          :loading="isGenerating"
          @generate="handleGenerate"
        />
        <EditPanel
          v-else
          :current-tab="editSubTab"
          :loading="isEditing"
          @update:sub-tab="editSubTab = $event"
          @update:uploaded-image="uploadedImage = $event"
          @edit="handleEdit"
        />
      </aside>

      <main class="content-area">
        <template v-if="activeTab === 'generate'">
          <EmptyState
            v-if="!generatedImages.length && !isGenerating"
            icon="image" title="开始创作" description="在左侧输入提示词生成图像"
          />
          <LoadingSpinner v-if="isGenerating" text="AI创作中..." />
          <div v-if="generatedImages.length" class="image-grid">
            <ImageCard
              v-for="(img, i) in generatedImages" :key="i"
              :src="img" :index="i"
              @preview="previewImage = $event"
              @download="downloadImage"
            />
          </div>
        </template>

        <template v-else>
          <EmptyState
            v-if="!isEditing && !editedImage && editSubTab !== 'sketch'"
            icon="image" title="上传图像" description="在左侧上传图像开始编辑"
          />
          <EmptyState
            v-if="!isEditing && !editedImage && editSubTab === 'sketch'"
            icon="sketch" title="涂鸦作画" description="在左侧画布上涂鸦，输入描述后生成图像"
          />
          <LoadingSpinner v-if="isEditing" text="编辑中..." />
          <div v-if="uploadedImage && editedImage && editSubTab !== 'sketch'" class="comparison-view">
            <div class="comparison-side">
              <h4>原图</h4>
              <img :src="uploadedImage">
            </div>
            <div class="comparison-side">
              <h4>编辑后</h4>
              <img :src="editedImage">
            </div>
          </div>
          <div v-if="editedImage && editSubTab === 'sketch'" class="single-result">
            <h4>生成结果</h4>
            <img :src="editedImage">
          </div>
        </template>

        <div v-if="logs.length" class="logs-panel">
          <div class="logs-header">
            <span>日志</span>
            <button @click="logs = []"><AppIcon name="close" size="16" /></button>
          </div>
          <div class="logs-content">
            <div v-for="(log, i) in logs" :key="i">{{ log }}</div>
          </div>
        </div>
      </main>
    </div>

    <div v-if="previewImage" class="modal-overlay" @click="previewImage = null">
      <img :src="previewImage" class="preview-img" @click.stop>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AppIcon from '../components/common/AppIcon.vue'
import ImageCard from '../components/common/ImageCard.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import EmptyState from '../components/common/EmptyState.vue'
import GeneratePanel from '../components/panels/GeneratePanel.vue'
import EditPanel from '../components/panels/EditPanel.vue'
import { useDarkTheme } from '../composables/useDarkTheme.js'
import { useToast } from '../components/common/Toast.vue'

export default {
  name: 'MainView',
  components: { AppIcon, ImageCard, LoadingSpinner, EmptyState, GeneratePanel, EditPanel },
  setup() {
    const { isDarkTheme, toggleTheme } = useDarkTheme()
    const { show: toast } = useToast()
    return { isDarkTheme, toggleTheme, toast }
  },
  data() {
    return {
      user: null,
      activeTab: 'generate',
      editSubTab: 'instruct',
      generatedImages: [],
      uploadedImage: null,
      editedImage: null,
      isGenerating: false,
      isEditing: false,
      logs: [],
      previewImage: null
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
      await axios.get('/api/logout')
      localStorage.removeItem('user')
      this.$router.push('/')
    },
    async handleGenerate(form) {
      this.isGenerating = true
      this.logs = []
      this.generatedImages = []
      try {
        const res = await axios.post('/api/generate', {
          prompt: form.prompt,
          api_choice: form.apiChoice,
          negativePrompt: form.negativePrompt,
          size: form.size,
          count: form.count,
          seed: form.seed || null
        })
        this.generatedImages = res.data.images || (res.data.image ? [res.data.image] : [])
        if (res.data.logs) this.logs = res.data.logs
      } catch (error) {
        this.toast(error.response?.data?.error || error.message || '生成失败', 'error')
      } finally {
        this.isGenerating = false
      }
    },
    async handleEdit(payload) {
      this.isEditing = true
      this.logs = []
      this.editedImage = null
      this.uploadedImage = payload.image

      const endpoints = {
        instruct: { url: '/api/edit', data: { image: payload.image, prompt: payload.prompt, api_choice: payload.apiChoice, size: payload.size, count: payload.count } },
        inpaint: { url: '/api/inpaint', data: { image: payload.image, mask: payload.mask, prompt: payload.prompt, size: payload.size, count: payload.count } },
        background: { url: '/api/background', data: { image: payload.image, prompt: payload.prompt } },
        style: { url: '/api/style-repaint', data: { image: payload.image, style_index: payload.styleIndex } },
        sketch: { url: '/api/sketch', data: { image: payload.image, prompt: payload.prompt } }
      }

      try {
        const ep = endpoints[payload.type]
        const res = await axios.post(ep.url, ep.data)
        this.editedImage = res.data.image
        if (res.data.logs) this.logs = res.data.logs
      } catch (error) {
        this.toast('编辑失败: ' + (error.response?.data?.error || error.message), 'error')
      } finally {
        this.isEditing = false
      }
    },
    downloadImage(img, index) {
      const link = document.createElement('a')
      link.href = img
      link.download = `image_${index}_${Date.now()}.png`
      link.click()
    }
  }
}
</script>

<style scoped>
.main-app {
  min-height: 100vh;
  background: var(--bg-secondary);
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #c98d5f, #a0522d);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.navbar-right {
  display: flex;
  gap: 8px;
  align-items: center;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-left: 4px;
  padding-left: 12px;
  border-left: 1px solid var(--border);
}

.username {
  font-size: 13px;
  color: var(--text-secondary);
  font-weight: 500;
}

.logout-btn {
  width: 32px;
  height: 32px;
  background: var(--danger-bg);
  border: 1px solid var(--danger-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition);
  color: var(--danger);
}

.logout-btn:hover {
  background: #fee2e2;
}

.main-container {
  display: flex;
  max-width: 1500px;
  margin: 0 auto;
  gap: 20px;
  padding: 20px 24px 24px;
}

.sidebar {
  width: 370px;
  flex-shrink: 0;
  padding: 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  max-height: calc(100vh - 96px);
  overflow-y: auto;
}

.content-area {
  flex: 1;
  padding: 24px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  min-height: calc(100vh - 96px);
}

.mode-selector {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.mode-btn {
  flex: 1;
  padding: 10px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all var(--transition);
}

.mode-btn:hover {
  background: var(--accent-light);
  color: var(--accent);
}

.mode-btn.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.comparison-view {
  display: flex;
  gap: 20px;
}

.comparison-side {
  flex: 1;
  text-align: center;
}

.comparison-side h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 12px;
}

.comparison-side img {
  width: 100%;
  max-width: 500px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.single-result {
  text-align: center;
}

.single-result h4 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 12px;
}

.single-result img {
  max-width: 100%;
  border-radius: var(--radius);
  border: 1px solid var(--border);
}

.logs-panel {
  margin-top: 20px;
  background: var(--bg-tertiary);
  border-radius: var(--radius);
  padding: 14px;
  border: 1px solid var(--border);
}

.logs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.logs-header button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-muted);
  padding: 2px;
}

.logs-header button:hover {
  color: var(--text-primary);
}

.logs-content {
  max-height: 160px;
  overflow-y: auto;
  font-family: var(--mono);
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.preview-img {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
}

@media (max-width: 1200px) {
  .main-container {
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
    max-height: none;
  }
  .comparison-view {
    flex-direction: column;
  }
}
</style>
