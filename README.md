# AB测试论文阅读系统

一个全自动的AB测试论文阅读和摘要系统，每日自动从arXiv获取最新的AB测试相关论文，并使用AI生成中文摘要和解读。

## 功能特性

✅ **每日自动抓取**：自动查询arXiv上关于AB TEST相关的最新论文  
✅ **AI智能解读**：使用OpenAI API阅读论文并生成中文摘要和详细解读  
✅ **智能分类**：根据论文内容自动分类（统计方法、实验平台、因果推断等）  
✅ **Web界面**：美观的前端页面，支持按日期、分类查询和展示  
✅ **RESTful API**：完整的后端API接口  
✅ **数据持久化**：使用SQLite存储论文数据  

## 技术栈

### 后端
- **FastAPI**：高性能异步Web框架
- **SQLAlchemy**：ORM数据库操作
- **arxiv**：arXiv API客户端
- **OpenAI**：AI论文解读
- **APScheduler**：定时任务调度

### 前端
- **原生HTML/CSS/JavaScript**：简洁高效的单页面应用
- **响应式设计**：支持各种屏幕尺寸

### 数据库
- **SQLite**：轻量级本地数据库

## 项目结构

```
.
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI主应用
│   ├── models.py           # 数据库模型
│   ├── arxiv_service.py    # arXiv API集成
│   ├── ai_service.py       # AI解读服务
│   ├── scheduler.py        # 定时任务
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端代码
│   └── index.html         # 主页面
├── README.md              # 项目文档
└── start.sh               # 启动脚本
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- OpenAI API Key

### 2. 安装依赖

```bash
# 安装后端依赖
cd backend
pip install -r requirements.txt
```

## AI服务配置

系统支持多种AI服务提供商，不仅限于OpenAI！

### 支持的AI服务商

- ✅ **OpenAI** (gpt-4o-mini, gpt-4等)
- ✅ **通义千问/Qwen** (阿里云) - 推荐国内用户
- ✅ **DeepSeek** - 价格最低
- ✅ **Moonshot/Kimi** - 长文本处理
- ✅ **智谱AI/GLM** 
- ✅ **自定义** - 任何兼容OpenAI接口的服务

### 快速配置

创建 `.env` 文件并设置：

```bash
# 使用OpenAI（默认）
AI_PROVIDER=openai
AI_API_KEY=sk-xxxxx

# 或使用通义千问（推荐国内用户）
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxx

# 或使用DeepSeek（最便宜）
AI_PROVIDER=deepseek
AI_API_KEY=sk-xxxxx
```

**详细配置文档**: 查看 [docs/AI_PROVIDERS.md](docs/AI_PROVIDERS.md)

### 成本对比

| 服务商 | 相对成本 | 推荐场景 |
|--------|---------|---------|
| DeepSeek | 1x (最低) | 个人学习、高频调用 |
| 通义千问 | 2-5x | 国内生产环境 |
| OpenAI | 10-100x | 追求最高质量 |

### 4. 启动应用

#### 方式一：使用启动脚本（推荐）

```bash
# 在项目根目录
chmod +x start.sh
./start.sh
```

#### 方式二：手动启动

```bash
# 启动后端服务
cd backend
python main.py

# 在另一个终端启动定时任务（可选）
python scheduler.py
```

### 5. 访问应用

- 前端页面：打开 `frontend/index.html` 文件
- API文档：http://localhost:8000/docs
- API端点：http://localhost:8000/api

## 使用说明

### 获取论文

1. **自动获取**：系统每天早上9点自动抓取最新论文
2. **手动获取**：在Web界面点击"手动获取最新论文"按钮

### 查询论文

- **按日期查询**：选择具体日期查看当天发布的论文
- **按分类查询**：选择论文分类（统计方法、实验平台等）
- **查看详情**：每篇论文包含标题、摘要、解读、分类和链接

### API接口

#### 获取论文列表
```
GET /api/papers?date=2024-03-04&category=统计方法
```

#### 获取论文详情
```
GET /api/papers/{paper_id}
```

#### 手动触发论文抓取
```
POST /api/fetch?days_back=1
```

#### 获取统计信息
```
GET /api/stats
```

#### 获取分类列表
```
GET /api/categories
```

## 定时任务配置

系统默认每天早上9点自动抓取论文。如需修改，编辑 `backend/scheduler.py`：

```python
# 修改这一行来改变执行时间
self.scheduler.add_job(
    self.fetch_and_process_papers,
    'cron',
    hour=9,  # 小时
    minute=0,  # 分钟
    id='daily_paper_fetch'
)
```

## 数据库

论文数据存储在 `backend/papers.db` SQLite数据库中。

数据表结构：
- `id`: 主键
- `arxiv_id`: arXiv论文ID（唯一）
- `title`: 论文标题
- `authors`: 作者列表
- `abstract`: 英文摘要
- `summary_cn`: 中文摘要
- `interpretation`: 论文解读
- `category`: 分类
- `arxiv_url`: arXiv链接
- `pdf_url`: PDF下载链接
- `published_date`: 发布日期
- `created_at`: 创建时间
- `updated_at`: 更新时间

## 常见问题

### 1. OpenAI API调用失败

确保：
- API Key正确配置在环境变量中
- 账户有足够的额度
- 网络可以访问OpenAI API

### 2. arXiv API超时

arXiv API有时会比较慢，可以：
- 增加超时时间
- 减少单次查询的论文数量
- 稍后重试

### 3. 没有找到论文

可能原因：
- 当天没有发布AB测试相关的论文
- arXiv分类系统延迟
- 关键词匹配不到

解决方法：
- 查询更早的日期
- 调整 `arxiv_service.py` 中的关键词列表

## 开发建议

### 扩展关键词

编辑 `backend/arxiv_service.py` 的 `AB_TEST_KEYWORDS` 列表：

```python
AB_TEST_KEYWORDS = [
    "A/B test",
    "AB test",
    # 添加更多关键词...
]
```

### 自定义分类

编辑 `backend/ai_service.py` 的分类提示词：

```python
prompt = f"""请根据以下AB测试论文的标题和摘要，将其归类到以下类别之一：
- 统计方法
- 实验平台
- 你的新分类
...
```

### 修改AI模型

在 `backend/ai_service.py` 中修改：

```python
response = self.client.chat.completions.create(
    model="gpt-4o-mini",  # 改为其他模型如 gpt-4
    ...
)
```

## 部署建议

### 生产环境

1. 使用PostgreSQL替代SQLite
2. 配置Nginx反向代理
3. 使用Gunicorn运行FastAPI
4. 设置环境变量而不是.env文件
5. 配置日志系统
6. 添加错误监控

### Docker部署（可选）

```dockerfile
# Dockerfile示例
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过以下方式联系：
- 提交Issue
- 发送邮件

## 更新日志

### v1.0.0 (2024-03-04)
- ✅ 初始版本发布
- ✅ 实现arXiv论文自动抓取
- ✅ 集成OpenAI论文解读
- ✅ 完成Web界面
- ✅ 添加定时任务功能
