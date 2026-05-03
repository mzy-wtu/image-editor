# Warm Amber Frontend Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current indigo/slate design system with a warm amber palette, add functional dark mode, redesign login page with split layout.

**Architecture:** Two-phase approach: (1) Foundation — rewrite CSS design tokens and dark mode mechanism, since all components depend on them. (2) Pages & components — update each view and component to use the new tokens and match spec wireframes. All changes are CSS/scoped-style only; no structural changes to components.

**Tech Stack:** Vue 3, Vite, CSS custom properties, no additional dependencies.

---

### Task 1: Rewrite useDarkTheme composable

**Files:**
- Modify: `frontend/src/composables/useDarkTheme.js`

- [ ] **Step 1: Rewrite to use data-theme attribute**

Replace the entire file:

```js
import { ref, watchEffect } from 'vue'

const isDarkTheme = ref(false)

function loadTheme() {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    isDarkTheme.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  } else if (saved === 'light') {
    document.documentElement.setAttribute('data-theme', 'light')
  } else {
    const prefers = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDarkTheme.value = prefers
    document.documentElement.setAttribute('data-theme', prefers ? 'dark' : 'light')
  }
}

function toggleTheme() {
  isDarkTheme.value = !isDarkTheme.value
  const theme = isDarkTheme.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

loadTheme()

export function useDarkTheme() {
  return { isDarkTheme, toggleTheme }
}
```

- [ ] **Step 2: Verify build**

Run: `cd frontend && npx vite build`
Expected: Build succeeds, no errors.

---

### Task 2: Rewrite global.css — Warm amber design tokens + dark mode

**Files:**
- Modify: `frontend/src/assets/styles/global.css`

- [ ] **Step 1: Replace entire global.css**

```css
:root {
  /* Accent — warm amber */
  --accent: #c98d5f;
  --accent-hover: #a0522d;
  --accent-light: #fdf6f0;
  --accent-subtle: #faf0e6;

  /* Backgrounds */
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;

  /* Text */
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;
  --text-inverse: #ffffff;

  /* Borders */
  --border: #e2e8f0;
  --border-light: #f1f5f9;
  --border-focus: #c98d5f;

  /* Status */
  --danger: #ef4444;
  --danger-bg: #fef2f2;
  --danger-border: #fecaca;
  --success: #22c55e;
  --success-bg: #f0fdf4;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.05), 0 2px 4px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.06), 0 4px 6px rgba(0, 0, 0, 0.04);

  /* Radii */
  --radius-sm: 6px;
  --radius: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;

  /* Typography */
  --font: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  --mono: 'JetBrains Mono', ui-monospace, 'Cascadia Code', Consolas, monospace;

  /* Transition */
  --transition: 0.15s ease;
}

/* Dark mode overrides */
[data-theme="dark"] {
  --bg-primary: #1e293b;
  --bg-secondary: #0f172a;
  --bg-tertiary: #334155;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --text-inverse: #1e293b;
  --border: #334155;
  --border-light: #1e293b;
  --border-focus: #c98d5f;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.2);
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.25);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.35);
  --accent-light: rgba(201, 141, 95, 0.15);
  --accent-subtle: rgba(201, 141, 95, 0.1);
  --danger-bg: rgba(239, 68, 68, 0.15);
  --success-bg: rgba(34, 197, 94, 0.15);
}

*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  font-family: var(--font);
  font-size: 14px;
  color: var(--text-primary);
  background: var(--bg-secondary);
  -webkit-font-smoothing: antialiased;
}

.card, .glass-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.input-field {
  width: 100%;
  padding: 10px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 14px;
  color: var(--text-primary);
  resize: vertical;
  transition: border-color var(--transition), box-shadow var(--transition);
  box-sizing: border-box;
  font-family: inherit;
  line-height: 1.5;
}
.input-field::placeholder { color: var(--text-muted); }
.input-field:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(201, 141, 95, 0.15);
}

.btn-primary {
  padding: 12px 20px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.btn-primary:hover:not(:disabled) { background: var(--accent-hover); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-sm {
  padding: 6px 12px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all var(--transition);
}
.btn-sm:hover { background: var(--bg-tertiary); border-color: var(--accent); color: var(--accent); }

.icon-btn {
  width: 38px; height: 38px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all var(--transition);
  color: var(--text-secondary);
}
.icon-btn:hover { background: var(--bg-tertiary); border-color: var(--accent); color: var(--accent); }

.top-navbar {
  background: var(--bg-primary);
  padding: 0 24px;
  height: 56px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border);
  position: relative;
  z-index: 10;
}

.nav-btn {
  padding: 8px 14px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 13px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all var(--transition);
}
.nav-btn:hover { background: var(--bg-tertiary); color: var(--text-primary); }
.nav-btn.logout { color: var(--danger); border-color: var(--danger-border); background: var(--danger-bg); }
.nav-btn.logout:hover { background: #fee2e2; }

.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(15, 23, 42, 0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: 28px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  border: 1px solid var(--border);
  box-shadow: var(--shadow-lg);
}

.loading-spinner {
  width: 18px; height: 18px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

input[type="range"] {
  width: 100%; height: 6px;
  -webkit-appearance: none; appearance: none;
  background: var(--border);
  border-radius: 3px;
  outline: none;
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px; height: 18px;
  background: var(--accent);
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: var(--shadow-sm);
}

select.input-field {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  padding-right: 36px;
  cursor: pointer;
}
```

