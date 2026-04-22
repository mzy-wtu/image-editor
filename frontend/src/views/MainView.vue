<template>
  <div class="main-app" :class="{ 'dark-theme': isDarkTheme }">
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
    </div>
    
    <header class="top-navbar">
      <div class="navbar-left">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
        </div>
        <h1 class="logo">AI图像工坊</h1>
      </div>
      <div class="navbar-right">
        <button class="icon-btn" @click="isDarkTheme = !isDarkTheme" :title="isDarkTheme ? '浅色模式' : '深色模式'">
          <svg v-if="isDarkTheme" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"/>
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
          </svg>
        </button>
        <button class="icon-btn" @click="$router.push('/history')" title="历史记录">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 3v5h5M3.05 13A9 9 0 1 0 6 5.3L3 8M12 7v5l4 2"/>
          </svg>
        </button>
        <button v-if="user?.is_admin" class="icon-btn" @click="$router.push('/admin')" title="用户管理">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </button>
        <div class="user-menu">
          <span class="username">{{ user?.username }}</span>
          <button class="logout-btn" @click="logout">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>
            </svg>
          </button>
        </div>
      </div>
    </header>
    
    <div class="main-container">
      <aside class="sidebar">
        <div class="mode-selector">
          <button :class="['mode-btn', { active: activeTab === 'generate' }]" @click="activeTab = 'generate'">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 3v18M3 12h18"/>
            </svg>
            文生图
          </button>
          <button :class="['mode-btn', { active: activeTab === 'edit' }]" @click="activeTab = 'edit'">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            图像编辑
          </button>
        </div>
        
        <div v-if="activeTab === 'generate'" class="params-panel">
          <div class="panel-section">
            <label>提示词</label>
            <textarea v-model="generateForm.prompt" placeholder="描述你想要生成的图像..." rows="6"></textarea>
            <div class="prompt-actions">
              <button class="small-btn" @click="showTemplates = true">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
                </svg>
                模板
              </button>
              <button class="small-btn" @click="enhancePrompt">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                </svg>
                增强
              </button>
            </div>
          </div>
          <div class="panel-section">
            <label>负面提示词</label>
            <textarea v-model="generateForm.negativePrompt" placeholder="不想要的元素..." rows="2"></textarea>
          </div>
          <div class="panel-section">
            <label>模型选择</label>
            <div class="api-selector">
              <label v-for="api in apiOptions" :key="api.value" class="radio-card" :class="{ active: generateForm.apiChoice === api.value }">
                <input type="radio" :value="api.value" v-model="generateForm.apiChoice">
                <span class="api-icon">{{ api.icon }}</span>
                <span class="api-label">{{ api.label }}</span>
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
            <div class="range-wrapper">
              <input type="range" v-model="generateForm.count" min="1" max="4">
              <div class="range-dots">
                <span v-for="i in 4" :key="i" :class="{ active: i <= generateForm.count }">{{ i }}</span>
              </div>
            </div>
          </div>
          <button class="generate-btn" @click="generateImage" :disabled="isGenerating || !generateForm.prompt">
            <svg v-if="!isGenerating" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
              <path d="M3.27 6.96L12 12.01l8.73-5.05M12 22.08V12"/>
            </svg>
            <span v-if="isGenerating" class="loading-spinner"></span>
            {{ isGenerating ? '生成中...' : '开始生成' }}
          </button>
        </div>
        
        <div v-else class="params-panel">
          <div class="edit-sub-tabs">
            <button :class="['sub-tab-btn', { active: editSubTab === 'instruct' }]" @click="editSubTab = 'instruct'">指令编辑</button>
            <button :class="['sub-tab-btn', { active: editSubTab === 'inpaint' }]" @click="editSubTab = 'inpaint'">局部重绘</button>
            <button :class="['sub-tab-btn', { active: editSubTab === 'background' }]" @click="editSubTab = 'background'">背景生成</button>
            <button :class="['sub-tab-btn', { active: editSubTab === 'style' }]" @click="editSubTab = 'style'">风格重绘</button>
            <button :class="['sub-tab-btn', { active: editSubTab === 'sketch' }]" @click="editSubTab = 'sketch'">涂鸦作画</button>
          </div>

          <div class="panel-section" v-if="editSubTab !== 'sketch'">
            <label>上传图像</label>
            <div class="upload-area" @click="$refs.fileInput.click()" @drop.prevent="handleDrop" @dragover.prevent>
              <input ref="fileInput" type="file" accept="image/*" @change="handleImageUpload" style="display:none">
              <div v-if="!uploadedImage" class="upload-placeholder">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                <p>点击或拖拽上传</p>
              </div>
              <div v-else class="uploaded-preview">
                <img :src="uploadedImage">
                <button class="remove-btn" @click.stop="uploadedImage = null; editedImage = null">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <template v-if="editSubTab === 'instruct'">
            <div class="panel-section">
              <label>编辑指令</label>
              <textarea v-model="editForm.prompt" placeholder="描述编辑效果，例如：将背景改为星空..." rows="4"></textarea>
            </div>
            <div class="panel-section">
              <label>模型选择</label>
              <div class="api-selector">
                <label v-for="api in apiOptions" :key="api.value" class="radio-card" :class="{ active: editForm.apiChoice === api.value }">
                  <input type="radio" :value="api.value" v-model="editForm.apiChoice">
                  <span class="api-icon">{{ api.icon }}</span>
                  <span class="api-label">{{ api.label }}</span>
                </label>
              </div>
            </div>
            <button class="generate-btn" @click="editImage" :disabled="isEditing || !uploadedImage">
              <svg v-if="!isEditing" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
              <span v-if="isEditing" class="loading-spinner"></span>
              {{ isEditing ? '处理中...' : '开始编辑' }}
            </button>
          </template>

          <template v-else-if="editSubTab === 'inpaint'">
            <div class="panel-section">
              <label>在原图上涂抹要重绘的区域</label>
              <div class="sketch-canvas-wrap">
                <img v-if="uploadedImage" :src="uploadedImage" class="inpaint-bg-img" />
                <canvas
                  ref="inpaintCanvas"
                  :width="inpaintSize.w" :height="inpaintSize.h"
                  class="inpaint-canvas"
                  @mousedown="inpaintStart"
                  @mousemove="inpaintDraw"
                  @mouseup="inpaintEnd"
                  @mouseleave="inpaintEnd"
                ></canvas>
                <button class="sketch-clear-btn" @click="clearInpaint">清除</button>
              </div>
            </div>
            <div class="panel-section">
              <label>重绘内容描述</label>
              <textarea v-model="inpaintForm.prompt" placeholder="例如：一只戴红色眼镜的猫..." rows="3"></textarea>
            </div>
            <div class="panel-tip">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
              先上传原图，再在图上涂抹要修改的区域
            </div>
            <button class="generate-btn" @click="submitInpaint" :disabled="isEditing || !uploadedImage">
              <span v-if="isEditing" class="loading-spinner"></span>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/>
              </svg>
              {{ isEditing ? '重绘中...' : '开始局部重绘' }}
            </button>
          </template>

          <template v-else-if="editSubTab === 'background'">
            <div class="panel-section">
              <label>背景描述</label>
              <textarea v-model="bgForm.prompt" placeholder="描述想要的背景，例如：夕阳下的海滩、星空下的城市..." rows="4"></textarea>
            </div>
            <div class="panel-tip">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
              AI 自动识别主体，生成全新背景（请上传已抠图的透明背景PNG）
            </div>
            <button class="generate-btn" @click="generateBackground" :disabled="isEditing || !uploadedImage">
              <span v-if="isEditing" class="loading-spinner"></span>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/>
              </svg>
              {{ isEditing ? '生成中...' : '生成背景' }}
            </button>
          </template>

          <template v-else-if="editSubTab === 'style'">
            <div class="panel-section">
              <label>选择风格</label>
              <div class="style-grid">
                <div
                  v-for="s in styleOptions"
                  :key="s.index"
                  :class="['style-card', { active: styleForm.styleIndex === s.index }]"
                  @click="styleForm.styleIndex = s.index"
                >
                  <span class="style-emoji">{{ s.emoji }}</span>
                  <span class="style-name">{{ s.label }}</span>
                </div>
              </div>
            </div>
            <div class="panel-tip">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
              适合人物照片，AI 将重绘为所选艺术风格
            </div>
            <button class="generate-btn" @click="styleRepaint" :disabled="isEditing || !uploadedImage">
              <span v-if="isEditing" class="loading-spinner"></span>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
              {{ isEditing ? '重绘中...' : '开始重绘' }}
            </button>
          </template>

          <template v-else-if="editSubTab === 'sketch'">
            <div class="panel-section">
              <label>涂鸦画布</label>
              <div class="sketch-canvas-wrap">
                <canvas
                  ref="sketchCanvas"
                  width="320" height="320"
                  class="sketch-canvas"
                  @mousedown="sketchStart"
                  @mousemove="sketchDraw"
                  @mouseup="sketchEnd"
                  @mouseleave="sketchEnd"
                ></canvas>
                <button class="sketch-clear-btn" @click="clearSketch">清除</button>
              </div>
            </div>
            <div class="panel-section">
              <label>描述画面内容</label>
              <textarea v-model="sketchForm.prompt" placeholder="例如：一只猫坐在窗边..." rows="3"></textarea>
            </div>
            <button class="generate-btn" @click="submitSketch" :disabled="isEditing">
              <span v-if="isEditing" class="loading-spinner"></span>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
              {{ isEditing ? '生成中...' : '涂鸦生图' }}
            </button>
          </template>
        </div>
      </aside>
      
      <main class="content-area">
        <div v-if="activeTab === 'generate'">
          <div v-if="!generatedImages.length && !isGenerating" class="empty-state">
            <div class="empty-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <path d="M21 15l-5-5L5 21"/>
              </svg>
            </div>
            <h3>开始创作</h3>
            <p>在左侧输入提示词生成图像</p>
          </div>
          <div v-if="isGenerating" class="generating-state">
            <div class="generating-spinner">
              <div class="spinner-ring"></div>
              <div class="spinner-ring"></div>
              <div class="spinner-ring"></div>
            </div>
            <p>AI创作中...</p>
          </div>
          <div v-if="generatedImages.length" class="image-grid">
            <div v-for="(img, i) in generatedImages" :key="i" class="image-card" @click="previewImage = img">
              <img :src="img">
              <div class="image-overlay">
                <button @click.stop="downloadImage(img, i)" title="下载">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                </button>
                <button @click.stop="previewImage = img" title="预览">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8"/>
                    <path d="M21 21l-4.35-4.35"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else>
          <div v-if="!uploadedImage && editSubTab !== 'sketch'" class="empty-state">
            <div class="empty-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <path d="M21 15l-5-5L5 21"/>
              </svg>
            </div>
            <h3>上传图像</h3>
            <p>在左侧上传图像开始编辑</p>
          </div>
          <div v-if="!editedImage && editSubTab === 'sketch' && !isEditing" class="empty-state">
            <div class="empty-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
            </div>
            <h3>涂鸦作画</h3>
            <p>在左侧画布上涂鸦，输入描述后生成图像</p>
          </div>
          <div v-if="isEditing" class="generating-state">
            <div class="generating-spinner">
              <div class="spinner-ring"></div>
              <div class="spinner-ring"></div>
              <div class="spinner-ring"></div>
            </div>
            <p>编辑中...</p>
          </div>
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
          <div v-if="editedImage && editSubTab === 'sketch'" class="comparison-side" style="text-align:center">
            <h4>生成结果</h4>
            <img :src="editedImage" style="max-width:100%;border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,0.2)">
          </div>
        </div>
        
        <div v-if="logs.length" class="logs-panel">
          <div class="logs-header">
            <span>📋 日志</span>
            <button @click="logs = []">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
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
        <button class="close-btn" @click="showTemplates = false">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
        <div v-for="t in promptTemplates" :key="t.id" class="template-card" @click="useTemplate(t)">
          <h4>{{ t.title }}</h4>
          <p>{{ t.prompt }}</p>
        </div>
      </div>
    </div>
    
    <div v-if="previewImage" class="modal-overlay" @click="previewImage = null" @click.stop>
      <img :src="previewImage" class="preview-img">
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MainView',
  data() {
    return {
      user: null,
      isDarkTheme: false,
      activeTab: 'generate',
      generateForm: { prompt: '', negativePrompt: '', apiChoice: 'API-1', size: '1024*1536', count: 1, seed: null },
      editForm: { prompt: '', apiChoice: 'API-1' },
      editSubTab: 'instruct',
      bgForm: { prompt: '' },
      styleForm: { styleIndex: 0 },
      styleOptions: [
        { index: 0, label: '复古漫画', emoji: '🎨' },
        { index: 1, label: '3D童话', emoji: '🧸' },
        { index: 2, label: '二次元', emoji: '✨' },
        { index: 3, label: '小清新', emoji: '🌿' },
        { index: 4, label: '未来科技', emoji: '🤖' },
        { index: 5, label: '国画古风', emoji: '🏮' },
        { index: 7, label: '炫彩卡通', emoji: '🌈' },
        { index: 30, label: '童话世界', emoji: '🏰' },
        { index: 31, label: '黏土世界', emoji: '🪆' },
        { index: 35, label: '3D世界', emoji: '🌐' },
        { index: 36, label: '二次元世界', emoji: '🌸' },
        { index: 38, label: '蜡笔世界', emoji: '🖍️' },
      ],
      sketchForm: { prompt: '' },
      sketchDrawing: false,
      sketchLastPos: null,
      inpaintForm: { prompt: '' },
      inpaintDrawing: false,
      inpaintLastPos: null,
      inpaintSize: { w: 512, h: 512 },
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
        { value: 'API-3', label: '模拟', icon: '🧪' },
        { value: 'API-4', label: '万象Pro', icon: '🌟' }
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
      await axios.get('/api/logout')
      localStorage.removeItem('user')
      this.$router.push('/')
    },
    async generateImage() {
      if (!this.generateForm.prompt) return
      this.isGenerating = true
      this.logs = []
      this.generatedImages = []
      console.log('[DEBUG] Sending api_choice:', this.generateForm.apiChoice)
      try {
        const response = await axios.post('/api/generate', {
          prompt: this.generateForm.prompt,
          api_choice: this.generateForm.apiChoice,
          negativePrompt: this.generateForm.negativePrompt,
          size: this.generateForm.size,
          count: parseInt(this.generateForm.count),
          seed: this.generateForm.seed || null
        })
        this.generatedImages = response.data.images || (response.data.image ? [response.data.image] : [])
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
          const img = new Image()
          img.onload = () => { this.inpaintSize = { w: img.width, h: img.height } }
          img.src = e.target.result
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
          const img = new Image()
          img.onload = () => { this.inpaintSize = { w: img.width, h: img.height } }
          img.src = e.target.result
        }
        reader.readAsDataURL(file)
      }
    },
    async editImage() {
      if (!this.uploadedImage) return
      this.isEditing = true
      this.logs = []
      try {
        const response = await axios.post('/api/edit', {
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
    },
    async generateBackground() {
      if (!this.uploadedImage) return
      this.isEditing = true
      this.logs = []
      this.editedImage = null
      try {
        const response = await axios.post('/api/background', {
          image: this.uploadedImage,
          prompt: this.bgForm.prompt
        })
        this.editedImage = response.data.image
        if (response.data.logs) this.logs = response.data.logs
      } catch (error) {
        alert('背景生成失败: ' + (error.response?.data?.error || error.message))
      } finally {
        this.isEditing = false
      }
    },
    async styleRepaint() {      if (!this.uploadedImage) return
      this.isEditing = true
      this.logs = []
      this.editedImage = null
      try {
        const response = await axios.post('/api/style-repaint', {
          image: this.uploadedImage,
          style_index: this.styleForm.styleIndex
        })
        this.editedImage = response.data.image
        if (response.data.logs) this.logs = response.data.logs
      } catch (error) {
        alert('风格重绘失败: ' + (error.response?.data?.error || error.message))
      } finally {
        this.isEditing = false
      }
    },
    sketchStart(e) {
      this.sketchDrawing = true
      const rect = this.$refs.sketchCanvas.getBoundingClientRect()
      this.sketchLastPos = { x: e.clientX - rect.left, y: e.clientY - rect.top }
    },
    sketchDraw(e) {
      if (!this.sketchDrawing) return
      const canvas = this.$refs.sketchCanvas
      const ctx = canvas.getContext('2d')
      const rect = canvas.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      ctx.strokeStyle = '#000'
      ctx.lineWidth = 3
      ctx.lineCap = 'round'
      ctx.beginPath()
      ctx.moveTo(this.sketchLastPos.x, this.sketchLastPos.y)
      ctx.lineTo(x, y)
      ctx.stroke()
      this.sketchLastPos = { x, y }
    },
    sketchEnd() {
      this.sketchDrawing = false
    },
    clearSketch() {
      const canvas = this.$refs.sketchCanvas
      canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
    },
    async submitSketch() {
      const canvas = this.$refs.sketchCanvas
      const imageData = canvas.toDataURL('image/png')
      this.isEditing = true
      this.logs = []
      this.editedImage = null
      try {
        const response = await axios.post('/api/sketch', {
          image: imageData,
          prompt: this.sketchForm.prompt
        })
        this.editedImage = response.data.image
        if (response.data.logs) this.logs = response.data.logs
      } catch (error) {
        alert('涂鸦生图失败: ' + (error.response?.data?.error || error.message))
      } finally {
        this.isEditing = false
      }
    },
    inpaintStart(e) {
      this.inpaintDrawing = true
      const rect = this.$refs.inpaintCanvas.getBoundingClientRect()
      const scaleX = this.inpaintSize.w / rect.width
      const scaleY = this.inpaintSize.h / rect.height
      this.inpaintLastPos = {
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY
      }
    },
    inpaintDraw(e) {
      if (!this.inpaintDrawing) return
      const canvas = this.$refs.inpaintCanvas
      const ctx = canvas.getContext('2d')
      const rect = canvas.getBoundingClientRect()
      const scaleX = this.inpaintSize.w / rect.width
      const scaleY = this.inpaintSize.h / rect.height
      const x = (e.clientX - rect.left) * scaleX
      const y = (e.clientY - rect.top) * scaleY
      ctx.strokeStyle = 'rgba(255,0,0,0.6)'
      ctx.lineWidth = 20
      ctx.lineCap = 'round'
      ctx.beginPath()
      ctx.moveTo(this.inpaintLastPos.x, this.inpaintLastPos.y)
      ctx.lineTo(x, y)
      ctx.stroke()
      this.inpaintLastPos = { x, y }
    },
    inpaintEnd() { this.inpaintDrawing = false },
    clearInpaint() {
      const c = this.$refs.inpaintCanvas
      c.getContext('2d').clearRect(0, 0, c.width, c.height)
    },
    async submitInpaint() {
      if (!this.uploadedImage) return
      // 生成白底黑色蒙版
      const canvas = this.$refs.inpaintCanvas
      const maskCanvas = document.createElement('canvas')
      maskCanvas.width = canvas.width
      maskCanvas.height = canvas.height
      const mCtx = maskCanvas.getContext('2d')
      mCtx.fillStyle = 'black'
      mCtx.fillRect(0, 0, maskCanvas.width, maskCanvas.height)
      // 将红色涂抹区域转为白色
      const src = canvas.getContext('2d', { willReadFrequently: true }).getImageData(0, 0, canvas.width, canvas.height)
      const dst = mCtx.getImageData(0, 0, maskCanvas.width, maskCanvas.height)
      for (let i = 0; i < src.data.length; i += 4) {
        if (src.data[i + 3] > 0) {
          dst.data[i] = 255; dst.data[i+1] = 255; dst.data[i+2] = 255; dst.data[i+3] = 255
        }
      }
      mCtx.putImageData(dst, 0, 0)
      const maskData = maskCanvas.toDataURL('image/png')
      this.isEditing = true
      this.logs = []
      this.editedImage = null
      try {
        const response = await axios.post('/api/inpaint', {
          image: this.uploadedImage,
          mask: maskData,
          prompt: this.inpaintForm.prompt
        })
        this.editedImage = response.data.image
        if (response.data.logs) this.logs = response.data.logs
      } catch (error) {
        alert('局部重绘失败: ' + (error.response?.data?.error || error.message))
      } finally {
        this.isEditing = false
      }
    }
  }
}
</script>

<style scoped>
.main-app {
  min-height: 100vh;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: all 0.3s;
}

.dark-theme {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.bg-shapes {
  position: fixed;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
}

.shape-1 {
  width: 800px;
  height: 800px;
  background: #764ba2;
  top: -300px;
  right: -200px;
  animation: float 25s infinite ease-in-out;
}

.shape-2 {
  width: 600px;
  height: 600px;
  background: #667eea;
  bottom: -200px;
  left: -200px;
  animation: float 30s infinite ease-in-out reverse;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(30px, -30px); }
}

.top-navbar {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 10;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.logo {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  color: white;
  letter-spacing: -0.5px;
}

.navbar-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.icon-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.icon-btn svg {
  width: 20px;
  height: 20px;
  color: white;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  color: white;
  font-weight: 500;
}

.logout-btn {
  width: 36px;
  height: 36px;
  background: rgba(255, 100, 100, 0.2);
  border: 1px solid rgba(255, 100, 100, 0.3);
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.logout-btn svg {
  width: 18px;
  height: 18px;
  color: #ff6b6b;
}

.logout-btn:hover {
  background: rgba(255, 100, 100, 0.3);
}

.main-container {
  display: flex;
  max-width: 1600px;
  margin: 20px auto;
  gap: 24px;
  padding: 0 24px 24px;
  position: relative;
  z-index: 1;
}

.sidebar {
  width: 380px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 24px;
  max-height: calc(100vh - 140px);
  overflow-y: auto;
}

.dark-theme .sidebar {
  background: rgba(0, 0, 0, 0.2);
}

.mode-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.mode-btn {
  flex: 1;
  padding: 14px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
}

.mode-btn svg {
  width: 18px;
  height: 18px;
}

.mode-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
}

.edit-sub-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.sub-tab-btn {
  flex: 1;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s;
}

.sub-tab-btn.active {
  background: rgba(102, 126, 234, 0.3);
  color: white;
  border-color: rgba(102, 126, 234, 0.5);
}

.params-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.panel-section label {
  font-weight: 600;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.panel-section textarea,
.panel-section select {
  width: 100%;
  padding: 14px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 14px;
  color: white;
  resize: vertical;
  transition: all 0.3s;
  box-sizing: border-box;
}

.panel-section textarea::placeholder,
.panel-section select::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.panel-section textarea:focus,
.panel-section select:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
}

.panel-section select option {
  background: #302b63;
  color: white;
}

.prompt-actions {
  display: flex;
  gap: 8px;
}

.small-btn {
  padding: 8px 14px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.small-btn svg {
  width: 14px;
  height: 14px;
}

.small-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.api-selector {
  display: flex;
  gap: 10px;
}

.radio-card {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.radio-card:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.4);
}

.radio-card.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
}

.radio-card input {
  display: none;
}

.api-icon {
  font-size: 18px;
}

.api-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  font-weight: 500;
}

