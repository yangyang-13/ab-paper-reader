from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import logging
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from models import Paper, init_db, get_db
from arxiv_service import ArxivService
from ai_service import AIService
from scheduler import scheduler_instance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AB测试论文阅读系统", version="2.1.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载前端静态文件
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")
    logger.info(f"✅ 前端静态文件已挂载: {frontend_path}")
else:
    logger.warning(f"⚠️ 前端目录不存在: {frontend_path}")

# 初始化数据库
init_db()

# 初始化服务
arxiv_service = ArxivService()
ai_service = AIService()

# 应用启动和关闭事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("=" * 80)
    logger.info("🚀 应用启动中...")
    logger.info("=" * 80)
    
    # 启动定时任务
    try:
        scheduler_instance.start()
        logger.info("✅ 定时任务已启动 - 每天早上9:00自动抓取论文")
    except Exception as e:
        logger.error(f"❌ 定时任务启动失败: {e}")
    
    logger.info("=" * 80)
    logger.info("✅ 应用启动完成")
    logger.info("=" * 80)

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    logger.info("=" * 80)
    logger.info("🛑 应用关闭中...")
    logger.info("=" * 80)
    
    # 停止定时任务
    try:
        scheduler_instance.stop()
        logger.info("✅ 定时任务已停止")
    except Exception as e:
        logger.error(f"❌ 定时任务停止失败: {e}")
    
    logger.info("=" * 80)
    logger.info("✅ 应用已关闭")
    logger.info("=" * 80)

