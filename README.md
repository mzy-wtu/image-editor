# 图像编辑系统

基于大模型的图像编辑Web应用，支持文生图和图像编辑功能。

## 功能特点

- **用户管理**：注册、登录、权限控制
- **文生图**：通过文本描述生成图像
- **图像编辑**：上传图片并进行编辑
- **管理员功能**：管理用户列表，禁用/启用用户
- **模拟API**：提供三个模拟大模型API接口

## 技术栈

- **后端**：Python, Flask, Flask-Login, Flask-CORS, Flask-SQLAlchemy
- **前端**：Vue 3, Vite, Vue Router, Axios
- **数据库**：MySQL
- **图像处理**：Pillow

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
│   │   └── mock_api.py     # 模拟API实现
│   ├── db/                 # 数据库脚本
│   │   ├── init_db.py      # 数据库初始化
│   │   └── create_db.py    # 数据库创建
│   ├── __init__.py         # 应用初始化
│   ├── config.py           # 配置文件
│   └── routes.py           # 路由定义
├── frontend/               # 前端应用
│   ├── src/                # 源代码
│   ├── public/             # 公共文件
│   └── package.json        # 前端依赖
├── instance/               # 实例文件夹（SQLite备选）
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
- MySQL 5.7+ 或 SQLite（开发用）

## 快速部署（Linux云服务器）

### 1. 安装系统依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-venv python3-pip mysql-server nodejs npm

# CentOS/RHEL
sudo yum install python3-venv python3-pip mysql-server nodejs npm
```

### 2. 配置MySQL

```bash
sudo mysql
```

在MySQL终端中执行：

```sql
CREATE DATABASE image_editor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'image_editor'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON image_editor.* TO 'image_editor'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. 下载并配置项目

```bash
git clone https://github.com/mzy-wtu/image-editor.git
cd image-editor
```

### 4. 创建虚拟环境并安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件，修改数据库连接信息
nano .env
```

### 6. 构建前端

```bash
cd frontend
npm install
npm run build
cd ..
```

### 7. 初始化数据库

```bash
python app/db/create_db.py
python app/db/init_db.py
```

### 8. 启动应用

```bash
chmod +x start.sh
./start.sh
```

应用将运行在：
- 后端地址: http://localhost:5000
- 前端地址: http://localhost:5000

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

编辑 `app/config.py` 或创建 `.env` 文件配置数据库连接。

### 3. 初始化数据库

```bash
python app/db/create_db.py
python app/db/init_db.py
```

### 4. 启动开发服务器

```bash
# Windows
start.bat

# Linux
./start.sh

# 或手动启动
# 终端1: 启动后端
python -m flask run --host=0.0.0.0

# 终端2: 启动前端热重载
cd frontend
npm run dev
```

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

## 扩展建议

1. **添加真实大模型API**：替换模拟API为真实的大模型API
2. **添加更多图像处理功能**：如图像修复、超分辨率等
3. **添加用户图像历史记录**：保存用户生成和编辑的图像
4. **添加更多管理员功能**：如用户权限管理、API使用统计等
5. **部署优化**：使用Gunicorn/Nginx进行生产部署

## 注意事项

- 本项目使用的是模拟API，仅用于演示目的
- 生产环境中，请使用真实的大模型API并加强安全措施
- 确保MySQL服务已启动，且数据库配置正确
- 请修改默认管理员密码
