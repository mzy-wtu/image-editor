from app import app
from app.api.user_api import user_bp
from app.api.image_api import image_bp
from flask import render_template, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
import os

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(image_bp)

# 静态文件路由 - 用于生产环境
export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')

@app.route('/')
def index():
    # 生产环境：返回Vue构建文件
    if os.path.exists(os.path.join(export_dir, 'index.html')):
        return send_from_directory(export_dir, 'index.html')
    # 开发环境：重定向到Vue开发服务器
    return redirect('http://localhost:5173')

@app.route('/login')
def login():
    # 生产环境：返回Vue构建文件
    if os.path.exists(os.path.join(export_dir, 'index.html')):
        return send_from_directory(export_dir, 'index.html')
    # 开发环境：重定向到Vue开发服务器
    return redirect('http://localhost:5173')

@app.route('/main')
@login_required
def main():
    # 生产环境：返回Vue构建文件
    if os.path.exists(os.path.join(export_dir, 'index.html')):
        return send_from_directory(export_dir, 'index.html')
    # 开发环境：重定向到Vue开发服务器
    return redirect('http://localhost:5173')

@app.route('/admin')
@login_required
def admin():
    # 生产环境：返回Vue构建文件
    if os.path.exists(os.path.join(export_dir, 'index.html')):
        return send_from_directory(export_dir, 'index.html')
    # 开发环境：重定向到Vue开发服务器
    return redirect('http://localhost:5173')

# 静态文件路由
@app.route('/<path:path>')
def static_file(path):
    if os.path.exists(os.path.join(export_dir, path)):
        return send_from_directory(export_dir, path)
    return redirect('http://localhost:5173/' + path)