- [ ] **Step 2: Verify build**

Run: `cd frontend && npx vite build`
Expected: Build succeeds, no errors.

---

### Task 3: Rewrite LoginView — Warm split layout

**Files:**
- Modify: `frontend/src/views/LoginView.vue`

- [ ] **Step 1: Replace template**

```html
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
```

- [ ] **Step 2: Replace style**

```css
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
```

- [ ] **Step 3: Verify build**

Run: `cd frontend && npx vite build`
Expected: Build succeeds.

---

### Task 4: Update MainView — Clean workspace with amber accents

**Files:**
- Modify: `frontend/src/views/MainView.vue`

**Note:** Script section unchanged from current version. Only replace template and style.

- [ ] **Step 1: Replace template** (remove bg-shapes, remove dark-theme class binding)

```html
<template>
  <div class="main-app">
    <header class="top-navbar">
      <div class="navbar-left">
        <div class="logo-icon">
          <AppIcon name="image" size="22" />
        </div>
        <h1 class="logo">AI图像工坊</h1>
      </div>
      <div class="navbar-right">
        <button class="icon-btn" @click="toggleTheme" :title="isDarkTheme ? '浅色模式' : '深色模式'">
          <AppIcon :name="isDarkTheme ? 'sun' : 'moon'" size="18" />
        </button>
        <button class="icon-btn" @click="$router.push('/history')" title="历史记录">
          <AppIcon name="history" size="18" />
        </button>
        <button v-if="user?.is_admin" class="icon-btn" @click="$router.push('/admin')" title="用户管理">
          <AppIcon name="admin" size="18" />
        </button>
        <div class="user-menu">
          <span class="username">{{ user?.username }}</span>
          <button class="logout-btn" @click="logout">
            <AppIcon name="logout" size="16" />
          </button>
        </div>
      </div>
    </header>

    <div class="main-container">
      <aside class="sidebar">
        <div class="mode-selector">
          <button :class="['mode-btn', { active: activeTab === 'generate' }]" @click="activeTab = 'generate'">
            <AppIcon name="plus" size="16" />文生图
          </button>
          <button :class="['mode-btn', { active: activeTab === 'edit' }]" @click="activeTab = 'edit'">
            <AppIcon name="edit" size="16" />图像编辑
          </button>
        </div>

        <GeneratePanel v-if="activeTab === 'generate'" :loading="isGenerating" @generate="handleGenerate" />
        <EditPanel v-else :current-tab="editSubTab" :loading="isEditing"
          @update:sub-tab="editSubTab = $event" @update:uploaded-image="uploadedImage = $event" @edit="handleEdit" />
      </aside>

      <main class="content-area">
        <template v-if="activeTab === 'generate'">
          <EmptyState v-if="!generatedImages.length && !isGenerating" icon="image" title="开始创作" description="在左侧输入提示词生成图像" />
          <LoadingSpinner v-if="isGenerating" text="AI创作中..." />
          <div v-if="generatedImages.length" class="image-grid">
            <ImageCard v-for="(img, i) in generatedImages" :key="i" :src="img" :index="i"
              @preview="previewImage = $event" @download="downloadImage" />
          </div>
        </template>

        <template v-else>
          <EmptyState v-if="!isEditing && !editedImage && editSubTab !== 'sketch'" icon="image" title="上传图像" description="在左侧上传图像开始编辑" />
          <EmptyState v-if="!isEditing && !editedImage && editSubTab === 'sketch'" icon="sketch" title="涂鸦作画" description="在左侧画布上涂鸦，输入描述后生成图像" />
          <LoadingSpinner v-if="isEditing" text="编辑中..." />
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
          <div v-if="editedImage && editSubTab === 'sketch'" class="single-result">
            <h4>生成结果</h4>
            <img :src="editedImage">
          </div>
        </template>

        <div v-if="logs.length" class="logs-panel">
          <div class="logs-header">
            <span>日志</span>
            <button @click="logs = []"><AppIcon name="close" size="16" /></button>
          </div>
          <div class="logs-content">
            <div v-for="(log, i) in logs" :key="i">{{ log }}</div>
          </div>
        </div>
      </main>
    </div>

    <div v-if="previewImage" class="modal-overlay" @click="previewImage = null">
      <img :src="previewImage" class="preview-img" @click.stop>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Replace style**

```css
<style scoped>
.main-app {
  min-height: 100vh;
  background: var(--bg-secondary);
}

