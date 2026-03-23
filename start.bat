@echo off

REM 图像编辑系统启动脚本 (Windows)

cls
echo ==================================
echo    图像编辑系统启动脚本
echo ==================================
echo.

REM 检查前端目录
if not exist "frontend" (
    echo 错误: 前端目录不存在
    pause
    exit /b 1
)

REM 检查或创建虚拟环境
if not exist "venv" (
    echo [1/5] 创建虚拟环境...
    python -m venv venv
) else (
    echo [1/5] 虚拟环境已存在...
)

echo [2/5] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo [3/5] 初始化数据库...
python app\db\create_db.py
python app\db\init_db.py

echo [4/5] 安装前端依赖...
cd frontend
if not exist "node_modules" (
    call npm install
)
cd ..

echo [5/5] 启动服务...
echo.
echo 启动后端服务...
start "Flask Backend" cmd /k "venv\Scripts\python.exe -m flask run --host=localhost"

echo 启动前端开发服务器...
start "Vue Frontend" cmd /k "cd frontend ^&^& npm run dev"

echo.
echo ==================================
echo 系统已启动!
echo 后端地址: http://localhost:5000
echo 前端地址: http://localhost:5173
echo ==================================
echo.
pause
