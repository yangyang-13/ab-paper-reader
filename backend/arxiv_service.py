import arxiv
from datetime import datetime, timedelta, timezone
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArxivService:
    """arXiv论文查询服务"""
    
    # AB测试相关的关键词（专业版）
    AB_TEST_KEYWORDS = [
        # AB测试核心词
        "A/B test", "AB test", "A/B testing", "AB testing",
        
        # 实验设计相关
        "randomized controlled trial", "online experiment",
        "controlled experiment", "randomized experiment",
        "experimental design", "online experimentation",
        "web experimentation", "digital experimentation",
        
        # 顺序测试和自适应实验
        "sequential testing", "sequential analysis",
        "multi-armed bandit", "adaptive experiment",
        "contextual bandit", "bandit algorithm",
        "thompson sampling", "upper confidence bound",
        
        # 因果推断
        "causal inference", "treatment effect",
        "average treatment effect", "heterogeneous treatment effect",
        "uplift modeling", "causal effect estimation",
        "difference-in-differences", "synthetic control",
        
        # 统计方法
        "variance reduction", "CUPED",
        "stratification", "regression adjustment",
        "sensitivity analysis", "power analysis",
        
        # 假设检验
        "hypothesis testing", "statistical significance",
        "multiple testing", "false discovery rate",
        "sequential probability ratio test",
        
        # 应用场景
        "conversion optimization", "personalization",
        "recommendation system experiment", "ranking experiment",
        "click-through rate optimization"
    ]
    
    @staticmethod
    def build_query() -> str:
        """构建arXiv搜索查询"""
        # 组合关键词，使用OR连接
        keyword_queries = [f'all:"{kw}"' for kw in ArxivService.AB_TEST_KEYWORDS]
        query = " OR ".join(keyword_queries)
        return query
    
    @staticmethod
    def fetch_papers(days_back: int = 1, max_results: int = 50) -> List[Dict]:
        """
        从arXiv获取最新的AB测试相关论文
        
        Args:
            days_back: 查询过去多少天的论文
            max_results: 最多返回多少篇论文
            
        Returns:
            论文列表
        """
        query = ArxivService.build_query()
        # 使用timezone-aware的datetime
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_back)
        
        logger.info(f"=" * 80)
        logger.info(f"开始查询arXiv论文")
        logger.info(f"查询关键词数量: {len(ArxivService.AB_TEST_KEYWORDS)}")
        logger.info(f"查询字符串: {query[:200]}...")
        logger.info(f"截止日期: {cutoff_date}")
        logger.info(f"最大结果数: {max_results * 3}")
        logger.info(f"=" * 80)
        
        try:
            # 使用arxiv API搜索
            search = arxiv.Search(
                query=query,
                max_results=max_results * 3,  # 查询更多结果，然后按日期过滤
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            count = 0
            total_checked = 0
            
            logger.info("开始遍历搜索结果...")
            
            for result in search.results():
                total_checked += 1
                
                # 每10篇打印一次进度
                if total_checked % 10 == 0:
                    logger.info(f"已检查 {total_checked} 篇论文，找到 {count} 篇符合条件")
                
                # 只保留最近发布的论文
                if result.published < cutoff_date:
                    logger.debug(f"跳过旧论文: {result.title[:50]}... (发布于 {result.published})")
                    continue
                
                if count >= max_results:
                    logger.info(f"已达到最大结果数 {max_results}，停止查询")
                    break
                    
                paper_data = {
                    'arxiv_id': result.entry_id.split('/')[-1],
                    'title': result.title,
                    'authors': ', '.join([author.name for author in result.authors]),
                    'abstract': result.summary,
                    'arxiv_url': result.entry_id,
                    'pdf_url': result.pdf_url,
                    'published_date': result.published,
                    'categories': result.categories
                }
                papers.append(paper_data)
                count += 1
                logger.info(f"✓ 找到论文 #{count}: {paper_data['title'][:80]}... (发布于 {result.published.date()})")
            
            logger.info(f"=" * 80)
            logger.info(f"查询完成！共检查 {total_checked} 篇，找到 {len(papers)} 篇符合条件的论文")
            logger.info(f"=" * 80)
            
            return papers
            
        except Exception as e:
            logger.error(f"❌ Error fetching papers from arXiv: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # 返回空列表而不是抛出异常
            return []
    
    @staticmethod
    def fetch_papers_by_date(target_date: datetime, max_results: int = 50) -> List[Dict]:
        """
        获取指定日期的论文
        
        Args:
            target_date: 目标日期
            max_results: 最多返回多少篇论文
            
        Returns:
            论文列表
        """
        query = ArxivService.build_query()
        
        logger.info(f"Searching arXiv for papers on date: {target_date.date()}")
        
        # 使用arxiv API搜索
        search = arxiv.Search(
            query=query,
            max_results=max_results * 2,  # 多查一些，然后过滤
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        # 使用timezone-aware的datetime
        if target_date.tzinfo is None:
            target_date = target_date.replace(tzinfo=timezone.utc)
        target_date_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        target_date_end = target_date_start + timedelta(days=1)
        
        for result in search.results():
            # 只保留目标日期的论文
            if target_date_start <= result.published < target_date_end:
                paper_data = {
                    'arxiv_id': result.entry_id.split('/')[-1],
                    'title': result.title,
                    'authors': ', '.join([author.name for author in result.authors]),
                    'abstract': result.summary,
                    'arxiv_url': result.entry_id,
                    'pdf_url': result.pdf_url,
                    'published_date': result.published,
                    'categories': result.categories
                }
                papers.append(paper_data)
                
                if len(papers) >= max_results:
                    break
        
        logger.info(f"Total papers found for {target_date.date()}: {len(papers)}")
        return papers
