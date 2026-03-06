#!/usr/bin/env python3
"""测试不同AI服务提供商的配置"""

import sys
sys.path.insert(0, '/Users/yangyang/ply/backend')

# 模拟不同的环境变量配置
import os

print("=" * 80)
print("AI服务提供商配置测试")
print("=" * 80)
print()

# 测试1: OpenAI
print("【测试1】OpenAI配置")
print("-" * 80)
os.environ["AI_PROVIDER"] = "openai"
os.environ["AI_API_KEY"] = "sk-test-key"
os.environ.pop("AI_BASE_URL", None)
os.environ.pop("AI_MODEL", None)

from ai_service import AIService
service = AIService()
print(f"Provider: {service.provider}")
print(f"Model: {service.model}")
print(f"Base URL: {service.base_url}")
print()

# 测试2: 通义千问
print("【测试2】通义千问/Qwen配置")
print("-" * 80)
os.environ["AI_PROVIDER"] = "qwen"
os.environ["AI_API_KEY"] = "sk-test-key"
os.environ.pop("AI_BASE_URL", None)
os.environ.pop("AI_MODEL", None)

# 重新加载模块
import importlib
import ai_service as ai_module
importlib.reload(ai_module)
from ai_service import AIService

service = AIService()
print(f"Provider: {service.provider}")
print(f"Model: {service.model}")
print(f"Base URL: {service.base_url}")
print()

# 测试3: DeepSeek
print("【测试3】DeepSeek配置")
print("-" * 80)
os.environ["AI_PROVIDER"] = "deepseek"
os.environ["AI_API_KEY"] = "sk-test-key"

importlib.reload(ai_module)
from ai_service import AIService

service = AIService()
print(f"Provider: {service.provider}")
print(f"Model: {service.model}")
print(f"Base URL: {service.base_url}")
print()

# 测试4: 自定义配置
print("【测试4】自定义配置")
print("-" * 80)
os.environ["AI_PROVIDER"] = "custom"
os.environ["AI_API_KEY"] = "sk-test-key"
os.environ["AI_BASE_URL"] = "https://my-custom-api.com/v1"
os.environ["AI_MODEL"] = "my-custom-model"

importlib.reload(ai_module)
from ai_service import AIService

service = AIService()
print(f"Provider: {service.provider}")
print(f"Model: {service.model}")
print(f"Base URL: {service.base_url}")
print()

print("=" * 80)
print("✓ 所有配置测试完成")
print("=" * 80)
