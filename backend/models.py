from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Paper(Base):
    """论文数据模型 - v2.0"""
    __tablename__ = 'papers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    arxiv_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # 基本信息
    title = Column(String(500), nullable=False)
    title_cn = Column(String(500))  # 中文标题
    authors = Column(Text)
    abstract = Column(Text)
    
    # AI生成内容
    summary_cn = Column(Text)  # 中文摘要
    interpretation = Column(Text)  # 原始论文解读（保留兼容）
    structured_interpretation = Column(Text)  # 结构化解读（JSON格式）
    mindmap = Column(Text)  # 思维导图数据（JSON格式）
    platform_value = Column(Text)  # 平台价值分析（JSON格式：判断+价值点）
    
    # 分类和链接
    category = Column(String(100))  # 论文分类
    arxiv_url = Column(String(200))
    pdf_url = Column(String(200))
    
    # 用户交互
    is_marked = Column(Boolean, default=False, index=True)  # 是否标记
    
    # 时间戳
    published_date = Column(DateTime, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        import json
        
        # 解析JSON字段
        structured_interp = None
        if self.structured_interpretation:
            try:
                structured_interp = json.loads(self.structured_interpretation)
            except:
                pass
        
        mindmap_data = None
        if self.mindmap:
            try:
                mindmap_data = json.loads(self.mindmap)
            except:
                pass
        
        platform_value_data = None
        if self.platform_value:
            try:
                platform_value_data = json.loads(self.platform_value)
            except:
                pass
        
        return {
            'id': self.id,
            'arxiv_id': self.arxiv_id,
            'title': self.title,
            'title_cn': self.title_cn,
            'authors': self.authors,
            'abstract': self.abstract,
            'summary_cn': self.summary_cn,
            'interpretation': self.interpretation,
            'structured_interpretation': structured_interp,
            'mindmap': mindmap_data,
            'platform_value': platform_value_data,
            'category': self.category,
            'arxiv_url': self.arxiv_url,
            'pdf_url': self.pdf_url,
            'is_marked': self.is_marked,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

# 数据库配置
DATABASE_URL = "sqlite:///./papers.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
