# 数据库管理指南

## 📊 数据库管理操作

系统提供了完整的数据库管理功能，方便您查看、清空和重新获取论文数据。

---

## 1️⃣ 查看数据库统计

### API 端点：
```
GET https://ab-paper-reader.onrender.com/api/stats
```

### 使用浏览器访问：
```
https://ab-paper-reader.onrender.com/api/stats
```

### 返回示例：
```json
{
  "total_papers": 15,
  "marked_papers": 3,
  "category_distribution": {
    "实验设计": 5,
    "统计分析": 7,
    "因果推断": 3
  }
}
```

### 使用 curl：
```bash
curl https://ab-paper-reader.onrender.com/api/stats
```

---

## 2️⃣ 清空数据库

### ⚠️ 重要提示

**清空数据库会删除所有论文数据，此操作不可恢复！**

### 方法A：使用浏览器（推荐）

**步骤**：

1. **在浏览器访问**：
   ```
   https://ab-paper-reader.onrender.com/api/papers/clear?confirm=true
   ```

2. **确认提示**：
   - 浏览器会显示返回的 JSON 结果

3. **查看结果**：
   ```json
   {
     "message": "成功删除 15 篇论文",
     "deleted_count": 15
   }
   ```

### 方法B：使用 curl

```bash
# 清空数据库
curl -X DELETE "https://ab-paper-reader.onrender.com/api/papers/clear?confirm=true"
```

### 方法C：使用本地脚本（仅本地开发）

如果是本地运行，可以使用：

```bash
cd backend
python3 clear_database.py
```

**注意**：这只对本地数据库有效，不影响线上 Render 的数据库！

---

## 3️⃣ 重新获取论文

### 清空后重新获取的完整流程：

#### 步骤1：清空数据库

```bash
curl -X DELETE "https://ab-paper-reader.onrender.com/api/papers/clear?confirm=true"
```

#### 步骤2：验证已清空

```bash
curl https://ab-paper-reader.onrender.com/api/stats
```

**预期返回**：
```json
{
  "total_papers": 0,
  "marked_papers": 0,
  "category_distribution": {}
}
```

#### 步骤3：重新获取论文

**方式A**：通过网页界面
1. 访问：https://ab-paper-reader.onrender.com/frontend/index_v2.html
2. 选择获取范围（如"最近7天"）
3. 点击"手动获取论文"
4. 等待5-15分钟

**方式B**：通过 API
```bash
# 获取最近7天的论文
curl -X POST "https://ab-paper-reader.onrender.com/api/fetch?days_back=7"
```

#### 步骤4：监控进度

查看 Render Logs：
1. 访问：https://dashboard.render.com
2. 进入服务 → Logs
3. 观察处理进度

#### 步骤5：验证结果

刷新页面或查询统计：
```bash
curl https://ab-paper-reader.onrender.com/api/stats
```

---

## 4️⃣ 数据库管理脚本

### 创建管理脚本（推荐）

创建 `manage_db.sh`：

```bash
#!/bin/bash

BASE_URL="https://ab-paper-reader.onrender.com"

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 查看统计
stats() {
    echo -e "${YELLOW}📊 数据库统计${NC}"
    echo "======================================"
    curl -s "$BASE_URL/api/stats" | python3 -m json.tool
    echo ""
}

# 清空数据库
clear_db() {
    echo -e "${RED}⚠️  警告：即将清空数据库！${NC}"
    read -p "确认删除所有论文数据？(yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        echo -e "${YELLOW}正在清空数据库...${NC}"
        result=$(curl -s -X DELETE "$BASE_URL/api/papers/clear?confirm=true")
        echo "$result" | python3 -m json.tool
        echo -e "${GREEN}✓ 完成${NC}"
    else
        echo -e "${YELLOW}已取消${NC}"
    fi
}

# 重新获取论文
fetch_papers() {
    read -p "获取最近几天的论文？(1-30): " days
    echo -e "${YELLOW}正在获取最近 ${days} 天的论文...${NC}"
    echo "这可能需要 5-15 分钟，请耐心等待..."
    
    curl -X POST "$BASE_URL/api/fetch?days_back=$days" \
        -H "Content-Type: application/json"
    
    echo ""
    echo -e "${GREEN}✓ 请求已发送，请查看 Render Logs 监控进度${NC}"
}

# 完整重置流程
reset_all() {
    echo -e "${RED}⚠️  完整重置流程${NC}"
    echo "======================================"
    echo "1. 清空数据库"
    echo "2. 重新获取论文"
    echo ""
    
    read -p "确认执行完整重置？(yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        # 步骤1：清空
        echo -e "${YELLOW}步骤1：清空数据库${NC}"
        curl -s -X DELETE "$BASE_URL/api/papers/clear?confirm=true" | python3 -m json.tool
        echo ""
        
        # 步骤2：验证
        echo -e "${YELLOW}步骤2：验证已清空${NC}"
        stats
        
        # 步骤3：重新获取
        echo -e "${YELLOW}步骤3：重新获取论文${NC}"
        read -p "获取最近几天的论文？(建议7): " days
        curl -X POST "$BASE_URL/api/fetch?days_back=$days"
        
        echo ""
        echo -e "${GREEN}✓ 重置流程已启动${NC}"
        echo "请访问 https://dashboard.render.com 查看 Logs 监控进度"
    else
        echo -e "${YELLOW}已取消${NC}"
    fi
}

# 主菜单
show_menu() {
    echo ""
    echo -e "${GREEN}====================================${NC}"
    echo -e "${GREEN}  AB测试论文系统 - 数据库管理${NC}"
    echo -e "${GREEN}====================================${NC}"
    echo ""
    echo "1. 查看统计"
    echo "2. 清空数据库"
    echo "3. 获取论文"
    echo "4. 完整重置（清空+获取）"
    echo "5. 退出"
    echo ""
    read -p "请选择操作 (1-5): " choice
    
    case $choice in
        1) stats ;;
        2) clear_db ;;
        3) fetch_papers ;;
        4) reset_all ;;
        5) exit 0 ;;
        *) echo -e "${RED}无效选择${NC}" ;;
    esac
    
    show_menu
}

# 启动菜单
show_menu
```

