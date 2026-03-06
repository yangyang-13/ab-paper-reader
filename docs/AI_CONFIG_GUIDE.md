# AI服务多提供商支持 - 配置示例

本文档提供各AI服务商的详细配置示例，让您快速切换使用不同的AI服务。

## 配置文件位置

编辑 `backend/.env` 文件进行配置。

## 🚀 快速开始

### 方案1: 使用通义千问（推荐国内用户）

**优势**: 价格便宜、速度快、中文能力强、无需科学上网

1. 获取API Key: https://dashscope.aliyuncs.com/
2. 配置 `.env`:

```bash
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxxxxxxxxxxxxx
```

完成！系统会自动使用 `qwen-plus` 模型和正确的API端点。

### 方案2: 使用DeepSeek（最便宜）

**优势**: 价格极低、中文能力强

1. 获取API Key: https://platform.deepseek.com/
2. 配置 `.env`:

```bash
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxxxxxxxxxxxxxx
```

### 方案3: 使用OpenAI（默认）

**优势**: 模型质量最好、生态最成熟

1. 获取API Key: https://platform.openai.com/
2. 配置 `.env`:

```bash
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxxxxxxxxxxxxx
```

## 📋 完整配置示例

### OpenAI

```bash
# backend/.env
AI_PROVIDER=openai
AI_API_KEY=sk-proj-xxxxxx

# 可选：指定模型（默认 gpt-4o-mini）
AI_MODEL=gpt-4o-mini

# 可选模型：
# - gpt-4o-mini (推荐，性价比高)
# - gpt-4 (质量最好，较贵)
# - gpt-3.5-turbo (经济实惠)
```

### 通义千问 (Qwen)

```bash
# backend/.env
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxx  # 从阿里云DashScope获取

# 可选：指定模型（默认 qwen-plus）
AI_MODEL=qwen-plus

# 可选模型：
# - qwen-plus (推荐，平衡性能和成本)
# - qwen-turbo (速度快，成本低)
# - qwen-max (最强性能)
# - qwen-long (长文本处理)
```

### DeepSeek

```bash
# backend/.env
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxxx

# 可选：指定模型（默认 deepseek-chat）
AI_MODEL=deepseek-chat
```

### Moonshot (Kimi)

```bash
# backend/.env
AI_PROVIDER=moonshot
AI_API_KEY=sk-xxxxxx

# 可选：指定模型（默认 moonshot-v1-8k）
AI_MODEL=moonshot-v1-8k

# 可选模型：
# - moonshot-v1-8k (8K上下文)
# - moonshot-v1-32k (32K上下文)
# - moonshot-v1-128k (128K上下文)
```

### 智谱AI (GLM)

```bash
# backend/.env
AI_PROVIDER=glm
AI_API_KEY=xxxxxx.xxxxxx

# 可选：指定模型（默认 glm-4）
AI_MODEL=glm-4

# 可选模型：
# - glm-4 (最新版本)
# - glm-4-flash (快速版本)
# - glm-3-turbo (经济版本)
```

### 自定义服务（兼容OpenAI接口）

如果您使用的是其他兼容OpenAI接口的服务（本地部署、代理等）：

```bash
# backend/.env
AI_PROVIDER=custom
AI_API_KEY=your-api-key
AI_BASE_URL=https://your-api-endpoint.com/v1
AI_MODEL=your-model-name
```

## 🔄 切换服务商

1. 编辑 `backend/.env` 文件
2. 修改 `AI_PROVIDER` 和 `AI_API_KEY`
3. 重启服务：
   ```bash
   ./start.sh  # Linux/Mac
   # 或
   start.bat   # Windows
   ```

## 💰 成本对比（处理1000篇论文）

| 服务商 | 模型 | 估算成本(¥) | 速度 | 质量 |
|--------|------|------------|------|------|
| DeepSeek | deepseek-chat | 2 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 通义千问 | qwen-turbo | 4 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 通义千问 | qwen-plus | 10 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| OpenAI | gpt-4o-mini | 20 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| OpenAI | gpt-4 | 200 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎯 推荐配置

**个人学习/开发**:
```bash
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxxx
```
理由：成本极低，适合高频调用和测试

**生产环境（国内）**:
```bash
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxx
AI_MODEL=qwen-plus
```
理由：平衡成本和质量，速度快，稳定性好

**生产环境（海外）**:
```bash
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxx
AI_MODEL=gpt-4o-mini
```
理由：质量最好，生态成熟

**追求最高质量**:
```bash
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxx
AI_MODEL=gpt-4
```
理由：最强大的语言模型

## 🔧 高级配置

### 1. 自定义API端点

如果您需要通过代理或自定义端点访问：

```bash
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxx
AI_BASE_URL=https://your-proxy.com/v1
```

### 2. 混合使用多个key

虽然系统同时只能使用一个provider，但您可以准备多个配置文件：

```bash
# .env.openai
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxx

# .env.qwen
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxx

# .env.deepseek
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxxx
```

切换时：
```bash
cp .env.qwen .env
./start.sh
```

## ❓ 常见问题

### Q: 我应该选择哪个服务商？

**如果您在国内**:
- 首选：通义千问 (qwen) - 速度快、价格合理
- 备选：DeepSeek - 价格最低

**如果您在海外**:
- 首选：OpenAI - 质量最好
- 备选：DeepSeek - 价格最低

### Q: 如何获取API Key？

每个服务商的获取方式：

1. **OpenAI**: https://platform.openai.com/api-keys
2. **通义千问**: https://dashscope.aliyuncs.com/ → API-KEY管理
3. **DeepSeek**: https://platform.deepseek.com/ → API Keys
4. **Moonshot**: https://platform.moonshot.cn/ → API Keys
5. **智谱AI**: https://open.bigmodel.cn/ → API Keys

### Q: API Key是否安全？

**重要**：
- ✅ .env文件已在 .gitignore 中，不会提交到Git
- ✅ 不要在代码中硬编码API Key
- ✅ 不要分享您的.env文件
- ✅ 定期轮换API Key

### Q: 遇到"API Key无效"错误怎么办？

1. 检查API Key是否正确复制（无多余空格）
2. 检查账户是否有余额
3. 检查API Key权限是否正确
4. 某些服务商的Key有前缀要求（如sk-）

### Q: 可以本地部署模型吗？

可以！使用 `custom` provider配置本地模型服务：

```bash
AI_PROVIDER=custom
AI_API_KEY=dummy-key
AI_BASE_URL=http://localhost:8080/v1
AI_MODEL=your-local-model
```

前提：您的本地服务需要兼容OpenAI API格式。

## 📞 获取帮助

- 查看日志: `tail -f backend/server.log`
- 测试配置: `python3 backend/test_ai_providers.py`
- 详细文档: `docs/AI_PROVIDERS.md`
