# 图像编辑系统

基于大模型的AI图像生成与编辑Web应用，支持文生图和图像编辑功能，提供现代化UI和高级参数控制。

## ✨ 功能特点

### 核心功能
- **用户管理**：注册、登录、权限控制
- **文生图**：通过文本描述生成图像，支持批量生成（1-4张）
- **图像编辑**：上传图片并进行AI编辑
- **管理员功能**：管理用户列表，禁用/启用用户
- **多模型支持**：千问、通义万相和模拟API

### 🎨 前端特性
- **现代化UI**：渐变背景、毛玻璃效果、圆角卡片设计
- **深色/浅色主题**：一键切换主题模式
- **提示词模板**：4种预设风格（写实、动漫、水彩、赛博朋克）
- **高级参数控制**：
  - 图像尺寸选择（正方形/竖版/横版）
  - 生成数量滑块（1-4张）
  - 负面提示词输入
  - 随机种子控制
- **拖拽上传**：支持点击和拖拽上传图像
- **图像网格展示**：悬停操作栏、全屏预览、一键下载
- **响应式布局**：适配不同屏幕尺寸

## 🛠 技术栈

### 后端
- **框架**：Python 3.8+, Flask
- **扩展**：Flask-Login, Flask-CORS, Flask-SQLAlchemy
- **数据库**：MySQL（默认）/ SQLite
- **图像处理**：Pillow
- **AI模型**：DashScope（阿里云千问）

### 前端
- **框架**：Vue 3 (Composition API)
- **构建工具**：Vite
- **路由**：Vue Router
- **HTTP客户端**：Axios
- **样式**：原生CSS（渐变、动画、响应式）

## 📁 项目结构

```
image-editor/
├── app/                          # 后端应用
│   ├── api/                      # API路由
│   │   ├── user_api.py           # 用户管理API
│   │   └── image_api.py          # 图像处理API（支持批量生成）
│   ├── models/                   # 数据模型
│   │   ├── user.py               # 用户模型
│   │   └── image_record.py       # 图像记录模型（含高级参数）
│   ├── utils/                    # 工具函数
│   │   └── image_generator.py    # AI图像生成器（千问/通义/模拟）
│   ├── services/                 # 业务逻辑层
│   ├── configs/                  # 配置模块
│   ├── db/                       # 数据库脚本
│   │   ├── init_db.py            # 数据库初始化
│   │   ├── create_db.py          # 数据库创建
│   │   └── migrate_add_params.py # 参数字段迁移脚本
│   ├── static/                   # 静态文件（前端构建输出）
│   ├── __init__.py               # 应用初始化
│   ├── config.py                 # 配置文件
│   └── routes.py                 # 路由定义
├── frontend/                     # 前端应用
│   ├── src/                      # 源代码
│   │   ├── views/                # 页面组件
│   │   │   └── MainView.vue      # 主界面（现代化UI）
│   │   ├── router/               # 路由配置
│   │   ├── App.vue               # 根组件
│   │   └── main.js               # 入口文件
│   ├── dist/                     # 构建输出
│   ├── public/                   # 公共资源
│   ├── package.json              # 前端依赖
│   └── vite.config.js            # Vite配置
├── instance/                     # 数据库存储
├── images/                       # 用户上传图像
├── requirements.txt              # Python依赖
├── .env.example                  # 环境变量示例
├── start.bat                     # Windows启动脚本
├── start.sh                      # Linux启动脚本
├── stop.bat                      # Windows停止脚本
├── FRONTEND_OPTIMIZATION.md      # 前端优化文档
├── PROJECT_STRUCTURE_ANALYSIS.md # 项目结构分析
└── README.md                     # 项目说明
```

## 🚀 快速部署（Linux云服务器）

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

### 4. 配置环境变量

```bash
cp .env.example .env
nano .env
```

配置千问API密钥：
```
DASHSCOPE_API_KEY=your-api-key-here
```

### 5. 初始化数据库

```bash
# 创建数据库
python app/db/create_db.py

# 初始化表结构
python app/db/init_db.py

# 迁移新增字段（如果从旧版本升级）
python app/db/migrate_add_params.py
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

应用访问地址：`http://你的服务器IP:5000`

## 💻 本地开发

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

编辑 `app/config.py` 或创建 `.env` 文件：

```python
# MySQL配置（推荐）
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/image_editor'

# 或使用SQLite（开发环境）
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/image_editor.db'
```

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

前端开发模式（热重载）：
```bash
cd frontend
npm run dev
```

## 🔑 配置大模型API

### 千问API（推荐）

1. 获取阿里云DashScope API Key：https://dashscope.console.aliyun.com/
2. 在 `.env` 文件中配置：

```bash
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
```

3. 支持的参数：
   - `size`: 图像尺寸（1024*1024, 720*1280, 1280*720）
   - `negative_prompt`: 负面提示词
   - `seed`: 随机种子（可选）
   - `n`: 生成数量（1-4）

### 通义万相API

在 `app/utils/image_generator.py` 中配置相应的API密钥。

## 👤 默认账号

- **管理员**：`admin` / `admin`
- 首次登录后请修改密码

