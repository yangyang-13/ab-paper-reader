## 快速配置通义千问 (Qwen)

已为您配置好使用通义千问！现在只需3步：

### 步骤1: 填写API Key

编辑 `backend/.env` 文件，将您的通义千问API Key填入：

```bash
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxxxxxxxxxx  # ← 替换成您的真实API Key
```

**如何获取API Key**:
1. 访问阿里云DashScope: https://dashscope.aliyuncs.com/
2. 登录/注册账号
3. 进入"API-KEY管理"页面
4. 创建新的API Key或复制现有的Key

### 步骤2: 保存并重启服务

**Linux/Mac:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

### 步骤3: 验证配置

启动后，查看日志确认配置成功：

```bash
tail -f backend/server.log
```

应该看到：
```
✓ AI服务已初始化: qwen (qwen-plus) at https://dashscope.aliyuncs.com/compatible-mode/v1
```

---

## 完整配置示例

您的 `backend/.env` 文件应该是这样的：

```bash
# AI服务配置 - 使用通义千问
AI_PROVIDER=qwen
AI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

# 可选：指定具体模型（默认使用 qwen-plus）
# AI_MODEL=qwen-plus

# 可选的其他通义千问模型：
# AI_MODEL=qwen-turbo   # 速度快，成本低
# AI_MODEL=qwen-max     # 最强性能
# AI_MODEL=qwen-long    # 长文本处理
```

---

## 通义千问优势

✅ **价格实惠**: 比OpenAI便宜5-10倍  
✅ **速度快**: 服务器在国内，无需科学上网  
✅ **中文能力强**: 专门优化过中文理解和生成  
✅ **稳定可靠**: 阿里云企业级服务  

---

## 成本估算

使用通义千问处理论文的大概成本：

| 任务 | 数量 | 估算成本 |
|------|------|---------|
| 论文摘要生成 | 100篇 | ¥1-2 |
| 论文解读生成 | 100篇 | ¥3-5 |
| 论文分类 | 100篇 | ¥0.5 |
| **合计** | **100篇** | **¥5-8** |

非常经济实惠！

---

## 常见问题

### Q: 我的API Key在哪里？
A: 登录 https://dashscope.aliyuncs.com/ → "API-KEY管理"

### Q: 需要付费吗？
A: 新用户通常有免费额度，之后按量付费，价格很便宜。

### Q: 如何查看余额？
A: 在DashScope控制台的"账户中心"查看。

### Q: 支持哪些模型？
A: qwen-turbo（快速）、qwen-plus（推荐）、qwen-max（最强）、qwen-long（长文本）

### Q: 配置后不生效怎么办？
A: 
1. 确认API Key正确（无多余空格）
2. 确认账户有余额
3. 重启服务
4. 查看日志: `tail -f backend/server.log`

---

## 测试配置

配置完成后，在网页上点击"手动获取最新论文"，系统会：

1. ✅ 从arXiv获取论文
2. ✅ 使用通义千问生成中文摘要
3. ✅ 使用通义千问生成详细解读
4. ✅ 使用通义千问进行分类

全程使用您配置的通义千问服务！

---

## 下一步

配置完成后，您可以：
- 📊 开始抓取和解读AB测试论文
- 🔍 浏览历史论文数据
- 📅 查看每日自动更新（每天早上9点）
- ⚙️ 调整定时任务配置

祝使用愉快！🎉
