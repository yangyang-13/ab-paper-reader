from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging
from sqlalchemy.orm import Session

from models import SessionLocal, Paper
from arxiv_service import ArxivService
from ai_service import AIService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperScheduler:
    """论文自动抓取定时任务"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.arxiv_service = ArxivService()
        self.ai_service = AIService()
    
    def fetch_and_process_papers(self):
        """获取并处理论文的主任务"""
        logger.info(f"[{datetime.now()}] Starting scheduled paper fetch...")
        
        db: Session = SessionLocal()
        try:
            # 获取最近1天的论文
            papers = self.arxiv_service.fetch_papers(days_back=1, max_results=50)
            
            if not papers:
                logger.info("No new papers found.")
                return
            
            new_papers_count = 0
            
            for paper_data in papers:
                # 检查是否已存在
                existing = db.query(Paper).filter(
                    Paper.arxiv_id == paper_data['arxiv_id']
                ).first()
                
                if existing:
                    logger.info(f"Paper already exists: {paper_data['arxiv_id']}")
                    continue
                
                # 使用AI处理论文
                try:
                    ai_result = self.ai_service.process_paper(paper_data)
                except Exception as e:
                    logger.error(f"Error processing paper {paper_data['arxiv_id']}: {e}")
                    # 即使AI处理失败，也保存基本信息
                    ai_result = {
                        'summary_cn': '处理失败',
                        'interpretation': '处理失败',
                        'category': '其他'
                    }
                
                # 创建数据库记录
                paper = Paper(
                    arxiv_id=paper_data['arxiv_id'],
                    title=paper_data['title'],
                    authors=paper_data['authors'],
                    abstract=paper_data['abstract'],
                    summary_cn=ai_result['summary_cn'],
                    interpretation=ai_result['interpretation'],
                    category=ai_result['category'],
                    arxiv_url=paper_data['arxiv_url'],
                    pdf_url=paper_data['pdf_url'],
                    published_date=paper_data['published_date']
                )
                
                db.add(paper)
                new_papers_count += 1
                
                logger.info(f"Added new paper: {paper_data['title'][:100]}...")
            
            db.commit()
            logger.info(f"Successfully processed {new_papers_count} new papers.")
            
        except Exception as e:
            logger.error(f"Error in scheduled task: {e}")
            db.rollback()
        finally:
            db.close()
    
    def start(self):
        """启动定时任务"""
        # 每天早上9点执行
        self.scheduler.add_job(
            self.fetch_and_process_papers,
            'cron',
            hour=9,
            minute=0,
            id='daily_paper_fetch'
        )
        
        self.scheduler.start()
        logger.info("Scheduler started. Papers will be fetched daily at 9:00 AM.")
    
    def stop(self):
        """停止定时任务"""
        self.scheduler.shutdown()
        logger.info("Scheduler stopped.")
    
    def run_now(self):
        """立即执行一次任务"""
        logger.info("Running task immediately...")
        self.fetch_and_process_papers()

# 单例实例
scheduler_instance = PaperScheduler()

if __name__ == "__main__":
    # 测试运行
    scheduler = PaperScheduler()
    scheduler.run_now()
