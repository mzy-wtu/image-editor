<<<<<<< HEAD
# 图像编辑系统

## 项目概述

这是一个基于大模型的图像编辑Web应用，用户可通过注册登录进入系统，使用文生图和图像编辑功能。后端使用Python Flask框架，前端使用Vue.js，数据库使用MySQL。

## 功能特点

- **用户管理**：注册、登录、权限控制
- **文生图**：通过文本描述生成图像
- **图像编辑**：上传图片并进行编辑
- **管理员功能**：管理用户列表，禁用/启用用户
- **模拟API**：提供三个模拟大模型API接口

## 技术栈

- **后端**：Python, Flask, Flask-Login, Flask-CORS, Flask-SQLAlchemy
- **前端**：Vue.js, Vue Router, Axios
- **数据库**：MySQL
- **图像处理**：Pillow

## 项目结构

```
image-editor/
├── app/            # 后端应用
│   ├── api/        # API路由
│   │   ├── user_api.py    # 用户管理API
│   │   └── image_api.py   # 图像处理API
│   ├── models/     # 数据模型
│   │   └── user.py        # 用户模型
│   ├── static/     # 静态文件
│   ├── templates/  # HTML模板
│   ├── utils/      # 工具函数
│   │   └── mock_api.py    # 模拟API实现
│   ├── __init__.py # 应用初始化
│   ├── config.py   # 配置文件
│   └── routes.py   # 路由定义
├── frontend/       # 前端应用
│   ├── src/        # 源代码
│   ├── dist/       # 构建文件
│   └── public/     # 公共文件
├── images/         # 图像存储目录
├── venv/           # 虚拟环境
├── init_db.py      # 数据库初始化脚本
├── create_db.py    # 数据库创建脚本
├── requirements.txt # 依赖包
├── 启动系统.bat    # 启动脚本
├── start.ps1       # PowerShell启动脚本
├── stop.bat        # 停止脚本
└── README.md       # 项目说明
```

## 安装与运行

### 1. 准备工作

- 安装Python 3.7+
- 安装MySQL数据库

### 2. 安装依赖

```bash
# 创建虚拟环境（如果尚未创建）
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
cd ..
```

### 3. 创建数据库

```bash
python create_db.py
```

这将创建名为 `image_editor` 的数据库。

### 4. 初始化数据库

```bash
python init_db.py
```

这将创建数据库表并添加默认管理员账号：`admin/admin`

### 5. 启动应用

**方法一：使用启动脚本（推荐）**

- 双击 `启动系统.bat` 文件
- 脚本会自动构建前端并启动后端和前端服务

**方法二：手动启动**

1. 构建前端：
   ```bash
   cd frontend
   npm run build
   cd ..
   ```

2. 启动后端：
   ```bash
   python -m flask run
   ```

3. 启动前端开发服务器（可选，用于热重载）：
   ```bash
   cd frontend
   npm run dev
   cd ..
   ```

应用将运行在：
- 后端地址: http://localhost:5000
- 前端开发地址: http://localhost:5173
- 前端构建地址: http://localhost:5000

### 6. 停止应用

- 双击 `stop.bat` 文件
- 脚本会自动停止所有相关进程

## 使用指南

### 1. 登录/注册

- 访问 `http://localhost:5000` 进入登录页面
- 可以注册新用户，或使用默认管理员账号登录

### 2. 文生图功能

- 登录后进入主页面，选择"文生图"标签
- 输入图像描述，选择API，点击"生成图像"按钮
- 生成的图像将显示在下方

### 3. 图像编辑功能

- 选择"图像编辑"标签
- 上传一张图片，可选输入编辑提示词
- 选择API，点击"编辑图像"按钮
- 编辑前后的图像将并排显示

### 4. 管理员功能

- 以管理员身份登录后，点击"用户管理"按钮
- 可以查看所有用户列表，禁用/启用用户

## API接口

### 用户管理

- `POST /api/register`：注册新用户
- `POST /api/login`：用户登录
- `GET /api/logout`：用户注销
- `GET /api/admin/users`：获取所有用户列表（管理员权限）
- `PUT /api/admin/users/<user_id>`：更新用户状态（管理员权限）

### 图像处理

- `POST /api/generate`：文生图
- `POST /api/edit`：图像编辑

## 扩展建议

1. **添加真实大模型API**：替换模拟API为真实的大模型API
2. **添加更多图像处理功能**：如图像修复、超分辨率等
3. **优化前端界面**：使用现代前端框架如Vue 3的Composition API
4. **添加用户图像历史记录**：保存用户生成和编辑的图像
5. **添加更多管理员功能**：如用户权限管理、API使用统计等

## 注意事项

- 本项目使用的是模拟API，仅用于演示目的
- 在生产环境中，应使用真实的大模型API
- 应加强安全措施，如密码加密、API密钥管理等
- 确保MySQL服务已启动，且数据库配置正确
=======
# image-editor
>>>>>>> ae33cf25b5b0fb1fb24e1c37687da52c2bd260fa
