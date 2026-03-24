<template>
  <div class="app">
    <div class="header">
      <h1>图像编辑系统</h1>
      <div class="user-info">
        <span>欢迎，{{ user?.username }}</span>
        <button v-if="user?.is_admin" class="btn" @click="$router.push('/admin')">
          用户管理
        </button>
        <button class="btn" @click="showLogs = !showLogs">
          {{ showLogs ? '隐藏日志' : '显示日志' }}
        </button>
        <button class="btn logout-btn" @click="logout">
          注销
        </button>
      </div>
    </div>
    
    <div class="container">
      <div class="function-tabs">
        <button 
          :class="{ active: activeTab === 'generate' }" 
          @click="activeTab = 'generate'"
        >
          文生图
        </button>
        <button 
          :class="{ active: activeTab === 'edit' }" 
          @click="activeTab = 'edit'"
        >
          图像编辑
        </button>
      </div>
      
      <!-- 文生图功能 -->
      <div v-if="activeTab === 'generate'" class="function-content">
        <h2>文生图</h2>
        <div class="input-group">
          <label for="prompt">提示词</label>
          <textarea 
            id="prompt" 
            v-model="generateForm.prompt" 
            placeholder="请输入图像描述..."
          ></textarea>
        </div>
        <div class="input-group">
          <label for="api-choice">选择API</label>
          <select id="api-choice" v-model="generateForm.apiChoice">
            <option value="API-1">API-1</option>
            <option value="API-2">API-2</option>
            <option value="API-3">API-3</option>
          </select>
        </div>
        <button 
          class="btn" 
          @click="generateImage"
          :disabled="isGenerating"
        >
          {{ isGenerating ? '生成中...' : '生成图像' }}
        </button>
        <div class="image-preview" v-if="generatedImage">
          <img :src="generatedImage" alt="生成的图像">
        </div>
        <div class="debug-info" v-if="debugInfo">
          <h3>调试信息</h3>
          <pre>{{ debugInfo }}</pre>
        </div>
      </div>
      
      <!-- 图像编辑功能 -->
      <div v-else class="function-content">
        <h2>图像编辑</h2>
        <div class="input-group">
          <label for="image-upload">上传图像</label>
          <input 
            type="file" 
            id="image-upload" 
            accept="image/*" 
            @change="handleImageUpload"
          >
        </div>
        <div class="input-group">
          <label for="edit-prompt">编辑提示词 (可选)</label>
          <textarea 
            id="edit-prompt" 
            v-model="editForm.prompt" 
            placeholder="请输入编辑要求..."
          ></textarea>
        </div>
        <div class="input-group">
          <label for="edit-api-choice">选择API</label>
          <select id="edit-api-choice" v-model="editForm.apiChoice">
            <option value="API-1">API-1</option>
            <option value="API-2">API-2</option>
            <option value="API-3">API-3</option>
          </select>
        </div>
        <button 
          class="btn" 
          @click="editImage"
          :disabled="isEditing || !uploadedImage"
        >
          {{ isEditing ? '编辑中...' : '编辑图像' }}
        </button>
        <div class="image-comparison" v-if="uploadedImage">
          <div class="image-box">
            <h3>原始图像</h3>
            <img :src="uploadedImage" alt="原始图像">
          </div>
          <div class="image-box">
            <h3>编辑后图像</h3>
            <div v-if="isEditing">
              <p>编辑中...</p>
            </div>
            <img v-else-if="editedImage" :src="editedImage" alt="编辑后的图像">
          </div>
        </div>
      </div>
    </div>
    
    <!-- 日志弹窗 -->
    <div v-if="showLogs" class="log-popup">
      <div class="log-popup-content">
        <div class="log-popup-header">
          <h3>API调用日志</h3>
          <button class="close-btn" @click="showLogs = false">&times;</button>
        </div>
        <div class="log-popup-body">
          <div v-if="logs.length === 0" class="no-logs">
            暂无日志
          </div>
          <ul v-else class="log-list">
            <li v-for="(log, index) in logs" :key="index" class="log-item">
              {{ log }}
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MainView',
  data() {
    return {
      user: null,
      activeTab: 'generate',
      generateForm: {
        prompt: '',
        apiChoice: 'API-1'
      },
      editForm: {
        prompt: '',
        apiChoice: 'API-1'
      },
      uploadedImage: null,
      generatedImage: null,
      editedImage: null,
      isGenerating: false,
      isEditing: false,
      showLogs: false,
      logs: [],
      debugInfo: null
    }
  },
  mounted() {
    // 从localStorage获取用户信息
    const userStr = localStorage.getItem('user')
    if (userStr) {
      this.user = JSON.parse(userStr)
      // 设置axios默认配置，确保携带认证信息
      axios.defaults.withCredentials = true
    } else {
      // 未登录，跳转到登录页面
      this.$router.push('/')
    }
  },
  methods: {
    async logout() {
      try {
        await axios.get('http://47.121.190.137:5000/api/logout')
        localStorage.removeItem('user')
        this.$router.push('/')
      } catch (error) {
        console.error('Logout error:', error)
      }
    },
    async generateImage() {
      if (!this.generateForm.prompt) {
        alert('请输入提示词')
        return
      }
      
      this.isGenerating = true
      this.logs = []
      this.debugInfo = null
      
      try {
        console.log('开始生成图像，参数:', {
          prompt: this.generateForm.prompt,
          api_choice: this.generateForm.apiChoice
        })
        
        const response = await axios.post('http://47.121.190.137:5000/api/generate', {
          prompt: this.generateForm.prompt,
          api_choice: this.generateForm.apiChoice
        }, {
          withCredentials: true, // 确保携带认证信息
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        console.log('生成图像响应:', response.data)
        
        // 检查响应是否为HTML
        if (typeof response.data === 'string' && response.data.includes('<!DOCTYPE html>')) {
          throw new Error('未登录或会话过期，请重新登录')
        }
        
        this.generatedImage = response.data.image
        if (response.data.logs) {
          this.logs = response.data.logs
        }
        
        // 添加调试信息
        this.debugInfo = JSON.stringify({
          responseStatus: response.status,
          responseData: response.data,
          imageLength: response.data.image ? response.data.image.length : 0,
          imagePrefix: response.data.image ? response.data.image.substring(0, 50) : 'No image'
        }, null, 2)
        
      } catch (error) {
        console.error('Generate image error:', error)
        this.debugInfo = JSON.stringify({
          error: error.message,
          errorResponse: error.response ? error.response.data : 'No response'
        }, null, 2)
        alert('生成失败，请稍后重试')
      } finally {
        this.isGenerating = false
      }
    },
    handleImageUpload(e) {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.uploadedImage = e.target.result
          this.editedImage = null
        }
        reader.readAsDataURL(file)
      }
    },
    async editImage() {
      if (!this.uploadedImage) {
        alert('请先上传图像')
        return
      }
      
      this.isEditing = true
      this.logs = []
      
      try {
        const response = await axios.post('http://47.121.190.137:5000/api/edit', {
          image: this.uploadedImage,
          prompt: this.editForm.prompt,
          api_choice: this.editForm.apiChoice
        }, {
          withCredentials: true, // 确保携带认证信息
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        // 检查响应是否为HTML
        if (typeof response.data === 'string' && response.data.includes('<!DOCTYPE html>')) {
          throw new Error('未登录或会话过期，请重新登录')
        }
        
        this.editedImage = response.data.image
        if (response.data.logs) {
          this.logs = response.data.logs
        }
      } catch (error) {
        console.error('Edit image error:', error)
        alert('编辑失败，请稍后重试')
      } finally {
        this.isEditing = false
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

.function-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.function-tabs button {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.function-tabs button.active {
  color: #333;
  border-bottom: 2px solid #4CAF50;
}

.function-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.function-content h2 {
  margin-bottom: 20px;
  color: #333;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  resize: vertical;
  min-height: 100px;
}

.input-group select {
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

.image-preview {
  margin-top: 20px;
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 500px;
  border-radius: 4px;
}

.image-comparison {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.image-comparison .image-box {
  flex: 1;
  text-align: center;
  margin: 0 10px;
}

.image-comparison h3 {
  margin-bottom: 10px;
  font-size: 16px;
  color: #666;
}

.image-comparison img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 4px;
}

.debug-info {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: monospace;
  font-size: 12px;
  white-space: pre-wrap;
}

.debug-info h3 {
  margin-top: 0;
  font-size: 14px;
  color: #333;
}

@media (max-width: 768px) {
  .function-tabs {
    flex-direction: column;
  }
  
  .function-tabs button {
    text-align: left;
    border-bottom: 1px solid #ddd;
  }
  
  .image-comparison {
    flex-direction: column;
  }
  
  .image-comparison .image-box {
    margin: 10px 0;
  }
  
  .log-popup-content {
    width: 90%;
    height: 80%;
  }
}

/* 日志弹窗样式 */
.log-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.log-popup-content {
  background-color: white;
  border-radius: 8px;
  width: 80%;
  height: 70%;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.log-popup-header {
  padding: 15px;
  border-bottom: 1px solid #ddd;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;
}

.log-popup-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: #e0e0e0;
}

.log-popup-body {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
}

.no-logs {
  text-align: center;
  color: #666;
  margin-top: 50px;
}

.log-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.log-item {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.4;
}

.log-item:last-child {
  border-bottom: none;
}
</style>