.logo-icon {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #c98d5f, #a0522d);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: white;
}

.logo {
  font-size: 18px; font-weight: 700;
  margin: 0; color: var(--text-primary);
  letter-spacing: -0.3px;
}

.navbar-left { display: flex; align-items: center; gap: 10px; }
.navbar-right { display: flex; gap: 8px; align-items: center; }

.user-menu {
  display: flex; align-items: center; gap: 10px;
  margin-left: 4px; padding-left: 12px;
  border-left: 1px solid var(--border);
}
.username { font-size: 13px; color: var(--text-secondary); font-weight: 500; }

.logout-btn {
  width: 32px; height: 32px;
  background: var(--danger-bg);
  border: 1px solid var(--danger-border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: var(--danger);
  transition: background var(--transition);
}
.logout-btn:hover { background: #fee2e2; }

.main-container {
  display: flex;
  max-width: 1500px; margin: 0 auto;
  gap: 20px; padding: 20px 24px 24px;
}

.sidebar {
  width: 370px; flex-shrink: 0;
  padding: 20px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  max-height: calc(100vh - 96px); overflow-y: auto;
}

.content-area {
  flex: 1;
  padding: 24px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  min-height: calc(100vh - 96px);
}

.mode-selector { display: flex; gap: 8px; margin-bottom: 20px; }

.mode-btn {
  flex: 1; padding: 10px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer; font-size: 13px; font-weight: 500;
  color: var(--text-secondary);
  display: flex; align-items: center; justify-content: center; gap: 6px;
  transition: all var(--transition);
}
.mode-btn:hover { background: var(--accent-light); color: var(--accent); }
.mode-btn.active { background: var(--accent); color: white; border-color: var(--accent); }

.image-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }

.comparison-view { display: flex; gap: 20px; }
.comparison-side { flex: 1; text-align: center; }
.comparison-side h4 { font-size: 14px; font-weight: 600; color: var(--text-secondary); margin: 0 0 12px; }
.comparison-side img { width: 100%; max-width: 500px; border-radius: var(--radius); border: 1px solid var(--border); }

.single-result { text-align: center; }
.single-result h4 { font-size: 14px; font-weight: 600; color: var(--text-secondary); margin: 0 0 12px; }
.single-result img { max-width: 100%; border-radius: var(--radius); border: 1px solid var(--border); }

.logs-panel {
  margin-top: 20px;
  background: var(--bg-tertiary);
  border-radius: var(--radius); padding: 14px;
  border: 1px solid var(--border);
}
.logs-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 13px; font-weight: 600; color: var(--text-secondary); }
.logs-header button { background: none; border: none; cursor: pointer; color: var(--text-muted); padding: 2px; }
.logs-header button:hover { color: var(--text-primary); }
.logs-content { max-height: 160px; overflow-y: auto; font-family: var(--mono); font-size: 12px; color: var(--text-secondary); line-height: 1.6; }

.preview-img { max-width: 90vw; max-height: 90vh; border-radius: var(--radius); box-shadow: var(--shadow-lg); }