.range-wrapper {
  padding: 0 8px;
}

.range-wrapper input[type="range"] {
  width: 100%;
  height: 6px;
  -webkit-appearance: none;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  outline: none;
}

.range-wrapper input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4);
}

.range-dots {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}

.range-dots span {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  transition: all 0.3s;
}

.range-dots span.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.generate-btn {
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
}

.generate-btn svg {
  width: 20px;
  height: 20px;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.upload-area {
  border: 2px dashed rgba(255, 255, 255, 0.3);
  border-radius: 14px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-area:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.upload-placeholder svg {
  width: 48px;
  height: 48px;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 12px;
}

.upload-placeholder p {
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.uploaded-preview {
  position: relative;
  width: 100%;
}

.uploaded-preview img {
  width: 100%;
  border-radius: 10px;
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 32px;
  height: 32px;
  background: rgba(255, 0, 0, 0.8);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn svg {
  width: 16px;
  height: 16px;
  color: white;
}

.content-area {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 30px;
  min-height: calc(100vh - 140px);
}

.dark-theme .content-area {
  background: rgba(0, 0, 0, 0.2);
}

.empty-state {
  text-align: center;
  padding: 100px 20px;
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin: 0 auto 24px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-icon svg {
  width: 60px;
  height: 60px;
  color: rgba(255, 255, 255, 0.5);
}

.empty-state h3 {
  font-size: 24px;
  color: white;
  margin-bottom: 10px;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.6);
}

.generating-state {
  text-align: center;
  padding: 100px 20px;
}

.generating-spinner {
  width: 80px;
  height: 80px;
  margin: 0 auto 24px;
  position: relative;
}

.spinner-ring {
  position: absolute;
  inset: 0;
  border: 3px solid transparent;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.spinner-ring:nth-child(2) {
  inset: 8px;
  border-top-color: #764ba2;
  animation-delay: -0.4s;
}

.spinner-ring:nth-child(3) {
  inset: 16px;
  border-top-color: #f093fb;
  animation-delay: -0.8s;
}

.generating-state p {
  color: rgba(255, 255, 255, 0.8);
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.image-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.image-card:hover {
  transform: translateY(-6px);
}

.image-card img {
  width: 100%;
  display: block;
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 20px;
  display: flex;
  gap: 12px;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-card:hover .image-overlay {
  opacity: 1;
}

.image-overlay button {
  width: 44px;
  height: 44px;
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.image-overlay button:hover {
  transform: scale(1.1);
}

.image-overlay button svg {
  width: 22px;
  height: 22px;
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
  color: white;
  margin-bottom: 16px;
}

.comparison-side img {
  width: 100%;
  max-width: 500px;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.logs-panel {
  margin-top: 24px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 14px;
  padding: 16px;
}

.logs-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 600;
}

.logs-header button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.logs-header button svg {
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.6);
}

.logs-content {
  max-height: 180px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.modal-content {
  background: linear-gradient(135deg, #302b63 0%, #24243e 100%);
  border-radius: 20px;
  padding: 30px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-content h3 {
  color: white;
  margin: 0 0 20px;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.close-btn svg {
  width: 24px;
  height: 24px;
  color: rgba(255, 255, 255, 0.6);
}

.template-card {
  padding: 16px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.template-card:hover {
  background: rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.template-card h4 {
  color: white;
  margin: 0 0 8px;
}

.template-card p {
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  font-size: 14px;
}

.style-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.style-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.style-card:hover {
  background: rgba(255, 255, 255, 0.15);
}

.style-card.active {
  background: rgba(102, 126, 234, 0.35);
  border-color: rgba(102, 126, 234, 0.7);
}

.style-emoji {
  font-size: 22px;
}

.style-name {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.85);
}

.panel-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: rgba(102, 126, 234, 0.15);
  border-radius: 10px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
}

.panel-tip svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: #667eea;
}

.sketch-canvas-wrap {
  position: relative;
  display: inline-block;
  width: 100%;
  min-height: 320px;
}

.sketch-canvas {
  width: 100%;
  height: 320px;
  background: white;
  border-radius: 12px;
  cursor: crosshair;
  display: block;
}

.sketch-clear-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 6px 12px;
  background: rgba(255, 100, 100, 0.8);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
}

.sketch-clear-btn:hover {
  background: rgba(255, 60, 60, 0.9);
}

.inpaint-bg-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 12px;
  pointer-events: none;
}

.inpaint-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  cursor: crosshair;
  border-radius: 12px;
}

.preview-img {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
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