## 📡 API接口

### 用户管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/register` | POST | 注册新用户 |
| `/api/login` | POST | 用户登录 |
| `/api/logout` | GET | 用户注销 |
| `/api/admin/users` | GET | 获取用户列表（管理员） |
| `/api/admin/users/<id>` | PUT | 更新用户状态（管理员） |

### 图像处理

| 接口 | 方法 | 描述 | 参数 |
|------|------|------|------|
| `/api/generate` | POST | 文生图 | `prompt`, `api_choice`, `count`, `size`, `negativePrompt`, `seed` |
| `/api/edit` | POST | 图像编辑 | `prompt`, `api_choice`, `image` |

#### `/api/generate` 请求示例

```json
{
  "prompt": "一只可爱的猫咪",
  "api_choice": "api1",
  "count": 2,
  "size": "1024*1024",
  "negativePrompt": "模糊，低质量",
  "seed": 42
}
```

#### 响应示例

```json
{
  "images": [
    "data:image/png;base64,iVBORw0KG...",
    "data:image/png;base64,iVBORw0KG..."
  ],
  "image": "data:image/png;base64,iVBORw0KG...",
  "logs": ["生成成功"]
}
```

## 🗄️ 数据库结构

### image_record 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| user_id | INT | 用户ID |
| image_type | VARCHAR(20) | 类型（generate/edit） |
| prompt | TEXT | 提示词 |
| api_choice | VARCHAR(20) | API选择 |
| original_image | LONGBLOB | 原始图像（编辑时） |
| result_image | LONGBLOB | 结果图像 |
| file_path | VARCHAR(255) | 文件路径 |
| created_at | DATETIME | 创建时间 |
| **size** | VARCHAR(20) | 图像尺寸 |
| **negative_prompt** | TEXT | 负面提示词 |
| **seed** | INT | 随机种子 |
| **generation_count** | INT | 生成数量 |

**注意**：粗体字段为新增字段，需要运行迁移脚本。

## 🔄 数据库迁移

如果从旧版本升级，需要执行迁移脚本添加新字段：

```bash
python app/db/migrate_add_params.py
```

迁移内容：
- 添加 `size` 字段（默认 '1024*1536'）
- 添加 `negative_prompt` 字段
- 添加 `seed` 字段
- 添加 `generation_count` 字段
- 升级 `result_image` 和 `original_image` 为 LONGBLOB（支持大图）

## 🎯 使用指南

### 文生图流程

1. 在左侧输入提示词或点击 **📝 模板** 选择预设模板
2. 可选：输入负面提示词（不想要的元素）
3. 选择模型（千问/通义/模拟）
4. 选择图像尺寸（正方形/竖版/横版）
5. 调整生成数量（1-4张）
6. 可选：设置随机种子（固定生成结果）
7. 点击 **🚀 开始生成**
8. 生成的图像显示在右侧网格中
9. 悬停图像可下载或全屏预览

### 图像编辑流程

1. 点击或拖拽上传图像
2. 输入编辑指令（如"把背景改成蓝天"）
3. 选择模型
4. 点击 **🎨 开始编辑**
5. 查看原图和编辑后的对比

### 主题切换

点击顶部导航栏的 🌙/☀️ 图标切换深色/浅色主题。

## 🚀 生产部署建议

### 1. 使用Gunicorn + Nginx

```bash
# 安装Gunicorn
pip install gunicorn

# 启动应用
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### 2. Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /root/workspace/image-editor/app/static;
    }
}
```

### 3. 安全建议

- 修改默认管理员密码
- 使用环境变量存储敏感信息（API密钥、数据库密码）
- 配置HTTPS证书
- 开启防火墙，仅开放必要端口
- 定期备份数据库
- 限制上传文件大小和类型

### 4. 性能优化

- 使用Redis缓存会话
- 配置CDN加速静态资源
- 启用Gzip压缩
- 图像懒加载和压缩

## 📚 文档

- [前端优化文档](FRONTEND_OPTIMIZATION.md) - 详细的功能清单和开发进度
- [项目结构分析](PROJECT_STRUCTURE_ANALYSIS.md) - 项目架构和代码组织

## 🐛 故障排查

### 1. 数据库连接失败

```bash
# 检查MySQL服务状态
sudo systemctl status mysql

# 检查数据库是否存在
mysql -u root -p -e "SHOW DATABASES;"
```

### 2. 图像生成失败（500错误）

- 检查API密钥是否配置正确
- 查看 `result_image` 字段是否为 LONGBLOB 类型
- 检查日志：`tail -f /var/log/flask.log`

### 3. 前端无法访问后端

- 检查CORS配置（`app/__init__.py`）
- 确认安全组已开放5000端口
- 检查防火墙规则

### 4. 前端构建失败

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

- GitHub: https://github.com/mzy-wtu/image-editor
- Issues: https://github.com/mzy-wtu/image-editor/issues

---

**更新日志**

- **2026-04-07**: 前端UI现代化改造，添加高级参数支持，实现批量生成功能
- **2026-04-06**: 修复数据库容量问题，升级为LONGBLOB
- **初始版本**: 基础文生图和图像编辑功能
