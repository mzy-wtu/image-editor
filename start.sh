#!/bin/bash

# 图像编辑系统启动脚本 (Linux)

set -e

echo "=================================="
echo "   图像编辑系统启动脚本"
echo "=================================="
echo ""

# 检查Python虚拟环境
if [ ! -d "venv" ]; then
    echo "[1/4] 创建虚拟环境..."
    python3 -m venv venv
fi

echo "[1/4] 激活虚拟环境..."
source venv/bin/activate

echo "[2/4] 安装依赖..."
pip install -r requirements.txt -q

echo "[3/4] 初始化数据库..."
python app/db/create_db.py
python app/db/init_db.py

echo "[4/4] 启动服务..."
echo ""
echo "启动后端服务..."
nohup python -m flask run --host=0.0.0.0 --port=5000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

echo ""
echo "=================================="
echo "系统已启动!"
echo "后端地址: http://localhost:5000"
echo "前端地址: http://localhost:5000"
echo ""
echo "日志文件: backend.log"
echo "停止服务: kill $BACKEND_PID"
echo "=================================="

# 保存PID到文件
echo $BACKEND_PID > .backend.pid
