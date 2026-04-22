<template>
  <div class="admin-page">
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
    </div>
    
    <header class="top-navbar">
      <div class="navbar-left">
        <div class="logo-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
            <circle cx="9" cy="7" r="4"/>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
          </svg>
        </div>
        <h1 class="page-title">用户管理</h1>
      </div>
      <div class="navbar-right">
        <button class="nav-btn" @click="$router.push('/main')">
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
      <div class="stats-bar">
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ users.length }}</span>
            <span class="stat-label">总用户数</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon active">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ activeCount }}</span>
            <span class="stat-label">活跃用户</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon warning">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
            </svg>
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
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
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
                  <button 
                    v-if="!user.is_admin"
                    :class="['action-btn', user.is_active ? 'disable' : 'enable']"
                    @click="toggleUserStatus(user.id, !user.is_active)"
                    :disabled="isUpdating === user.id"
                  >
                    <svg v-if="isUpdating === user.id" class="spinning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AdminView',
  data() {
    return {
      user: null,
      users: [],
      isLoading: false,
      error: '',
      isUpdating: null
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
        await axios.put(`/api/admin/users/${userId}`, {
          is_active: isActive
        })
        this.loadUsers()
      } catch (error) {
        console.error('Toggle user status error:', error)
        alert('操作失败，请稍后重试')
      } finally {
        this.isUpdating = null
      }
    }
  }
}
</script>

<style scoped>
.admin-page {
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
  top: -200px;
  right: -100px;
}

.shape-2 {
  width: 500px;
  height: 500px;
  background: #667eea;
  bottom: -150px;
  left: -100px;
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  position: relative;
  z-index: 1;
}

.stats-bar {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon {
  width: 56px;
  height: 56px;
  background: rgba(102, 126, 234, 0.2);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon svg {
  width: 28px;
  height: 28px;
  color: #667eea;
}

.stat-icon.active {
  background: rgba(34, 197, 94, 0.2);
}

.stat-icon.active svg {
  color: #22c55e;
}

.stat-icon.warning {
  background: rgba(239, 68, 68, 0.2);
}

.stat-icon.warning svg {
  color: #ef4444;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: white;
}

.stat-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
}

.table-container {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.loading-state,
.error-state {
  padding: 60px;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state svg {
  width: 48px;
  height: 48px;
  color: #ef4444;
  margin-bottom: 16px;
}

.error-state button {
  margin-top: 16px;
  padding: 10px 20px;
  background: #667eea;
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th {
  padding: 16px 20px;
  text-align: left;
  font-weight: 600;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: rgba(0, 0, 0, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.user-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.9);
}

.user-table tr:hover td {
  background: rgba(255, 255, 255, 0.03);
}

.user-table tr:last-child td {
  border-bottom: none;
}

.id-cell {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
}

.username-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
}

.avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.role-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.admin {
  background: rgba(168, 85, 247, 0.2);
  color: #a855f7;
}

.role-badge.user {
  background: rgba(59, 130, 246, 0.2);
  color: #3b82f6;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.status-badge.inactive {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.time-cell {
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
}

.action-buttons {
  display: flex;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.action-btn.enable {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.action-btn.enable:hover {
  background: rgba(34, 197, 94, 0.3);
}

.action-btn.disable {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.action-btn.disable:hover {
  background: rgba(239, 68, 68, 0.3);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinning {
  animation: spin 1s linear infinite;
}

.no-action {
  color: rgba(255, 255, 255, 0.3);
  font-size: 13px;
}

@media (max-width: 768px) {
  .stats-bar {
    grid-template-columns: 1fr;
  }
  
  .user-table {
    font-size: 14px;
  }
  
  .user-table th,
  .user-table td {
    padding: 12px;
  }
}
</style>