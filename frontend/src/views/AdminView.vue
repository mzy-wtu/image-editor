<template>
  <div class="admin-page">
    <header class="top-navbar">
      <div class="navbar-left">
        <div class="logo-icon">
          <AppIcon name="admin" size="20" />
        </div>
        <h1 class="page-title">用户管理</h1>
      </div>
      <div class="navbar-right">
        <button class="nav-btn" @click="$router.push('/main')">
          <AppIcon name="home" size="16" />返回主页
        </button>
        <button class="nav-btn logout" @click="logout">
          <AppIcon name="logout" size="16" />注销
        </button>
      </div>
    </header>

    <main class="main-content">
      <div class="stats-bar">
        <div class="stat-card">
          <div class="stat-icon">
            <AppIcon name="user" size="24" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ users.length }}</span>
            <span class="stat-label">总用户数</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon accent">
            <AppIcon name="check" size="24" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ activeCount }}</span>
            <span class="stat-label">活跃用户</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon warning">
            <AppIcon name="ban" size="24" />
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ users.length - activeCount }}</span>
            <span class="stat-label">已禁用</span>
          </div>
        </div>
      </div>

      <div class="table-container">
        <div v-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>
        <div v-else-if="error" class="error-state">
          <AppIcon name="alert" size="48" />
          <p>{{ error }}</p>
          <button @click="loadUsers">重试</button>
        </div>
        <table v-else class="user-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>邮箱</th>
              <th>角色</th>
              <th>状态</th>
              <th>注册时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td class="id-cell">{{ user.id }}</td>
              <td class="username-cell">
                <div class="avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
                {{ user.username }}
              </td>
              <td>{{ user.email || '-' }}</td>
              <td>
                <span :class="['role-badge', user.is_admin ? 'admin' : 'user']">
                  {{ user.is_admin ? '管理员' : '用户' }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                  <span class="status-dot"></span>
                  {{ user.is_active ? '活跃' : '禁用' }}
                </span>
              </td>
              <td class="time-cell">{{ user.created_at }}</td>
              <td>
                <div class="action-buttons">
                  <button class="action-btn history" @click="viewUserHistory(user)">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    历史
                  </button>
                  <button
                    v-if="!user.is_admin"
                    :class="['action-btn', user.is_active ? 'disable' : 'enable']"
                    @click="toggleUserStatus(user.id, !user.is_active)"
                    :disabled="isUpdating === user.id"
                  >
                    <svg v-if="isUpdating === user.id" class="spinning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                      <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14">
                      <circle cx="12" cy="12" r="10"/>
                      <polyline v-if="user.is_active" points="4.93 4.93 19.07 19.07"/>
                      <path v-else d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                      <polyline v-if="!user.is_active" points="22 4 12 14.01 9 11.01"/>
                    </svg>
                    {{ isUpdating === user.id ? '处理中' : (user.is_active ? '禁用' : '启用') }}
                  </button>
                  <span v-else class="no-action">无法操作</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <div v-if="showHistoryModal" class="modal-overlay" @click.self="closeHistoryModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ selectedUser?.username }} - 图像生成历史</h2>
          <button class="modal-close" @click="closeHistoryModal">
            <AppIcon name="close" size="20" />
          </button>
        </div>
        <div class="modal-body">
          <div v-if="historyLoading" class="loading-state">
            <div class="spinner"></div>
            <p>加载中...</p>
          </div>
          <div v-else-if="historyError" class="error-state">
            <p>{{ historyError }}</p>
          </div>
          <div v-else-if="userImages.length === 0" class="empty-state">
            <AppIcon name="image" size="48" />
            <p>暂无图像生成记录</p>
          </div>
          <div v-else class="image-grid">
            <div v-for="img in userImages" :key="img.id" class="image-card">
              <div class="image-preview" @click="previewImage(img.result_image)">
                <img v-if="img.result_image" :src="img.result_image" alt="生成图像" />
                <div v-else class="no-image">无图像</div>
              </div>
              <div class="image-info">
                <div class="image-type">{{ getImageTypeName(img.image_type) }}</div>
                <div class="image-prompt">{{ img.prompt || '无提示词' }}</div>
                <div class="image-meta">
                  <span>{{ img.api_choice }}</span>
                  <span>{{ img.size }}</span>
                </div>
                <div class="image-time">{{ img.created_at }}</div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="totalPages > 1" class="modal-footer">
          <button class="page-btn" :disabled="currentPage <= 1" @click="changePage(currentPage - 1)">上一页</button>
          <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
          <button class="page-btn" :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)">下一页</button>
        </div>
      </div>
    </div>

    <div v-if="previewImageUrl" class="preview-overlay" @click="previewImageUrl = null">
      <img :src="previewImageUrl" class="preview-image" />
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AppIcon from '../components/common/AppIcon.vue'
import { useToast } from '../components/common/Toast.vue'