### 使用管理脚本：

```bash
# 赋予执行权限
chmod +x manage_db.sh

# 运行脚本
./manage_db.sh
```

---

## 5️⃣ 快速命令参考

### 一键清空并重新获取（最近7天）：

```bash
# 清空数据库
curl -X DELETE "https://ab-paper-reader.onrender.com/api/papers/clear?confirm=true"

# 等待2秒
sleep 2

# 重新获取论文
curl -X POST "https://ab-paper-reader.onrender.com/api/fetch?days_back=7"

# 查看统计
sleep 5
curl https://ab-paper-reader.onrender.com/api/stats
```

### 监控处理进度：

```bash
# 持续查看论文数量变化
while true; do
  echo -n "$(date +%H:%M:%S) - "
  curl -s https://ab-paper-reader.onrender.com/api/stats | grep -o '"total_papers":[0-9]*'
  sleep 10
done
```

---

## 6️⃣ 常见场景

### 场景1：想要重新抓取所有论文

**原因**：可能是之前抓取的论文有问题，或者想用新的 AI 提供商重新处理

**操作**：
```bash
# 1. 清空数据库
curl -X DELETE "https://ab-paper-reader.onrender.com/api/papers/clear?confirm=true"

# 2. 重新获取最近30天的论文
curl -X POST "https://ab-paper-reader.onrender.com/api/fetch?days_back=30"
```

### 场景2：测试不同的时间范围

**操作**：
```bash
# 清空
curl -X DELETE "https://ab-paper-reader.onrender.com/api/papers/clear?confirm=true"

# 测试最近1天
curl -X POST "https://ab-paper-reader.onrender.com/api/fetch?days_back=1"
```

### 场景3：定期清理旧数据

如果论文太多，想只保留最近的：

**方案A**：清空后重新获取最近14天
```bash
curl -X DELETE "https://ab-paper-reader.onrender.com/api/papers/clear?confirm=true"
curl -X POST "https://ab-paper-reader.onrender.com/api/fetch?days_back=14"
```

**方案B**：创建定期清理计划任务（需要修改 scheduler.py）

---

## 7️⃣ API 端点完整列表

| 端点 | 方法 | 功能 | 参数 |
|------|------|------|------|
| `/api/stats` | GET | 查看统计 | 无 |
| `/api/papers` | GET | 查询论文 | date_from, date_to, category, etc. |
| `/api/papers/clear` | DELETE | 清空数据库 | confirm=true (必填) |
| `/api/fetch` | POST | 获取论文 | days_back (1-90) |
| `/api/health` | GET | 健康检查 | 无 |

---

## 8️⃣ 注意事项

### ⚠️ 数据持久化问题（Render Free Tier）

**重要**：Render Free Tier 的文件系统是**临时的**！

- 服务重启后 SQLite 数据会丢失
- 建议定期导出数据备份
- 或迁移到 PostgreSQL（永久存储）

### 🔒 安全建议

**生产环境**应该添加认证保护：

```python
# 示例：添加 API Key 验证
@app.delete("/api/papers/clear")
def clear_all_papers(
    api_key: str = Header(...),
    confirm: bool = Query(False),
    db: Session = Depends(get_db)
):
    if api_key != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    # ... 清空逻辑
```

---

## 9️⃣ 故障排查

### 问题1：清空失败

**错误**：`500 Internal Server Error`

**解决方案**：
1. 查看 Render Logs
2. 可能是数据库锁定，等待几秒后重试

### 问题2：清空后重新获取还是 0 篇

**原因**：可能是：
1. 最近没有相关论文发布
2. arXiv 搜索关键词太严格
3. 时间范围太短

**解决方案**：
- 扩大时间范围（如 30 天）
- 检查 arXiv_service.py 的搜索关键词

---

## 🎯 推荐工作流

**日常使用**：
1. 每天让定时任务自动更新（早上9:00）
2. 无需手动干预

**需要重置时**：
1. 访问：`/api/papers/clear?confirm=true` 清空
2. 访问页面点击"手动获取论文"
3. 或直接调用 `/api/fetch?days_back=7`

**定期维护**：
1. 每月检查一次数据库大小
2. 如果论文太多，清空并重新获取最近30天

---

**现在您可以完全掌控数据库了！** 🎉
