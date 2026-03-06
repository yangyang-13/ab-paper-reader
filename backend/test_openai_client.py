#!/usr/bin/env python3
"""测试OpenAI客户端初始化"""

from openai import OpenAI
import os

# 测试基本初始化
print("测试1: 基本初始化")
try:
    client = OpenAI(api_key="test-key")
    print("✓ 成功")
except Exception as e:
    print(f"✗ 失败: {e}")

# 测试带base_url初始化
print("\n测试2: 带base_url初始化")
try:
    client = OpenAI(
        api_key="test-key",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    print("✓ 成功")
    print(f"Base URL: {client.base_url}")
except Exception as e:
    print(f"✗ 失败: {e}")