export default {
  name: 'AdminView',
  components: { AppIcon },
  data() {
    return {
      user: null,
      users: [],
      isLoading: false,
      error: '',
      isUpdating: null,
      showHistoryModal: false,
      selectedUser: null,
      userImages: [],
      historyLoading: false,
      historyError: '',
      currentPage: 1,
      totalPages: 1,
      previewImageUrl: null
    }
  },
  computed: {
    activeCount() {
      return this.users.filter(u => u.is_active).length
    }
  },
  mounted() {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      this.user = JSON.parse(userStr)
      if (!this.user.is_admin) {
        this.$router.push('/main')
      } else {
        this.loadUsers()
      }
    } else {
      this.$router.push('/')
    }
  },
  setup() {
    const { show: toast } = useToast()
    return { toast }
  },
  methods: {
    async logout() {
      try {
        await axios.get('/api/logout')
        localStorage.removeItem('user')
        this.$router.push('/')
      } catch (error) {
        console.error('Logout error:', error)
      }
    },
    async loadUsers() {
      this.isLoading = true
      this.error = ''
      try {
        const response = await axios.get('/api/admin/users')
        this.users = response.data.users
      } catch (error) {
        console.error('Load users error:', error)
        this.error = '加载用户列表失败，请稍后重试'
      } finally {
        this.isLoading = false
      }
    },
    async toggleUserStatus(userId, isActive) {
      this.isUpdating = userId
      try {
        await axios.put(`/api/admin/users/${userId}`, { is_active: isActive })
        this.loadUsers()
      } catch (error) {
        console.error('Toggle user status error:', error)
        this.toast('操作失败，请稍后重试', 'error')
      } finally {
        this.isUpdating = null
      }
    },
    async viewUserHistory(user) {
      this.selectedUser = user
      this.showHistoryModal = true
      this.currentPage = 1
      await this.loadUserImages()
    },
    async loadUserImages() {
      if (!this.selectedUser) return
      this.historyLoading = true
      this.historyError = ''
      try {
        const response = await axios.get(`/api/admin/users/${this.selectedUser.id}/images`, {
          params: { page: this.currentPage, per_page: 12 }
        })
        this.userImages = response.data.images
        this.totalPages = response.data.pages
      } catch (error) {
        console.error('Load user images error:', error)
        this.historyError = '加载历史记录失败，请稍后重试'
      } finally {
        this.historyLoading = false
      }
    },
    closeHistoryModal() {
      this.showHistoryModal = false
      this.selectedUser = null
      this.userImages = []
      this.currentPage = 1
    },
    async changePage(page) {
      this.currentPage = page
      await this.loadUserImages()
    },
    getImageTypeName(type) {
      const types = {
        'generate': '文生图',
        'edit': '指令编辑',
        'inpaint': '局部重绘',
        'background': '背景生成',
        'style-repaint': '风格重绘',
        'sketch': '涂鸦作画'
      }
      return types[type] || type
    },
    previewImage(url) {
      this.previewImageUrl = url
    }
  }
}
</script>

