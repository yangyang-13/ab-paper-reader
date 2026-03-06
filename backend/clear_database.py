#!/usr/bin/env python3
"""清空数据库中的论文数据"""

import sys
sys.path.insert(0, '/Users/yangyang/ply/backend')

from models import SessionLocal, Paper
from sqlalchemy import func

print("=" * 80)
print("清空论文数据库")
print("=" * 80)
print()

db = SessionLocal()

try:
    # 查询当前论文数量
    count = db.query(func.count(Paper.id)).scalar()
    print(f"当前数据库中有 {count} 篇论文")
    print()
    
    if count == 0:
        print("✓ 数据库已经是空的，无需清空")
    else:
        # 确认删除
        print(f"⚠️  警告：即将删除所有 {count} 篇论文数据！")
        print()
        
        # 删除所有论文
        deleted = db.query(Paper).delete()
        db.commit()
        
        print(f"✓ 成功删除 {deleted} 篇论文")
        
        # 验证
        remaining = db.query(func.count(Paper.id)).scalar()
        print(f"✓ 当前数据库中有 {remaining} 篇论文")
    
    print()
    print("=" * 80)
    print("操作完成")
    print("=" * 80)
    
except Exception as e:
    print(f"✗ 错误: {e}")
    db.rollback()
finally:
    db.close()
