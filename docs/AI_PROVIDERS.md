# AI服务配置指南

本项目支持多种AI服务提供商，包括OpenAI、通义千问、DeepSeek、Moonshot等。

## 快速配置

编辑 `backend/.env` 文件，设置以下环境变量：

```bash
# 选择AI服务提供商
AI_PROVIDER=qwen  # 或 openai, deepseek, moonshot, glm

# 设置API密钥
AI_API_KEY=your-api-key-here
```

## 支持的AI服务商

### 1. OpenAI (默认)

```bash
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxxxxxxxxx
AI_MODEL=gpt-4o-mini  # 可选: gpt-4, gpt-3.5-turbo
```

**获取API Key**: https://platform.openai.com/api-keys

**推荐模型**:
- `gpt-4o-mini`: 性价比高，速度快
- `gpt-4`: 质量最好，但较贵
- `gpt-3.5-turbo`: 经济实惠

---

### 2. 通义千问 (Qwen) - 阿里云

```bash
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxxxxxxxxx
AI_MODEL=qwen-plus  # 可选: qwen-turbo, qwen-max, qwen-long
```

**获取API Key**: https://dashscope.aliyuncs.com/

**推荐模型**:
- `qwen-plus`: 平衡性能和成本
- `qwen-turbo`: 速度快，成本低
- `qwen-max`: 最强性能
- `qwen-long`: 长文本处理

**定价**: 比OpenAI便宜很多，适合国内用户

---

### 3. DeepSeek

```bash
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxxxxxxxxxx
AI_MODEL=deepseek-chat
```

**获取API Key**: https://platform.deepseek.com/

**特点**:
- 价格极低（比OpenAI便宜10倍以上）
- 中文能力强
- 适合高频调用

---

### 4. Moonshot (Kimi)

```bash
AI_PROVIDER=moonshot
AI_API_KEY=sk-xxxxxxxxxxxxx
AI_MODEL=moonshot-v1-8k  # 可选: moonshot-v1-32k, moonshot-v1-128k
```

**获取API Key**: https://platform.moonshot.cn/

**推荐模型**:
- `moonshot-v1-8k`: 标准版本
- `moonshot-v1-32k`: 长上下文
- `moonshot-v1-128k`: 超长上下文

---

### 5. 智谱AI (GLM)

```bash
AI_PROVIDER=glm
AI_API_KEY=xxxxxxxxxxxxx
AI_MODEL=glm-4
```

**获取API Key**: https://open.bigmodel.cn/

**推荐模型**:
- `glm-4`: 最新版本
- `glm-4-flash`: 快速版本
- `glm-3-turbo`: 经济版本

---

### 6. 自定义服务（兼容OpenAI接口）

如果您使用的是其他兼容OpenAI接口的服务（如本地部署的模型、代理服务等）：

```bash
AI_PROVIDER=custom
AI_API_KEY=your-key
AI_BASE_URL=https://your-api-endpoint.com/v1
AI_MODEL=your-model-name
```

## 配置示例

### 示例1: 使用通义千问（推荐国内用户）

```bash
# backend/.env
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxx  # 从阿里云DashScope获取
AI_MODEL=qwen-plus
```

### 示例2: 使用DeepSeek（最经济）

```bash
# backend/.env
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxxx
AI_MODEL=deepseek-chat
```

### 示例3: 使用OpenAI（质量最好）

```bash
# backend/.env
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxxx
AI_MODEL=gpt-4o-mini
```

## 成本对比

基于处理1000篇论文的估算（每篇约2000 tokens）：

| 服务商 | 模型 | 估算成本 | 相对比例 |
|--------|------|---------|---------|
| DeepSeek | deepseek-chat | ¥2 | 1x |
| 通义千问 | qwen-plus | ¥10 | 5x |
| 通义千问 | qwen-turbo | ¥4 | 2x |
| OpenAI | gpt-4o-mini | ¥20 | 10x |
| OpenAI | gpt-4 | ¥200 | 100x |

**建议**:
- 个人学习/测试: DeepSeek 或 qwen-turbo
- 生产环境（国内）: qwen-plus
- 追求最高质量: gpt-4o-mini 或 gpt-4

## 测试配置

配置完成后，重启服务：

```bash
# 停止现有服务
lsof -ti:8000 | xargs kill -9

# 启动服务
cd backend && python3 main.py
```

查看日志，确认AI服务初始化成功：

```
✓ AI服务已初始化: qwen (qwen-plus) at https://dashscope.aliyuncs.com/compatible-mode/v1
```

## 常见问题

### Q: 如何选择合适的服务商？

**国内用户推荐**: 通义千问 (qwen) 或 DeepSeek
- 速度快（服务器在国内）
- 价格便宜
- 中文能力强
- 无需科学上网

**海外用户推荐**: OpenAI
- 服务稳定
- 生态成熟
- 模型质量最好

### Q: API Key在哪里获取？

每个服务商都有自己的平台：
- OpenAI: https://platform.openai.com/
- 通义千问: https://dashscope.aliyuncs.com/
- DeepSeek: https://platform.deepseek.com/
- Moonshot: https://platform.moonshot.cn/
- 智谱AI: https://open.bigmodel.cn/

注册账号后，在"API密钥"或"凭证"页面创建。

### Q: 可以混合使用多个服务商吗？

目前版本同时只能使用一个服务商。如需切换，修改 `.env` 文件中的 `AI_PROVIDER` 和 `AI_API_KEY`，然后重启服务。

### Q: 遇到错误怎么办？

1. 检查API Key是否正确
2. 检查账户余额是否充足
3. 查看日志文件 `backend/server.log`
4. 确认模型名称是否正确

### Q: 兼容性说明

所有服务商都使用OpenAI兼容的接口格式。本项目通过统一的 `OpenAI` 客户端与不同服务商通信，只需修改 `base_url` 和 `model` 参数即可切换。

## 更多帮助

如有问题，请查看：
- 服务日志: `backend/server.log`
- 环境变量配置: `backend/.env`
- 代码实现: `backend/ai_service.py`