<style scoped>
.admin-page {
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 28px 24px;
}

.stats-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: var(--accent-light);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.stat-icon.accent {
  background: var(--success-bg);
  color: #16a34a;
}

.stat-icon.warning {
  background: var(--danger-bg);
  color: var(--danger);
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: var(--text-muted);
}

.table-container {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.loading-state,
.error-state {
  padding: 60px;
  text-align: center;
  color: var(--text-muted);
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state button {
  margin-top: 14px;
  padding: 8px 18px;
  background: var(--accent);
  border: none;
  border-radius: var(--radius-sm);
  color: white;
  cursor: pointer;
  font-size: 13px;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th {
  padding: 12px 18px;
  text-align: left;
  font-weight: 600;
  font-size: 12px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border);
}

.user-table td {
  padding: 14px 18px;
  text-align: left;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-primary);
  font-size: 14px;
}

.user-table tr:hover td {
  background: var(--bg-secondary);
}

.user-table tr:last-child td {
  border-bottom: none;
}

.id-cell {
  color: var(--text-muted);
  font-size: 13px;
}

.username-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;
}

.avatar {
  width: 32px;
  height: 32px;
  background: var(--accent);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  color: white;
}

.role-badge {
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.admin {
  background: #fef0e0;
  color: #c98d5f;
}

.role-badge.user {
  background: var(--accent-light);
  color: var(--accent);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background: var(--success-bg);
  color: #16a34a;
}

.status-badge.inactive {
  background: var(--danger-bg);
  color: var(--danger);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.time-cell {
  color: var(--text-muted);
  font-size: 13px;
}

.action-buttons {
  display: flex;
  gap: 6px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all var(--transition);
}

.action-btn.history {
  background: var(--accent-light);
  color: var(--accent);
}

.action-btn.history:hover {
  background: var(--accent-subtle);
}

.action-btn.enable {
  background: var(--success-bg);
  color: #16a34a;
}

.action-btn.enable:hover {
  background: #dcfce7;
}

.action-btn.disable {
  background: var(--danger-bg);
  color: var(--danger);
}

.action-btn.disable:hover {
  background: #fee2e2;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinning {
  animation: spin 0.8s linear infinite;
}

.no-action {
  color: var(--text-muted);
  font-size: 12px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 880px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-lg);
}

.modal-header {
  padding: 18px 22px;
  border-bottom: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 18px;
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  color: var(--text-muted);
  transition: color var(--transition);
}

.modal-close:hover {
  color: var(--text-primary);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 18px 22px;
}

.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: var(--text-muted);
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 14px;
}

.image-card {
  background: var(--bg-secondary);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
}

.image-preview {
  aspect-ratio: 1;
  background: var(--bg-tertiary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--transition);
}

.image-preview:hover img {
  transform: scale(1.05);
}

.no-image {
  color: var(--text-muted);
  font-size: 13px;
}

.image-info {
  padding: 10px;
}

.image-type {
  font-size: 11px;
  color: var(--accent);
  font-weight: 600;
  margin-bottom: 3px;
}

.image-prompt {
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 6px;
}

.image-meta {
  display: flex;
  gap: 6px;
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 3px;
}

.image-time {
  font-size: 11px;
  color: var(--text-muted);
}

.modal-footer {
  padding: 14px 22px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 14px;
}

.page-btn {
  padding: 7px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 13px;
  transition: all var(--transition);
}

.page-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  color: var(--text-muted);
  font-size: 13px;
}

.preview-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  cursor: pointer;
}

.preview-image {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
  border-radius: var(--radius);
}

@media (max-width: 768px) {
  .stats-bar {
    grid-template-columns: 1fr;
  }

  .user-table th,
  .user-table td {
    padding: 10px;
    font-size: 13px;
  }
}
</style>
