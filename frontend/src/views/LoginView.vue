<template>
  <div class="container">
    <div class="form-container">
      <h1>图像编辑系统</h1>
      
      <div class="form-tabs">
        <button 
          :class="{ active: activeTab === 'login' }" 
          @click="activeTab = 'login'"
        >
          登录
        </button>
        <button 
          :class="{ active: activeTab === 'register' }" 
          @click="activeTab = 'register'"
        >
          注册
        </button>
      </div>
      
      <!-- 登录表单 -->
      <form v-if="activeTab === 'login'" @submit.prevent="login">
        <div class="form-group">
          <label for="login-username">用户名</label>
          <input type="text" id="login-username" v-model="loginForm.username" required>
        </div>
        <div class="form-group">
          <label for="login-password">密码</label>
          <input type="password" id="login-password" v-model="loginForm.password" required>
        </div>
        <button type="submit" class="btn" :disabled="isLoading">
          {{ isLoading ? '登录中...' : '登录' }}
        </button>
        <div v-if="message" :class="['message', messageType]">
          {{ message }}
        </div>
      </form>
      
      <!-- 注册表单 -->
      <form v-else @submit.prevent="register">
        <div class="form-group">
          <label for="register-username">用户名</label>
          <input type="text" id="register-username" v-model="registerForm.username" required>
        </div>
        <div class="form-group">
          <label for="register-password">密码</label>
          <input type="password" id="register-password" v-model="registerForm.password" required>
        </div>
        <div class="form-group">
          <label for="register-email">邮箱 (可选)</label>
          <input type="email" id="register-email" v-model="registerForm.email">
        </div>
        <button type="submit" class="btn" :disabled="isLoading">
          {{ isLoading ? '注册中...' : '注册' }}
        </button>
        <div v-if="message" :class="['message', messageType]">
          {{ message }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LoginView',
  data() {
    return {
      activeTab: 'login',
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        email: ''
      },
      isLoading: false,
      message: '',
      messageType: ''
    }
  },
  methods: {
    async login() {
      this.isLoading = true
      this.message = ''
      
      try {
        const response = await axios.post('http://47.121.190.137:5000/api/login', this.loginForm, {
          withCredentials: true
        })
        this.message = response.data.message
        this.messageType = 'success'
        
        // 保存用户信息到localStorage
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
        // 跳转到主页面
        setTimeout(() => {
          this.$router.push('/main')
        }, 1000)
      } catch (error) {
        this.message = error.response?.data?.error || '登录失败，请稍后重试'
        this.messageType = 'error'
      } finally {
        this.isLoading = false
      }
    },
    async register() {
      this.isLoading = true
      this.message = ''
      
      try {
        const response = await axios.post('http://47.121.190.137:5000/api/register', this.registerForm, {
          withCredentials: true
        })
        this.message = response.data.message
        this.messageType = 'success'
        
        // 注册成功后切换到登录表单
        setTimeout(() => {
          this.activeTab = 'login'
        }, 1000)
      } catch (error) {
        this.message = error.response?.data?.error || '注册失败，请稍后重试'
        this.messageType = 'error'
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.form-container {
  max-width: 400px;
  margin: 100px auto;
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-container h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.form-tabs button {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.form-tabs button.active {
  color: #333;
  border-bottom: 2px solid #4CAF50;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.btn {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.btn:hover:not(:disabled) {
  background-color: #45a049;
}

.btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.message.error {
  background-color: #ffebee;
  color: #c62828;
}

.message.success {
  background-color: #e8f5e8;
  color: #2e7d32;
}
</style>