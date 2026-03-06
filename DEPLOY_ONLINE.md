# AB测试论文阅读系统 - 在线部署指南

## 🚀 最简单的部署方案：Render.com（5分钟上线）

### 为什么选择 Render.com？
- ✅ **完全免费**：Free tier 永久免费
- ✅ **自动HTTPS**：免费 SSL 证书
- ✅ **零配置**：自动检测 Python 项目
- ✅ **GitHub集成**：代码推送自动部署
- ✅ **简单易用**：适合快速上线

---

## 📋 部署步骤

### 第1步：准备代码（本地）

#### 1.1 确认项目配置
项目已经准备好所有配置文件：
- ✅ `render.yaml` - Render 部署配置
- ✅ `backend/requirements.txt` - Python 依赖
- ✅ `backend/.env` - 环境变量模板

#### 1.2 创建 GitHub 仓库

```bash
# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Ready for deployment"

# 在 GitHub 创建仓库（访问 https://github.com/new）
# 仓库名建议：ab-paper-reader

# 关联远程仓库（替换为你的用户名）
git remote add origin https://github.com/yangyang35/ab-paper-reader.git

# 推送代码
git branch -M main
git push -u origin main
```

---

### 第2步：部署到 Render.com

#### 2.1 注册账号
1. 访问 https://render.com
2. 点击右上角 "Get Started"
3. 使用 GitHub 账号登录（推荐）

#### 2.2 创建 Web Service

1. **点击 "New +"** → 选择 "Web Service"

2. **连接 GitHub 仓库**
   - 点击 "Connect a repository"
   - 授权 Render 访问你的 GitHub
   - 选择 `ab-paper-reader` 仓库

3. **配置服务**（会自动检测 render.yaml）
   - **Name**: `ab-paper-reader`
   - **Region**: `Singapore` (国内访问较快)
   - **Branch**: `main`
   - **Root Directory**: 留空
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **选择计划**
   - 选择 **"Free"** 计划（$0/月）

5. **点击 "Create Web Service"**

#### 2.3 配置环境变量

在服务创建后，进入 **Environment** 标签页：

点击 "Add Environment Variable"，添加以下变量：

| Key | Value | 说明 |
|-----|-------|------|
| `AI_PROVIDER` | `qwen` | AI 提供商 |
| `AI_API_KEY` | `你的通义千问API密钥` | ⚠️ 必须填写 |
| `AI_BASE_URL` | `https://dashscope.aliyuncs.com/compatible-mode/v1` | API 地址 |
| `AI_MODEL` | `qwen-plus` | 模型名称 |

⚠️ **重要**：添加完环境变量后，点击 "Save Changes"，服务会自动重新部署。

---

### 第3步：访问应用

#### 3.1 获取 URL
部署成功后，Render 会提供一个免费域名，格式如下：
```
https://ab-paper-reader.onrender.com
```

#### 3.2 访问前端
在浏览器中访问：
```
https://ab-paper-reader.onrender.com/frontend/index_v2.html
```

#### 3.3 测试 API
访问健康检查接口：
```
https://ab-paper-reader.onrender.com/api/health
```

应该返回：
```json
{
  "status": "ok",
  "timestamp": "2026-03-06T03:17:00.000000"
}
```

---

## 🎯 部署后配置

### 修改前端 API 地址

**重要**：前端需要指向线上 API 地址！

编辑 `frontend/frontend_v2.js`，找到第1行：
```javascript
const API_BASE = 'http://localhost:8000/api';
```

改为：
```javascript
const API_BASE = 'https://ab-paper-reader.onrender.com/api';
```

然后提交并推送：
```bash
git add frontend/frontend_v2.js
git commit -m "Update API endpoint for production"
git push
```

Render 会自动检测并重新部署（约2-3分钟）。

---

## ⚙️ Render.com 特性说明

### Free Tier 限制
- ✅ **免费HTTPS**
- ✅ **自动部署**
- ⚠️ **冷启动**：15分钟无访问自动休眠，下次访问需要30-60秒唤醒
- ⚠️ **资源限制**：512MB RAM，0.1 CPU
- ⚠️ **每月750小时**免费运行时间

### 冷启动问题
由于 Free tier 会自动休眠，首次访问较慢。解决方案：

#### 方案1：定期 ping（推荐）
使用第三方服务定期访问，保持唤醒：
- **UptimeRobot**: https://uptimerobot.com （免费）
- **Cron-job.org**: https://cron-job.org （免费）

配置每5分钟访问一次健康检查接口：
```
https://ab-paper-reader.onrender.com/api/health
```

#### 方案2：升级到付费计划
- **Starter**: $7/月，无休眠
- **Standard**: $25/月，更高性能

---

## 🔧 常见问题

### Q1: 部署失败怎么办？

**查看日志**：
1. 在 Render 控制台，点击你的服务
2. 点击 "Logs" 标签
3. 查看构建和运行日志

**常见原因**：
- Python 版本不匹配 → 确保 `render.yaml` 中指定了 Python 3.9
- 依赖安装失败 → 检查 `requirements.txt`
- 环境变量未设置 → 确认 AI_API_KEY 已填写