@media (max-width: 1200px) {
  .main-container { flex-direction: column; }
  .sidebar { width: 100%; max-height: none; }
  .comparison-view { flex-direction: column; }
}
</style>
```

- [ ] **Step 3: Verify build**

Run: `cd frontend && npx vite build`
Expected: Build succeeds.

---

### Task 5: Update remaining views — HistoryView, AdminView

**Files:**
- Modify: `frontend/src/views/HistoryView.vue`
- Modify: `frontend/src/views/AdminView.vue`

These two views from the previous redesign already use `var(--*)` tokens for all colors. They just need:
- Logo background: `linear-gradient(135deg, #c98d5f, #a0522d)`
- Download button color: `var(--accent)` instead of `var(--accent)` (already does)
- Any remaining `#4f46e5` (indigo) references changed to `#c98d5f` (amber)

- [ ] **Step 1: Check HistoryView for indigo references and replace with amber**

Run: `grep -n '#4f46e5\|#4338ca\|#667eea\|#764ba2' frontend/src/views/HistoryView.vue`
If no matches, skip. If matches found, replace with amber equivalents.

- [ ] **Step 2: Check AdminView for indigo references and replace with amber**

Run: `grep -n '#4f46e5\|#4338ca\|#667eea\|#764ba2' frontend/src/views/AdminView.vue`
If no matches, skip. Replace found instances: `#4f46e5` → `#c98d5f`, `#4338ca` → `#a0522d`.

- [ ] **Step 3: Verify build**

Run: `cd frontend && npx vite build`
Expected: Build succeeds.

---

### Task 6: Update panel components — GeneratePanel, EditPanel

**Files:**
- Modify: `frontend/src/components/panels/GeneratePanel.vue`
- Modify: `frontend/src/components/panels/EditPanel.vue`

These already use CSS variables. Need to update `apiOptions` colors to warm palette and ensure amber accent.

- [ ] **Step 1: Update GeneratePanel apiOptions colors**

Find the `apiOptions` array in `data()` and replace color values:
```js
apiOptions: [
  { value: 'API-1', label: '千问', color: '#c98d5f' },
  { value: 'API-2', label: '通义', color: '#0891b2' },
  { value: 'API-3', label: '模拟', color: '#6b7280' },
  { value: 'API-4', label: '万象Pro', color: '#a0522d' }
],
```

- [ ] **Step 2: Update EditPanel apiOptions colors**

Same as above — apply identical change to EditPanel's `apiOptions`.

- [ ] **Step 3: Update EditPanel style-card active state to use amber**

In EditPanel `<style scoped>`, ensure `.style-card.active` uses `--accent` colors (already does via variables). Check `.style-initial` uses amber:
```css
.style-initial {
  background: var(--accent);
  /* ... */
}
```
If currently `#4f46e5`, change to `var(--accent)`.

- [ ] **Step 4: Verify build**

Run: `cd frontend && npx vite build`
Expected: Build succeeds.

---

### Task 7: Update common components — Toast, ImageUpload

**Files:**
- Modify: `frontend/src/components/common/Toast.vue`
- Modify: `frontend/src/components/common/ImageUpload.vue`

- [ ] **Step 1: Update Toast info color to amber**

In Toast.vue `<style scoped>`, replace:
```css
.toast-info { background: #eef2ff; color: #3730a3; border-color: #c7d2fe; }
```
With:
```css
.toast-info { background: #fdf6f0; color: #9a5c2e; border-color: #f5d5b8; }
```

- [ ] **Step 2: Update ImageUpload hover border to amber**

In ImageUpload.vue `<style scoped>`, verify hover uses `var(--accent)`. Current uses `var(--accent)` — should already work since the variable changed. No code change needed if already using variables.

- [ ] **Step 3: Verify build**

Run: `cd frontend && npx vite build`
Expected: Build succeeds.

---

### Task 8: Final verification & cleanup

- [ ] **Step 1: Full production build**

Run: `cd frontend && npx vite build`
Expected: Clean build, zero errors, CSS output uses warm amber hex values.

- [ ] **Step 2: Check for any remaining old palette colors**

Run: `cd frontend && grep -rn '#4f46e5\|#4338ca\|#667eea\|#764ba2\|#f093fb\|#302b63\|#24243e' src/`
Expected: No matches (all replaced).

- [ ] **Step 3: Check for any remaining emoji in functional roles**

Run: `cd frontend && grep -rn "'🤖'\|'🎯'\|'🧪'\|'🌟'\|'🎨'\|'🧸'\|'✨'\|'🌿'\|'🌈'\|'🏮'\|'🏰'\|'🪆'\|'🌐'\|'🌸'\|'🖍️'" src/`
Expected: No matches (all emoji replaced with color dots or letter initials).

- [ ] **Step 4: Delete design doc**

Remove: `docs/superpowers/specs/2026-04-30-warm-amber-redesign.md`
(Per user request — delete after implementation complete.)

- [ ] **Step 5: Start dev server for manual verification**

Run: `cd frontend && npx vite --port 5173`
Open `http://localhost:5173` and verify:
- Login page shows warm gradient hero + white card
- Dark mode toggle works (check navbar, sidebar, content area)
- All pages render correctly
