# 监控"手动获取论文"进度指南

## 🔍 如何查看处理进度

当您点击"手动获取论文"后，有3种方式监控处理进度：

---

## 方法1：浏览器 Network 标签（推荐）

### 步骤：

1. **打开开发者工具**（F12 或右键→检查）
2. **切换到 Network 标签**
3. **点击"手动获取论文"**
4. **查找 `fetch` 请求**

### 预期看到：

```
Name: fetch?days_back=7
Method: POST
Status: (pending) → 等待中...
```

### 正常情况：

- **Status 显示 "pending"**：后台正在处理
- **时间持续增加**：说明正在运行
- **最终显示 200**：处理完成

### 处理时间：

| 论文数量 | 预计时间 |
|---------|---------|
| 1-5篇 | 2-5分钟 |
| 10篇 | 5-10分钟 |
| 20篇 | 10-20分钟 |
| 30篇 | 15-30分钟 |

### 如果请求超时：

浏览器可能会在2-5分钟后显示超时，但**后台仍在继续处理**！

**解决方案**：
1. 不用担心超时错误
2. 等待5-10分钟
3. 刷新页面查看是否有新论文

---

## 方法2：Render 控制台日志（最准确）

### 步骤：

1. **打开 Render.com**：https://dashboard.render.com
2. **登录账号**
3. **点击你的服务**：`ab-paper-reader`
4. **点击左侧 "Logs" 标签**
5. **查看实时日志输出**

### 预期日志（正常处理）：

```
INFO:arxiv_service:Fetching papers from last 7 days...
INFO:arxiv_service:Found 15 papers from arXiv

INFO:ai_service:Processing paper (v2.1 optimized): A/B Test Analysis...
INFO:ai_service:✓ Paper processed successfully (3 API calls)

INFO:main:Added new paper: 【AB测试分析框架】...
INFO:main:✓ Paper saved to database

INFO:ai_service:Processing paper (v2.1 optimized): Causal Inference...
INFO:ai_service:✓ Paper processed successfully (3 API calls)

INFO:main:Added new paper: 【因果推断在实验设计中的应用】...
INFO:main:✓ Paper saved to database

...

INFO:main:✅ Successfully processed 15 papers
```

### 关键日志指标：

| 日志内容 | 说明 |
|---------|------|
| `Fetching papers from last X days` | 开始抓取 |
| `Found X papers from arXiv` | 找到论文 |
| `Processing paper (v2.1 optimized)` | 正在处理论文 |
| `✓ Paper processed successfully` | 单篇处理成功 |
| `Added new paper` | 保存到数据库 |
| `✅ Successfully processed X papers` | 全部完成 |

### 如果看到错误：

```
ERROR:ai_service:AI API call failed: ...
```

**可能原因**：
- AI API Key 未配置
- AI API 配额用完
- 网络问题

---

## 方法3：直接查询数据库（快速验证）

### 使用浏览器访问：

```
https://ab-paper-reader.onrender.com/api/stats
```

**刷新这个URL**，查看 `total` 数量是否在增加：

```json
{
  "total": 5,        // 论文总数（会逐渐增加）
  "categories": {...}
}
```

如果 `total` 从 0 → 5 → 10...，说明正在正常处理！

---

## 🚨 常见问题

### Q1: Network 显示 "failed" 或超时？

**原因**：浏览器请求超时（通常2-5分钟）

**解决方案**：
- ✅ **后台仍在继续处理**，不用担心
- ✅ 去 Render Logs 查看实际进度
- ✅ 或定期刷新 `/api/stats` 查看论文数量

### Q2: Render Logs 没有新输出？

**可能原因**：
1. Free tier 服务休眠了
2. API 请求失败
3. 没有找到相关论文

**检查方法**：
1. 访问 `https://ab-paper-reader.onrender.com/api/health`
2. 查看是否返回 `{"status": "ok"}`
3. 如果超时，说明服务休眠，需要等待30-60秒唤醒

### Q3: 日志显示 "Found 0 papers"？

**原因**：最近X天内没有相关论文发布

**解决方案**：
- 扩大时间范围（改为14天或30天）
- 检查 arXiv 是否正常
- 查看日志中的搜索关键词是否合理

### Q4: 日志显示 AI API 错误？

**常见错误**：
```
ERROR: AI API call failed: 401 Unauthorized
```

**原因**：AI_API_KEY 未配置或无效

**解决方案**：
1. 进入 Render 服务设置
2. 点击 "Environment" 标签
3. 检查 `AI_API_KEY` 是否正确
4. 保存后重新部署

---

## 📊 完整监控流程

### 推荐操作步骤：

1. **点击"手动获取论文"**

2. **立即打开 Render Logs**
   - 访问：https://dashboard.render.com
   - 进入服务 → Logs

3. **观察日志输出**
   - 看到 "Fetching papers..." → 开始抓取 ✓
   - 看到 "Found X papers" → 找到论文 ✓
   - 看到 "Processing paper..." → 正在处理 ✓
   - 看到 "Added new paper..." → 保存成功 ✓

4. **等待处理完成**
   - 每篇论文约30-60秒
   - 10篇论文约5-10分钟

5. **刷新页面查看结果**
   - 论文列表应该显示新论文
   - 统计数据更新

---

## 🎯 快速测试命令

### 测试 API 是否响应：

```bash
# 健康检查
curl https://ab-paper-reader.onrender.com/api/health

# 查看统计（刷新查看论文数量变化）
curl https://ab-paper-reader.onrender.com/api/stats

# 手动触发抓取（1天内）
curl -X POST "https://ab-paper-reader.onrender.com/api/fetch?days_back=1"
```

### 在终端运行：

```bash
# 持续监控论文数量（每10秒刷新一次）
while true; do
  curl -s https://ab-paper-reader.onrender.com/api/stats | grep -o '"total":[0-9]*'
  sleep 10
done
```

如果看到 `"total":5` → `"total":10` → `"total":15`，说明正在处理！

---

## ✅ 成功标志

处理完成后，您应该看到：

1. **Render Logs**：
   ```
   ✅ Successfully processed 15 papers
   ```

2. **浏览器刷新页面**：
   - 论文总数：15篇
   - 论文列表：显示完整内容

3. **API 统计**：
   ```json
   {
     "total": 15,
     "categories": {
       "实验设计": 5,
       "统计分析": 10
     }
   }
   ```

---

## 💡 耐心提示

**重要**：处理需要时间！
- ✅ 每篇论文需要 3 次 AI API 调用
- ✅ 每次调用约 10-20 秒
- ✅ 10篇论文约 5-10 分钟

**不要着急**：
- 后台正在努力工作 💪
- Render Logs 会实时显示进度
- 处理完成后自动刷新页面

---

## 🔗 快速链接

- **Render 控制台**：https://dashboard.render.com
- **Render Logs**：https://dashboard.render.com/web/你的服务ID/logs
- **API 健康检查**：https://ab-paper-reader.onrender.com/api/health
- **API 统计**：https://ab-paper-reader.onrender.com/api/stats
- **API 文档**：https://ab-paper-reader.onrender.com/docs

---

**现在就去 Render Logs 查看实时进度吧！** 🚀
