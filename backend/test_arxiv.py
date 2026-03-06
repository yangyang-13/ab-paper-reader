#!/usr/bin/env python3
"""测试arXiv API，检查是否能正常返回论文"""

import sys
sys.path.insert(0, '/Users/yangyang/ply/backend')

from arxiv_service import ArxivService
from datetime import datetime

print("=" * 80)
print("arXiv API 测试脚本")
print("=" * 80)
print()

# 测试1: 使用通用关键词 "machine learning"
print("【测试1】使用通用关键词: machine learning")
print("-" * 80)

import arxiv

query = 'all:"machine learning"'
print(f"查询字符串: {query}")
print(f"查询最近30天的论文...")
print()

try:
    search = arxiv.Search(
        query=query,
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    count = 0
    for result in search.results():
        count += 1
        print(f"{count}. {result.title[:80]}")
        print(f"   发布日期: {result.published.date()}")
        print(f"   arXiv ID: {result.entry_id.split('/')[-1]}")
        print()
        
        if count >= 5:
            break
    
    print(f"✓ 成功获取到 {count} 篇论文")
    print()
    
except Exception as e:
    print(f"✗ 错误: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
print()

# 测试2: 使用我们的AB测试关键词
print("【测试2】使用AB测试关键词")
print("-" * 80)

service = ArxivService()
print(f"关键词数量: {len(service.AB_TEST_KEYWORDS)}")
print(f"关键词列表: {service.AB_TEST_KEYWORDS[:5]}...")
print()

papers = service.fetch_papers(days_back=30, max_results=10)

print()
print(f"结果: 找到 {len(papers)} 篇论文")

if papers:
    print()
    print("前5篇论文:")
    for i, paper in enumerate(papers[:5], 1):
        print(f"{i}. {paper['title'][:80]}")
        print(f"   发布日期: {paper['published_date'].date()}")
        print()

print("=" * 80)
