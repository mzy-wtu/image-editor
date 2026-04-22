<template>
  <div class="login-page">
    <div class="bg-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
    
    <div class="form-container">
      <div class="logo-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <circle cx="8.5" cy="8.5" r="1.5"/>
          <path d="M21 15l-5-5L5 21"/>
        </svg>
      </div>
      
      <h1>图像编辑系统</h1>
      <p class="subtitle">AI 驱动的智能图像生成与编辑平台</p>
      
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
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <input type="text" id="login-username" v-model="loginForm.username" required placeholder=" ">
            <label for="login-username">用户名</label>
          </div>
        </div>
        <div class="form-group">
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <input type="password" id="login-password" v-model="loginForm.password" required placeholder=" ">
            <label for="login-password">密码</label>
          </div>
        </div>
        <button type="submit" class="btn" :disabled="isLoading">
          <span v-if="!isLoading">登录</span>
          <span v-else class="loading-spinner"></span>
        </button>
        <div v-if="message" :class="['message', messageType]">
          {{ message }}
        </div>
      </form>
      
      <!-- 注册表单 -->
      <form v-else @submit.prevent="register">
        <div class="form-group">
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            <input type="text" id="register-username" v-model="registerForm.username" required placeholder=" ">
            <label for="register-username">用户名</label>
          </div>
        </div>
        <div class="form-group">
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            <input type="password" id="register-password" v-model="registerForm.password" required placeholder=" ">
            <label for="register-password">密码</label>
          </div>
        </div>
        <div class="form-group">
          <div class="input-wrapper">
            <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            <input type="email" id="register-email" v-model="registerForm.email" placeholder=" ">
            <label for="register-email">邮箱 (可选)</label>
          </div>
        </div>
        <button type="submit" class="btn" :disabled="isLoading">
          <span v-if="!isLoading">注册</span>
          <span v-else class="loading-spinner"></span>
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
        const response = await axios.post('/api/login', this.loginForm, {
          withCredentials: true
        })
        this.message = response.data.message
        this.messageType = 'success'
        
        localStorage.setItem('user', JSON.stringify(response.data.user))
        
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
        const response = await axios.post('/api/register', this.registerForm, {
          withCredentials: true
        })
        this.message = response.data.message
        this.messageType = 'success'
        
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
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}

.bg-shapes {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.shape {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: float 20s infinite ease-in-out;
}

.shape-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  top: -200px;
  left: -100px;
  animation-delay: 0s;
}

.shape-2 {
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  bottom: -150px;
  right: -100px;
  animation-delay: -5s;
}

.shape-3 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(30px, -30px) rotate(5deg);
  }
  50% {
    transform: translate(-20px, 20px) rotate(-5deg);
  }
  75% {
    transform: translate(20px, 30px) rotate(3deg);
  }
}

.form-container {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 1;
}

.logo-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.logo-icon svg {
  width: 36px;
  height: 36px;
  color: white;
}

.form-container h1 {
  text-align: center;
  margin: 0 0 8px;
  color: white;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.subtitle {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin-bottom: 30px;
}

.form-tabs {
  display: flex;
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 4px;
}

.form-tabs button {
  flex: 1;
  padding: 12px;
  background: transparent;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.6);
  transition: all 0.3s ease;
}

.form-tabs button.active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.5);
  transition: color 0.3s;
}

.input-wrapper input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 15px;
  color: white;
  outline: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.input-wrapper input::placeholder {
  color: transparent;
}

.input-wrapper input:focus {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
}

.input-wrapper input:focus + .input-icon,
.input-wrapper input:not(:placeholder-shown) + .input-icon,
.input-wrapper input:focus ~ label,
.input-wrapper input:not(:placeholder-shown) ~ label {
  color: #667eea;
}

.input-wrapper label {
  position: absolute;
  left: 48px;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.5);
  font-size: 15px;
  pointer-events: none;
  transition: all 0.3s ease;
}

.input-wrapper input:focus ~ label,
.input-wrapper input:not(:placeholder-shown) ~ label {
  top: 0;
  font-size: 12px;
  background: linear-gradient(135deg, #302b63 0%, #24243e 100%);
  padding: 0 8px;
}

.btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.message {
  margin-top: 16px;
  padding: 12px 16px;
  border-radius: 10px;
  text-align: center;
  font-size: 14px;
}

.message.error {
  background: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.message.success {
  background: rgba(34, 197, 94, 0.2);
  color: #86efac;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

@media (max-width: 480px) {
  .form-container {
    margin: 20px;
    padding: 30px 24px;
  }
  
  .shape-1,
  .shape-2,
  .shape-3 {
    width: 300px;
    height: 300px;
  }
}
</style>