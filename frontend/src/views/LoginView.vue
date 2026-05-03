<template>
  <div class="login-page">
    <div class="login-hero">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="hero-badge">AI-POWERED IMAGE STUDIO</div>
        <h1>用智能<br>重新定义创作</h1>
        <p>AI驱动的图像生成与编辑平台<br>一句话描述你想要的画面，即刻呈现</p>
      </div>
    </div>
    <div class="login-side">
      <div class="login-card">
        <div class="login-logo">
          <AppIcon name="image" size="32" />
        </div>
        <h2>欢迎回来</h2>
        <p class="login-subtitle">登录你的账户</p>

        <div class="login-tabs">
          <button :class="{ active: activeTab === 'login' }" @click="activeTab = 'login'">登录</button>
          <button :class="{ active: activeTab === 'register' }" @click="activeTab = 'register'">注册</button>
        </div>

        <form v-if="activeTab === 'login'" @submit.prevent="login">
          <div class="form-group">
            <div class="input-wrapper">
              <AppIcon name="user" size="18" class="input-icon" />
              <input type="text" v-model="loginForm.username" required placeholder="用户名">
            </div>
          </div>
          <div class="form-group">
            <div class="input-wrapper">
              <AppIcon name="lock" size="18" class="input-icon" />
              <input type="password" v-model="loginForm.password" required placeholder="密码">
            </div>
          </div>
          <button type="submit" class="login-btn" :disabled="isLoading">
            <span v-if="!isLoading">登 录</span>
            <span v-else class="loading-spinner"></span>
          </button>
          <div v-if="message" :class="['message', messageType]">{{ message }}</div>
        </form>

        <form v-else @submit.prevent="register">
          <div class="form-group">
            <div class="input-wrapper">
              <AppIcon name="user" size="18" class="input-icon" />
              <input type="text" v-model="registerForm.username" required placeholder="用户名">
            </div>
          </div>
          <div class="form-group">
            <div class="input-wrapper">
              <AppIcon name="lock" size="18" class="input-icon" />
              <input type="password" v-model="registerForm.password" required placeholder="密码">
            </div>
          </div>
          <div class="form-group">
            <div class="input-wrapper">
              <AppIcon name="mail" size="18" class="input-icon" />
              <input type="email" v-model="registerForm.email" placeholder="邮箱 (可选)">
            </div>
          </div>
          <button type="submit" class="login-btn" :disabled="isLoading">
            <span v-if="!isLoading">注 册</span>
            <span v-else class="loading-spinner"></span>
          </button>
          <div v-if="message" :class="['message', messageType]">{{ message }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import AppIcon from '../components/common/AppIcon.vue'

export default {
  name: 'LoginView',
  components: { AppIcon },
  data() {
    return {
      activeTab: 'login',
      loginForm: { username: '', password: '' },
      registerForm: { username: '', password: '', email: '' },
      isLoading: false,
      message: '',
      messageType: ''
    }
  },
  methods: {
    async login() {
      this.isLoading = true; this.message = ''
      try {
        const res = await axios.post('/api/login', this.loginForm, { withCredentials: true })
        this.message = res.data.message; this.messageType = 'success'
        localStorage.setItem('user', JSON.stringify(res.data.user))
        setTimeout(() => this.$router.push('/main'), 1000)
      } catch (error) {
        this.message = error.response?.data?.error || '登录失败，请稍后重试'
        this.messageType = 'error'
      } finally {
        this.isLoading = false
      }
    },
    async register() {
      this.isLoading = true; this.message = ''
      try {
        const res = await axios.post('/api/register', this.registerForm, { withCredentials: true })
        this.message = res.data.message; this.messageType = 'success'
        setTimeout(() => { this.activeTab = 'login' }, 1000)
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
  display: flex;
  min-height: 100vh;
}

.login-hero {
  flex: 2;
  position: relative;
  background: linear-gradient(135deg, #5c3d2e 0%, #8B7355 30%, #a0522d 50%, #c98d5f 70%, #d4a574 100%);
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 30% 40%, rgba(255, 220, 180, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 60% 70%, rgba(160, 82, 45, 0.3) 0%, transparent 50%);
}

.hero-content {
  position: relative;
  z-index: 1;
  padding: 80px;
  max-width: 560px;
}

.hero-badge {
  display: inline-block;
  font-size: 10px;
  letter-spacing: 4px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  margin-bottom: 32px;
  padding: 6px 14px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 4px;
}

.hero-content h1 {
  font-size: 44px;
  font-weight: 700;
  color: white;
  line-height: 1.2;
  margin: 0 0 20px;
  letter-spacing: -1px;
}

.hero-content p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.8;
  margin: 0;
}

.login-side {
  flex: 1;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-card {
  width: 100%;
  max-width: 360px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 40px 32px;
  box-shadow: var(--shadow-lg);
}

.login-logo {
  width: 52px;
  height: 52px;
  margin: 0 auto 16px;
  background: linear-gradient(135deg, #c98d5f, #a0522d);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.login-card h2 {
  text-align: center;
  margin: 0 0 4px;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.login-subtitle {
  text-align: center;
  font-size: 13px;
  color: var(--text-muted);
  margin: 0 0 24px;
}

.login-tabs {
  display: flex;
  background: var(--bg-tertiary);
  border-radius: var(--radius);
  padding: 3px;
  margin-bottom: 24px;
}

.login-tabs button {
  flex: 1;
  padding: 8px;
  background: transparent;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-muted);
  transition: all var(--transition);
}

.login-tabs button.active {
  background: var(--bg-primary);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
}

.form-group { margin-bottom: 16px; }

.input-wrapper { position: relative; }

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 11px 14px 11px 42px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 14px;
  color: var(--text-primary);
  outline: none;
  transition: all var(--transition);
  box-sizing: border-box;
}

.input-wrapper input::placeholder { color: var(--text-muted); }
.input-wrapper input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(201, 141, 95, 0.1);
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #c98d5f, #a0522d);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-btn:hover:not(:disabled) { opacity: 0.9; }
.login-btn:disabled { opacity: 0.5; cursor: not-allowed; }

.message {
  margin-top: 16px;
  padding: 10px 14px;
  border-radius: var(--radius);
  text-align: center;
  font-size: 13px;
}
.message.error { background: var(--danger-bg); color: var(--danger); border: 1px solid var(--danger-border); }
.message.success { background: var(--success-bg); color: #16a34a; border: 1px solid #bbf7d0; }

@media (max-width: 768px) {
  .login-page { flex-direction: column; }
  .login-hero { min-height: 240px; }
  .hero-content { padding: 40px; }
  .hero-content h1 { font-size: 28px; }
}
</style>
