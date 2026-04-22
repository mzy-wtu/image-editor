<template>
  <div class="history-page">
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
    </div>
    
    <header class="top-navbar">
      <div class="navbar-left">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polyline points="12 6 12 12 16 14"/>
          </svg>
        </div>
        <h1 class="page-title">图像历史</h1>
      </div>
      <div class="navbar-right">
        <button class="nav-btn" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
          返回主页
        </button>
        <button class="nav-btn logout" @click="logout">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          注销
        </button>
      </div>
    </header>
    
    <main class="main-content">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="!records || records.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
        </div>
        <h3>暂无图像记录</h3>
        <p>去主页生成一些图像吧！</p>
        <button @click="goBack">开始创作</button>
      </div>
      
      <div v-else class="history-list">
        <div v-for="record in records" :key="record.id" class="history-card">
          <div class="image-section">
            <img :src="record.result_image" alt="生成的图像" />
            <div class="image-type-badge">
              {{ record.image_type === 'generate' ? '文生图' : '编辑' }}
            </div>
          </div>
          <div class="info-section">
            <div class="info-grid">
              <div class="info-item">
                <span class="info-label">API</span>
                <span class="info-value">{{ record.api_choice }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">尺寸</span>
                <span class="info-value">{{ record.size || '默认' }}</span>
              </div>
              <div class="info-item full-width">
                <span class="info-label">提示词</span>
                <span class="info-value prompt">{{ record.prompt || '无' }}</span>
              </div>
              <div class="info-item full-width">
                <span class="info-label">时间</span>
                <span class="info-value">{{ record.created_at }}</span>
              </div>
            </div>
            <div class="card-actions">
              <button class="action-btn download" @click="downloadImage(record)">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7 10 12 15 17 10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                下载
              </button>
              <button class="action-btn delete" @click="deleteRecord(record.id)">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"/>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                </svg>
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
          上一页
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">
          下一页
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"/>
          </svg>
        </button>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'HistoryView',
  setup() {
    const router = useRouter()
    const records = ref([])
    const loading = ref(true)
    const currentPage = ref(1)
    const totalPages = ref(1)
    const perPage = 10
    
    const loadHistory = async (page = 1) => {
      loading.value = true
      try {
        const res = await axios.get('/api/history?page=' + page + '&per_page=' + perPage)
        records.value = res.data.records || []
        currentPage.value = res.data.current_page || 1
        totalPages.value = res.data.pages || 1
      } catch (err) {
        console.error('加载历史失败:', err)
        records.value = []
      } finally {
        loading.value = false
      }
    }
    
    const changePage = (page) => {
      loadHistory(page)
    }
    
    const goBack = () => {
      router.push('/main')
    }
    
    const logout = async () => {
      try {
        await axios.get('/api/logout')
      } catch (e) {}
      router.push('/')
    }
    
    const downloadImage = (record) => {
      const link = document.createElement('a')
      link.href = record.result_image
      link.download = 'image_' + record.id + '.png'
      link.click()
    }
    
    const deleteRecord = async (id) => {
      if (!confirm('确定删除此记录？')) return
      try {
        await axios.delete('/api/history/' + id)
        loadHistory(currentPage.value)
      } catch (e) {
        alert('删除失败')
      }
    }
    
    onMounted(() => {
      loadHistory()
    })
    
    return {
      records,
      loading,
      currentPage,
      totalPages,
      changePage,
      goBack,
      logout,
      downloadImage,
      deleteRecord
    }
  }
}
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  position: relative;
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
  opacity: 0.3;
}

.shape-1 {
  width: 600px;
  height: 600px;
  background: #764ba2;
  bottom: -200px;
  left: -100px;
}

.shape-2 {
  width: 500px;
  height: 500px;
  background: #667eea;
  top: -150px;
  right: -100px;
}

.top-navbar {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  padding: 16px 30px;
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
  width: 22px;
  height: 22px;
  color: white;
}

.page-title {
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.navbar-right {
  display: flex;
  gap: 12px;
}

.nav-btn {
  padding: 10px 18px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.nav-btn svg {
  width: 18px;
  height: 18px;
}

.nav-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.nav-btn.logout {
  background: rgba(255, 100, 100, 0.15);
  border-color: rgba(255, 100, 100, 0.3);
  color: #ff6b6b;
}

.nav-btn.logout:hover {
  background: rgba(255, 100, 100, 0.25);
}

.main-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px;
  position: relative;
  z-index: 1;
}

.loading-state {
  text-align: center;
  padding: 100px 20px;
  color: rgba(255, 255, 255, 0.6);
}

.spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  margin: 0 auto 24px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
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
  color: rgba(255, 255, 255, 0.4);
}

.empty-state h3 {
  font-size: 24px;
  color: white;
  margin-bottom: 10px;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 24px;
}

.empty-state button {
  padding: 14px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.empty-state button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.history-card {
  display: flex;
  gap: 20px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  transition: all 0.3s;
}

.history-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.image-section {
  width: 220px;
  flex-shrink: 0;
  position: relative;
}

.image-section img {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.image-type-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  font-size: 12px;
  color: white;
}

.info-section {
  flex: 1;
  padding: 20px 20px 20px 0;
  display: flex;
  flex-direction: column;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  flex: 1;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item.full-width {
  grid-column: span 2;
}

.info-label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.info-value.prompt {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn.download {
  background: rgba(102, 126, 234, 0.2);
  color: #667eea;
}

.action-btn.download:hover {
  background: rgba(102, 126, 234, 0.3);
}

.action-btn.delete {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.action-btn.delete:hover {
  background: rgba(239, 68, 68, 0.3);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.pagination button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  transition: all 0.3s;
}

.pagination button svg {
  width: 18px;
  height: 18px;
}

.pagination button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  color: rgba(255, 255, 255, 0.7);
  font-size: 14px;
}

@media (max-width: 768px) {
  .history-card {
    flex-direction: column;
  }
  
  .image-section img {
    height: 200px;
  }
  
  .info-section {
    padding: 16px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .info-item.full-width {
    grid-column: span 1;
  }
}
</style>