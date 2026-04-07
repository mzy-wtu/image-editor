# 图像编辑系统

基于大模型的图像编辑Web应用，支持文生图和图像编辑功能。

## 功能特点

- **用户管理**：注册、登录、权限控制
- **文生图**：通过文本描述生成图像
- **图像编辑**：上传图片并进行编辑
- **管理员功能**：管理用户列表，禁用/启用用户
- **大模型API**：支持千问、通义万相和模拟API

## 技术栈

- **后端**：Python 3.8+, Flask, Flask-Login, Flask-CORS, Flask-SQLAlchemy
- **前端**：Vue 3, Vite, Vue Router, Axios
- **数据库**：MySQL（默认）/ SQLite
- **图像处理**：Pillow
- **大模型**：DashScope（阿里云千问）

## 项目结构

```
image-editor/
├── app/                    # 后端应用
│   ├── api/                # API路由
│   │   ├── user_api.py     # 用户管理API
│   │   └── image_api.py    # 图像处理API
│   ├── models/             # 数据模型
│   │   └── user.py         # 用户模型
│   ├── utils/              # 工具函数
│   │   └── mock_api.py     # API实现（千问/通义/模拟）
│   ├── db/                 # 数据库脚本
│   │   ├── init_db.py      # 数据库初始化
│   │   └── create_db.py    # 数据库创建
│   ├── static/             # 静态文件（前端构建）
│   ├── __init__.py         # 应用初始化
│   ├── config.py           # 配置文件
│   └── routes.py           # 路由定义
├── frontend/               # 前端应用
│   ├── src/                # 源代码
│   ├── dist/               # 构建文件
│   ├── public/             # 公共文件
│   └── package.json        # 前端依赖
├── instance/               # 数据库存储
├── images/                 # 用户上传图像
├── requirements.txt        # Python依赖
├── .env.example            # 环境变量示例
├── start.bat               # Windows启动脚本
├── start.sh                # Linux启动脚本
├── stop.bat                # Windows停止脚本
└── README.md               # 项目说明
```

## 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 5.7+（默认）或 SQLite

## 快速部署（Linux云服务器）

### 1. 安装系统依赖

```bash
# CentOS/RHEL/Aliyun Linux
sudo yum install -y python38 gcc-c++ make

# Ubuntu/Debian
sudo apt update
sudo apt install python3-venv python3-pip gcc g++ make
```

### 2. 下载并配置项目

```bash
git clone https://github.com/mzy-wtu/image-editor.git
cd image-editor
```

### 3. 创建虚拟环境并安装依赖

```bash
python3.8 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install dashscope  # 阿里云千问SDK
```

### 4. 配置环境变量（可选）

```bash
cp .env.example .env
nano .env
```

### 5. 初始化数据库

```bash
python app/db/init_db.py
```

### 6. 构建前端

```bash
cd frontend
npm install
npm run build
cd ..
cp -r frontend/dist/* app/static/
```

### 7. 启动应用

```bash
python -m flask run --host=0.0.0.0 --port=5000
```

应用访问地址：http://你的服务器IP:5000

## 本地开发

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
cd ..
```

### 2. 配置数据库

编辑 `app/config.py` 或创建 `.env` 文件。

默认使用MySQL，需先创建数据库。

### 3. 初始化数据库

```bash
python app/db/init_db.py
```

### 4. 启动开发服务器

```bash
# Windows
start.bat

# Linux
./start.sh

# 或手动启动
python -m flask run --host=0.0.0.0
```

## 配置大模型API

### 千问API（API-1）

1. 获取阿里云DashScope API Key：https://dashscope.console.aliyun.com/
2. 在 `app/utils/mock_api.py` 中配置：

```python
self.api_key = os.getenv("DASHSCOPE_API_KEY", "your-api-key")
```

### 通义万相API（API-2）

在 `app/utils/mock_api.py` 中配置相应的API密钥。

## 默认账号

- 管理员：`admin` / `admin`

## API接口

### 用户管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/register` | POST | 注册新用户 |
| `/api/login` | POST | 用户登录 |
| `/api/logout` | GET | 用户注销 |
| `/api/admin/users` | GET | 获取用户列表（管理员） |
| `/api/admin/users/<id>` | PUT | 更新用户状态（管理员） |

### 图像处理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/generate` | POST | 文生图 |
| `/api/edit` | POST | 图像编辑 |

## 部署建议

1. **安全组开放端口**：云服务器需开放5000端口
2. **CORS配置**：如需跨域访问，在 `app/__init__.py` 中配置
3. **前端API地址**：前端默认连接 `http://localhost:5000`，部署时需修改为服务器IP
4. **生产部署**：建议使用Gunicorn + Nginx

## 注意事项

- 默认使用MySQL数据库，需确保MySQL服务已启动
- 千问/通义API需要有效的API密钥才能生成真实图像
- 生产环境中，请加强安全措施（修改默认密码、使用环境变量等）
- 如使用MySQL，请定期备份数据库