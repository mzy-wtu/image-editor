from app import app, db
from app.models.user import User

with app.app_context():
    try:
        # 创建数据库表
        db.create_all()
        print('数据库表创建成功')
        
        # 检查是否已有管理员账号
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # 创建管理员账号
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print('管理员账号已创建: admin/admin')
        else:
            print('管理员账号已存在')
        
        print('数据库初始化完成')
    except Exception as e:
        print(f'数据库初始化失败: {str(e)}')
        print('请确保MySQL服务已启动，且数据库配置正确')