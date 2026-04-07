import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def migrate():
    """添加高级参数字段到image_record表"""
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "123456"),
        database=os.getenv("DB_NAME", "image_editor")
    )
    
    try:
        with connection.cursor() as cursor:
            # 添加新字段
            sqls = [
                "ALTER TABLE image_record ADD COLUMN size VARCHAR(20) DEFAULT '1024*1536'",
                "ALTER TABLE image_record ADD COLUMN negative_prompt TEXT",
                "ALTER TABLE image_record ADD COLUMN seed INT",
                "ALTER TABLE image_record ADD COLUMN generation_count INT DEFAULT 1"
            ]
            
            for sql in sqls:
                try:
                    cursor.execute(sql)
                    print(f"✓ 执行成功: {sql[:50]}...")
                except pymysql.err.OperationalError as e:
                    if "Duplicate column name" in str(e):
                        print(f"⊙ 字段已存在，跳过: {sql[:50]}...")
                    else:
                        raise
        
        connection.commit()
        print("\n✅ 数据库迁移完成！")
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        connection.rollback()
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    migrate()
