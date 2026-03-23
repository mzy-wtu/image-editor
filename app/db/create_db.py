import pymysql

try:
    # 连接到MySQL服务器
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456'
    )
    
    # 创建游标
    cursor = connection.cursor()
    
    # 创建数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS image_editor CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print('数据库创建成功')
    
    # 关闭游标和连接
    cursor.close()
    connection.close()
    
    print('数据库创建完成')
except Exception as e:
    print(f'数据库创建失败: {str(e)}')
    print('请确保MySQL服务已启动，且连接信息正确')