### Q2: 访问很慢？

**原因**：
- Free tier 冷启动（休眠后首次访问）
- 服务器位置较远

**解决方案**：
1. 使用 UptimeRobot 保持唤醒
2. 选择新加坡（Singapore）服务器
3. 考虑升级到付费计划

### Q3: 定时任务会执行吗？

**会！** 只要服务保持运行，定时任务每天早上9:00会自动执行。

**注意**：
- Free tier 休眠时定时任务不会执行
- 建议使用 UptimeRobot 保持唤醒
- 或升级到 Starter 计划（$7/月）

### Q4: 数据会丢失吗？

**SQLite 数据库**：
- ⚠️ Render Free tier 的文件系统是**临时的**
- 服务重启后数据会丢失

**解决方案**：
1. **简单方案**：定期导出数据库（下载备份）
2. **推荐方案**：使用 PostgreSQL
   - Render 提供免费 PostgreSQL 数据库
   - 修改 `backend/models.py` 连接 PostgreSQL
   - 数据持久化保存

### Q5: 如何绑定自定义域名？

1. 在 Render 服务设置中，进入 **Custom Domains**
2. 点击 **Add Custom Domain**
3. 输入你的域名（如 `papers.yoursite.com`）
4. 在域名 DNS 设置中添加 CNAME 记录：
   ```
   papers.yoursite.com → ab-paper-reader.onrender.com
   ```
5. 等待 DNS 生效（通常几分钟到几小时）

---

## 🎨 优化建议

### 1. 迁移到 PostgreSQL（推荐）

**为什么**：
- 数据持久化
- 更好的性能
- 支持并发

**步骤**：

1. 在 Render 创建 PostgreSQL 数据库
   - New + → PostgreSQL
   - 选择 Free tier
   - 记下 `DATABASE_URL`

2. 修改 `backend/models.py`：
```python
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./papers.db")

# PostgreSQL URL 格式修正
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

3. 添加依赖 `backend/requirements.txt`：
```
psycopg2-binary==2.9.9
```

4. 在 Web Service 的环境变量中添加：
```
DATABASE_URL = <从 PostgreSQL 数据库复制>
```

5. 重新部署

### 2. 静态文件优化

**方案1**：使用 Render Static Site（推荐）
- 将前端部署到 Render Static Site（更快）
- 后端单独部署（Web Service）

**方案2**：使用 Vercel 托管前端
- 前端：Vercel（免费 CDN 加速）
- 后端：Render（免费 API 服务）

### 3. 监控和告警

使用 **UptimeRobot** 监控服务状态：
1. 注册 https://uptimerobot.com
2. 添加监控：`https://ab-paper-reader.onrender.com/api/health`
3. 设置告警：邮件/短信通知
4. 配置检查间隔：5分钟

---

## 📊 部署检查清单

部署完成后，请检查：

- [ ] API 健康检查正常 (`/api/health`)
- [ ] 前端页面可以访问 (`/frontend/index_v2.html`)
- [ ] 可以手动获取论文
- [ ] 论文列表显示正常
- [ ] 标记功能工作
- [ ] 排序功能正常
- [ ] 日期范围查询正常
- [ ] 定时任务已启动（查看日志）
- [ ] 环境变量已正确配置
- [ ] API 地址已更新为线上地址

---

## 🌐 分享给其他人

部署成功后，分享以下链接：

```
📱 在线访问地址：
https://ab-paper-reader.onrender.com/frontend/index_v2.html

📚 API 文档：
https://ab-paper-reader.onrender.com/docs

💡 使用说明：
- 默认显示最近7天的论文
- 可以按日期范围、分类、价值分筛选
- 点击"手动获取论文"抓取最新内容
- 支持标记重要论文
- 每天早上9:00自动更新
```

---

## 💰 成本估算

| 方案 | 月费用 | 特性 |
|------|--------|------|
| **Free Tier** | $0 | 冷启动、750小时/月 |
| **Free + PostgreSQL** | $0 | 冷启动、数据持久化 |
| **Starter** | $7 | 无休眠、高可用 |
| **Starter + PostgreSQL** | $7 | 完美方案 |

---

## 🎉 完成！

现在你的 AB 测试论文阅读系统已经在线了！

**系统功能**：
- ✅ 自动抓取 arXiv 最新论文
- ✅ AI 智能解读和分类
- ✅ 中文标题翻译
- ✅ 结构化解读
- ✅ 思维导图
- ✅ 平台价值评估
- ✅ 论文标记
- ✅ 多维度筛选
- ✅ 每天自动更新

**下一步**：
1. 配置 UptimeRobot 保持服务唤醒
2. 考虑迁移到 PostgreSQL（数据持久化）
3. 邀请团队成员使用
4. 收集反馈，持续优化

---

**需要帮助？**
- Render 文档：https://render.com/docs
- FastAPI 文档：https://fastapi.tiangolo.com
- 项目 GitHub：https://github.com/yangyang35/ab-paper-reader

祝部署顺利！🚀
