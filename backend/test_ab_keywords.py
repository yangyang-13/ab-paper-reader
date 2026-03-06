#!/usr/bin/env python3
"""测试AB测试关键词能找到多少论文"""

import sys
sys.path.insert(0, '/Users/yangyang/ply/backend')

import arxiv
from datetime import datetime, timedelta, timezone

print("=" * 80)
print("AB测试关键词效果分析")
print("=" * 80)
print()

# AB测试专用关键词（不含通用词）
ab_keywords = [
    "A/B test", "AB test", "A/B testing", "AB testing",
    "randomized controlled trial", "online experiment",
    "controlled experiment", "randomized experiment",
    "experimental design", "online experimentation",
    "sequential testing", 
    "multi-armed bandit", "adaptive experiment",
    "contextual bandit", "bandit algorithm",
    "causal inference", "treatment effect",
    "uplift modeling", 
    "variance reduction",
    "hypothesis testing",
]

print(f"AB测试关键词数量: {len(ab_keywords)}")
print(f"关键词: {ab_keywords[:5]}...")
print()

# 构建查询
query = " OR ".join([f'all:"{kw}"' for kw in ab_keywords])

# 测试1: 不限时间，看总共有多少
print("【测试1】查询所有时间的AB测试论文（前10篇）")
print("-" * 80)

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
        print(f"{count}. {result.title[:70]}")
        print(f"   发布日期: {result.published.date()}")
        print(f"   类别: {result.categories[:3]}")
        print()
    
    print(f"✓ 找到 {count} 篇论文")
    
except Exception as e:
    print(f"✗ 错误: {e}")

print()
print("=" * 80)

# 测试2: 查询最近30天
print("【测试2】查询最近30天的AB测试论文")
print("-" * 80)

cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)
print(f"截止日期: {cutoff_date.date()}")
print()

try:
    search = arxiv.Search(
        query=query,
        max_results=100,  # 多查一些
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    count = 0
    recent_count = 0
    
    for result in search.results():
        count += 1
        if result.published >= cutoff_date:
            recent_count += 1
            if recent_count <= 5:
                print(f"{recent_count}. {result.title[:70]}")
                print(f"   发布日期: {result.published.date()}")
                print()
    
    print(f"总共检查: {count} 篇")
    print(f"最近30天: {recent_count} 篇")
    
except Exception as e:
    print(f"✗ 错误: {e}")

print()
print("=" * 80)

# 测试3: 测试单个关键词
print("【测试3】测试各个关键词的效果")
print("-" * 80)

test_keywords = [
    "A/B test",
    "multi-armed bandit",
    "causal inference",
    "randomized controlled trial",
    "online experiment"
]

for kw in test_keywords:
    query = f'all:"{kw}"'
    try:
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        results = list(search.results())
        print(f"'{kw}': {len(results)} 篇")
        if results:
            print(f"  最新: {results[0].published.date()}")
    except Exception as e:
        print(f"'{kw}': 错误 - {e}")

print()
print("=" * 80)
