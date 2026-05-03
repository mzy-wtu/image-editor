<template>
  <div class="history-page">
    <header class="top-navbar">
      <div class="navbar-left">
        <div class="logo-icon">
          <AppIcon name="history" size="20" />
        </div>
        <h1 class="page-title">图像历史</h1>
      </div>
      <div class="navbar-right">
        <button class="nav-btn" @click="goBack">
          <AppIcon name="home" size="16" />返回主页
        </button>
        <button class="nav-btn logout" @click="logout">
          <AppIcon name="logout" size="16" />注销
        </button>
      </div>
    </header>

    <main class="main-content">
      <LoadingSpinner v-if="loading" text="加载中..." />

      <EmptyState
        v-else-if="!records.length"
        icon="image" title="暂无图像记录" description="去主页生成一些图像吧！"
        action-text="开始创作" @action="goBack"
      />

      <div v-else class="history-list">
        <div v-for="record in records" :key="record.id" class="history-card">
          <div class="image-section">
            <img :src="record.result_image" alt="生成的图像" loading="lazy" />
            <span class="image-type-badge">{{ record.image_type === 'generate' ? '文生图' : '编辑' }}</span>
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
                <AppIcon name="download" size="14" />下载
              </button>
              <button class="action-btn delete" @click="deleteRecord(record.id)">
                <AppIcon name="delete" size="14" />删除
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">
          <AppIcon name="chevron-left" size="16" />上一页
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">
          下一页<AppIcon name="chevron-right" size="16" />
        </button>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import AppIcon from '../components/common/AppIcon.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import EmptyState from '../components/common/EmptyState.vue'
import { useToast } from '../components/common/Toast.vue'

export default {
  name: 'HistoryView',
  components: { AppIcon, LoadingSpinner, EmptyState },
  setup() {
    const router = useRouter()
    const records = ref([])
    const loading = ref(true)
    const currentPage = ref(1)
    const totalPages = ref(1)
    const perPage = 10
    const { show: toast } = useToast()

    const loadHistory = async (page = 1) => {
      loading.value = true
      try {
        const res = await axios.get(`/api/history?page=${page}&per_page=${perPage}`)
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

    const changePage = (page) => loadHistory(page)
    const goBack = () => router.push('/main')
    const logout = async () => {
      try { await axios.get('/api/logout') } catch (e) {}
      router.push('/')
    }
    const downloadImage = (record) => {
      const link = document.createElement('a')
      link.href = record.result_image
      link.download = `image_${record.id}.png`
      link.click()
    }
    const deleteRecord = async (id) => {
      if (!confirm('确定删除此记录？')) return
      try {
        await axios.delete(`/api/history/${id}`)
        toast('删除成功', 'success')
        loadHistory(currentPage.value)
      } catch (e) {
        toast('删除失败', 'error')
      }
    }

    onMounted(() => loadHistory())

    return { records, loading, currentPage, totalPages, changePage, goBack, logout, downloadImage, deleteRecord }
  }
}
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  background: var(--bg-secondary);
}

.logo-icon {
  width: 36px;
  height: 36px;
  background: var(--accent);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.page-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0;
  color: var(--text-primary);
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.navbar-right {
  display: flex;
  gap: 8px;
}

.main-content {
  max-width: 960px;
  margin: 0 auto;
  padding: 28px 24px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-card {
  display: flex;
  gap: 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: box-shadow var(--transition);
}

.history-card:hover {
  box-shadow: var(--shadow-md);
}

.image-section {
  width: 200px;
  flex-shrink: 0;
  position: relative;
  background: var(--bg-tertiary);
}

.image-section img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.image-type-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 10px;
  background: rgba(0, 0, 0, 0.55);
  border-radius: 6px;
  font-size: 12px;
  color: white;
}

.info-section {
  flex: 1;
  padding: 18px 18px 18px 0;
  display: flex;
  flex-direction: column;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
  flex: 1;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.info-item.full-width {
  grid-column: span 2;
}

.info-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.info-value {
  font-size: 14px;
  color: var(--text-primary);
}

.info-value.prompt {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-actions {
  display: flex;
  gap: 10px;
  margin-top: 14px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all var(--transition);
  background: var(--bg-primary);
}

.action-btn.download {
  color: var(--accent);
  border-color: var(--accent-subtle);
}

.action-btn.download:hover {
  background: var(--accent-light);
}

.action-btn.delete {
  color: var(--danger);
  border-color: var(--danger-border);
}

.action-btn.delete:hover {
  background: var(--danger-bg);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 18px;
  margin-top: 32px;
}

.pagination button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
  transition: all var(--transition);
}

.pagination button:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.pagination button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  color: var(--text-muted);
  font-size: 13px;
}

@media (max-width: 768px) {
  .history-card {
    flex-direction: column;
  }
  .image-section {
    width: 100%;
  }
  .image-section img {
    height: 180px;
  }
  .info-section {
    padding: 14px;
  }
  .info-grid {
    grid-template-columns: 1fr;
  }
  .info-item.full-width {
    grid-column: span 1;
  }
}
</style>