@app.get("/")
def read_root():
    """根路径"""
    return {
        "message": "AB测试论文阅读系统API",
        "version": "1.0.0",
        "endpoints": {
            "papers": "/api/papers",
            "fetch": "/api/fetch",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
def health_check():
    """健康检查"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/papers")
def get_papers(
    date_from: Optional[str] = Query(None, description="开始日期，格式：YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="结束日期，格式：YYYY-MM-DD"),
    date: Optional[str] = Query(None, description="单个日期（兼容旧版），格式：YYYY-MM-DD"),
    category: Optional[str] = Query(None, description="论文分类"),
    marked_only: Optional[bool] = Query(False, description="只显示已标记的论文"),
    sort_by: Optional[str] = Query("date", description="排序方式：date(日期) 或 value(价值分)"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(50, ge=1, le=100, description="返回数量"),
    db: Session = Depends(get_db)
):
    """
    获取论文列表
    
    参数：
    - date_from: 可选，开始日期（YYYY-MM-DD格式）
    - date_to: 可选，结束日期（YYYY-MM-DD格式）
    - date: 可选，单个日期筛选（兼容旧版，YYYY-MM-DD格式）
    - category: 可选，按分类筛选
    - marked_only: 可选，只显示已标记的论文
    - sort_by: 可选，排序方式（date=按日期，value=按价值分）
    - skip: 跳过的记录数
    - limit: 返回的记录数
    """
    query = db.query(Paper)
    
    # 按日期范围筛选
    if date_from or date_to:
        try:
            # 如果只有开始日期，结束日期设为今天
            if date_from and not date_to:
                start_date = datetime.strptime(date_from, "%Y-%m-%d")
                end_date = datetime.now()
            # 如果只有结束日期，开始日期设为很早以前
            elif date_to and not date_from:
                start_date = datetime(2020, 1, 1)  # arXiv论文最早从2020年开始收录
                end_date = datetime.strptime(date_to, "%Y-%m-%d")
            # 如果都有，使用指定的范围
            else:
                start_date = datetime.strptime(date_from, "%Y-%m-%d")
                end_date = datetime.strptime(date_to, "%Y-%m-%d")
            
            # 结束日期加1天，使其包含当天
            end_date_inclusive = end_date + timedelta(days=1)
            
            query = query.filter(
                Paper.published_date >= start_date,
                Paper.published_date < end_date_inclusive
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
    # 兼容旧版单个日期查询
    elif date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
            next_date = target_date + timedelta(days=1)
            query = query.filter(
                Paper.published_date >= target_date,
                Paper.published_date < next_date
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，请使用YYYY-MM-DD格式")
    
    # 按分类筛选
    if category:
        query = query.filter(Paper.category == category)
    
    # 按标记状态筛选
    if marked_only:
        query = query.filter(Paper.is_marked == True)
    
    # 排序
    if sort_by == "value":
        # 按价值分降序排序（需要在Python层面处理）
        # 先获取所有数据
        all_papers = query.all()
        
        # 按价值分排序
        import json
        def get_value_score(paper):
            if paper.platform_value:
                try:
                    value_data = json.loads(paper.platform_value)
                    return value_data.get('score', 0)
                except:
                    return 0
            return 0
        
        all_papers.sort(key=get_value_score, reverse=True)
        
        # 手动分页
        total = len(all_papers)
        papers = all_papers[skip:skip+limit]
    else:
        # 按发布日期降序排序（默认）
        query = query.order_by(Paper.published_date.desc())
        
        # 分页
        total = query.count()
        papers = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "papers": [paper.to_dict() for paper in papers]
    }

@app.get("/api/papers/{paper_id}")
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    """获取单篇论文详情"""
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    return paper.to_dict()

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    """获取所有分类"""
    categories = db.query(Paper.category).distinct().all()
    return {
        "categories": [cat[0] for cat in categories if cat[0]]
    }

@app.get("/api/dates")
def get_available_dates(db: Session = Depends(get_db)):
    """获取有论文的日期列表"""
    from sqlalchemy import func
    dates = db.query(
        func.date(Paper.published_date).label('date')
    ).distinct().order_by(func.date(Paper.published_date).desc()).all()
    
    return {
        "dates": [str(date[0]) for date in dates if date[0]]
    }

@app.patch("/api/papers/{paper_id}/mark")
def toggle_paper_mark(paper_id: int, db: Session = Depends(get_db)):
    """切换论文的标记状态"""
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    paper.is_marked = not paper.is_marked
    db.commit()
    
    return {
        "id": paper_id,
        "is_marked": paper.is_marked,
        "message": "标记成功" if paper.is_marked else "取消标记成功"
    }

@app.post("/api/fetch")
def fetch_latest_papers(
    days_back: int = Query(7, ge=1, le=90, description="查询过去多少天的论文"),
    db: Session = Depends(get_db)
):
    """
    手动触发获取最新论文
    
    参数：
    - days_back: 查询过去多少天的论文（默认7天，手动获取建议范围）
    """
    logger.info(f"Fetching papers from last {days_back} days...")
    
    try:
        # 从arXiv获取论文
        papers = arxiv_service.fetch_papers(days_back=days_back, max_results=50)
        
        if not papers:
            return {
                "message": "未找到新论文，这可能是因为最近没有发布相关论文",
                "count": 0
            }
        
        new_papers_count = 0
        processed_papers = []
        
        for paper_data in papers:
            # 检查是否已存在
            existing = db.query(Paper).filter(
                Paper.arxiv_id == paper_data['arxiv_id']
            ).first()
            
            if existing:
                logger.info(f"Paper already exists: {paper_data['arxiv_id']}")
                continue
            
            # 使用AI处理论文
            ai_result = ai_service.process_paper(paper_data)
            
            # 创建数据库记录（v2.0增强版）
            paper = Paper(
                arxiv_id=paper_data['arxiv_id'],
                title=paper_data['title'],
                title_cn=ai_result.get('title_cn'),
                authors=paper_data['authors'],
                abstract=paper_data['abstract'],
                summary_cn=ai_result['summary_cn'],
                interpretation=ai_result['interpretation'],
                structured_interpretation=ai_result.get('structured_interpretation'),
                mindmap=ai_result.get('mindmap'),
                platform_value=ai_result.get('platform_value'),
                category=ai_result['category'],
                arxiv_url=paper_data['arxiv_url'],
                pdf_url=paper_data['pdf_url'],
                published_date=paper_data['published_date'],
                is_marked=False
            )
            
            db.add(paper)
            new_papers_count += 1
            processed_papers.append(paper_data['title'])
            
            logger.info(f"Added new paper: {paper_data['title'][:100]}...")
        
        db.commit()
        
        return {
            "message": f"成功获取并处理了 {new_papers_count} 篇新论文",
            "count": new_papers_count,
            "papers": processed_papers
        }
        
    except Exception as e:
        logger.error(f"Error fetching papers: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"获取论文失败：{str(e)}。arXiv API可能暂时不可用，请稍后重试。"
        )

@app.get("/api/stats")
def get_statistics(db: Session = Depends(get_db)):
    """获取统计信息"""
    from sqlalchemy import func
    
    total_papers = db.query(func.count(Paper.id)).scalar()
    
    category_stats = db.query(
        Paper.category,
        func.count(Paper.id).label('count')
    ).group_by(Paper.category).all()
    
    return {
        "total_papers": total_papers,
        "category_distribution": {
            cat: count for cat, count in category_stats if cat
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
