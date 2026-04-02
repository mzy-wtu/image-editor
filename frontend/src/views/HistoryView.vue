<template>
  <div class="history-page">
    <div class="history-header">
      <h2>我的图像历史</h2>
      <div class="header-actions">
        <button class="btn-back" @click="goBack">返回主页</button>
        <button class="btn-logout" @click="logout">注销</button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else-if="!records || records.length === 0" class="empty">
      <p>暂无图像记录</p>
      <p class="tip">去主页生成一些图像吧！</p>
    </div>
    
    <div v-else class="history-list">
      <div v-for="record in records" :key="record.id" class="history-item">
        <div class="image-box">
          <img :src="record.result_image" alt="生成的图像" />
        </div>
        <div class="image-info">
          <div class="info-row">
            <span class="label">类型：</span>
            <span class="value">{{ record.image_type === 'generate' ? '文生图' : '图像编辑' }}</span>
          </div>
          <div class="info-row">
            <span class="label">API：</span>
            <span class="value">{{ record.api_choice }}</span>
          </div>
          <div class="info-row">
            <span class="label">提示词：</span>
            <span class="value prompt">{{ record.prompt || '无' }}</span>
          </div>
          <div class="info-row">
            <span class="label">时间：</span>
            <span class="value">{{ record.created_at }}</span>
          </div>
          <div class="action-btns">
            <button class="btn-download" @click="downloadImage(record)">下载</button>
            <button class="btn-delete" @click="deleteRecord(record.id)">删除</button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">上一页</button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">下一页</button>
    </div>
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
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.history-header h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.btn-back, .btn-logout {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-back {
  background: #2196F3;
  color: white;
}

.btn-logout {
  background: #f44336;
  color: white;
}

.loading, .empty {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.empty .tip {
  font-size: 14px;
  color: #999;
  margin-top: 10px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.history-item {
  display: flex;
  gap: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
}

.image-box {
  width: 200px;
  height: 200px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

.image-box img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.image-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-row {
  display: flex;
  font-size: 14px;
}

.info-row .label {
  font-weight: bold;
  width: 70px;
  flex-shrink: 0;
}

.info-row .value {
  flex: 1;
}

.info-row .prompt {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 400px;
}

.action-btns {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn-download, .btn-delete {
  padding: 6px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-download {
  background: #4CAF50;
  color: white;
}

.btn-delete {
  background: #f44336;
  color: white;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 30px;
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
  border-radius: 4px;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
}
</style>
