<template>
  <div class="app">
    <div class="header">
      <h1>图像编辑系统 - 用户管理</h1>
      <div class="user-info">
        <span>欢迎，{{ user?.username }}</span>
        <button class="btn" @click="$router.push('/main')">
          返回主页面
        </button>
        <button class="btn logout-btn" @click="logout">
          注销
        </button>
      </div>
    </div>
    
    <div class="container">
      <div class="admin-container">
        <h2>用户列表</h2>
        <div v-if="isLoading">
          <p>加载中...</p>
        </div>
        <div v-else-if="error">
          <p class="error-message">{{ error }}</p>
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
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email || '-' }}</td>
              <td>{{ user.is_admin ? '管理员' : '普通用户' }}</td>
              <td>
                <span :class="['status-badge', user.is_active ? 'status-active' : 'status-inactive']">
                  {{ user.is_active ? '活跃' : '禁用' }}
                </span>
              </td>
              <td>{{ user.created_at }}</td>
              <td>
                <div class="action-buttons">
                  <button 
                    v-if="!user.is_admin"
                    :class="['btn', user.is_active ? 'btn-danger' : 'btn-primary']" 
                    @click="toggleUserStatus(user.id, !user.is_active)"
                    :disabled="isUpdating === user.id"
                  >
                    {{ isUpdating === user.id ? '处理中...' : (user.is_active ? '禁用' : '启用') }}
                  </button>
                  <span v-else>无法操作</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
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
  mounted() {
    // 从localStorage获取用户信息
    const userStr = localStorage.getItem('user')
    if (userStr) {
      this.user = JSON.parse(userStr)
      // 检查是否是管理员
      if (!this.user.is_admin) {
        // 非管理员，跳转到主页面
        this.$router.push('/main')
      } else {
        // 加载用户列表
        this.loadUsers()
      }
    } else {
      // 未登录，跳转到登录页面
      this.$router.push('/')
    }
  },
  methods: {
    async logout() {
      try {
        await axios.get('http://localhost:5000/api/logout')
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
        const response = await axios.get('http://localhost:5000/api/admin/users')
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
        await axios.put(`http://localhost:5000/api/admin/users/${userId}`, {
          is_active: isActive
        })
        // 重新加载用户列表
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
.app {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.header {
  background-color: #333;
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 20px;
}

.header .user-info {
  display: flex;
  align-items: center;
}

.header .user-info span {
  margin-right: 15px;
}

.header .btn {
  padding: 5px 10px;
  font-size: 14px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px;
}

.header .btn:hover {
  background-color: #45a049;
}

.header .logout-btn {
  background-color: #f44336;
}

.header .logout-btn:hover {
  background-color: #d32f2f;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px 20px;
}

.admin-container {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.admin-container h2 {
  margin-bottom: 20px;
  color: #333;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th, .user-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.user-table th {
  background-color: #f2f2f2;
  font-weight: bold;
}

.user-table tr:hover {
  background-color: #f5f5f5;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
}

.status-active {
  background-color: #e8f5e8;
  color: #2e7d32;
}

.status-inactive {
  background-color: #ffebee;
  color: #c62828;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.action-buttons button {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background-color: #2196F3;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1976D2;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background-color: #d32f2f;
}

.btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #c62828;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .user-table {
    font-size: 14px;
  }
  
  .user-table th, .user-table td {
    padding: 8px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons button {
    margin-bottom: 5px;
  }
}
</style>