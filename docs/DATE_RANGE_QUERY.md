# 日期范围查询功能说明

## 📅 功能概述

v2.1版本新增日期范围查询功能，从单个日期查询升级为支持开始日期和结束日期的范围查询。

---

## ✨ 新功能特性

### 1. 日期范围筛选

**前端界面**：
- ✅ **开始日期**：选择查询的起始日期
- ✅ **结束日期**：选择查询的截止日期
- ✅ **默认范围**：昨天到今天（自动填充）

**查询逻辑**：
- 如果两个日期都填写：查询该范围内的所有论文
- 如果只填开始日期：查询从该日期到今天的所有论文
- 如果只填结束日期：查询从2020年1月1日到该日期的所有论文
- 如果都不填：显示所有论文（不按日期筛选）

### 2. 兼容性

**向后兼容**：
- 后端API保留旧的 `date` 参数支持
- 可以同时接受新旧两种查询方式
- 前端完全升级为日期范围查询

---

## 🎯 使用场景

### 场景1：查看最近几天的论文
```
开始日期: 2026-03-01
结束日期: 2026-03-03
结果: 3天内的所有论文
```

### 场景2：查看某个月的论文
```
开始日期: 2026-02-01
结束日期: 2026-02-29
结果: 2月份的所有论文
```

### 场景3：查看某日期之后的所有论文
```
开始日期: 2026-02-15
结束日期: (留空)
结果: 2月15日至今的所有论文
```

### 场景4：查看某日期之前的所有论文
```
开始日期: (留空)
结束日期: 2026-02-28
结果: 2020年1月1日到2月28日的所有论文
```

### 场景5：查看全部论文
```
开始日期: (留空)
结束日期: (留空)
结果: 所有论文（不按日期筛选）
```

---

## 💻 技术实现

### 后端API

**参数说明**：
```python
@app.get("/api/papers")
def get_papers(
    date_from: Optional[str] = Query(None, description="开始日期，格式：YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="结束日期，格式：YYYY-MM-DD"),
    date: Optional[str] = Query(None, description="单个日期（兼容旧版），格式：YYYY-MM-DD"),
    ...
)
```

**查询逻辑**：
```python
# 如果只有开始日期，结束日期设为今天
if date_from and not date_to:
    start_date = datetime.strptime(date_from, "%Y-%m-%d")
    end_date = datetime.now()

# 如果只有结束日期，开始日期设为很早以前
elif date_to and not date_from:
    start_date = datetime(2020, 1, 1)
    end_date = datetime.strptime(date_to, "%Y-%m-%d")

# 如果都有，使用指定的范围
else:
    start_date = datetime.strptime(date_from, "%Y-%m-%d")
    end_date = datetime.strptime(date_to, "%Y-%m-%d")

# 结束日期加1天，使其包含当天
end_date_inclusive = end_date + timedelta(days=1)

query = query.filter(
    Paper.published_date >= start_date,
    Paper.published_date < end_date_inclusive
)
```

### 前端界面

**HTML结构**：
```html
<div class="control-group">
    <label for="dateFrom">开始日期：</label>
    <input type="date" id="dateFrom">
</div>
<div class="control-group">
    <label for="dateTo">结束日期：</label>
    <input type="date" id="dateTo">
</div>
```

**JavaScript调用**：
```javascript
async function loadPapers(dateFrom = '', dateTo = '', category = '', markedOnly = false, sortBy = 'date') {
    let url = `${API_BASE}/papers?limit=100`;
    if (dateFrom) url += `&date_from=${dateFrom}`;
    if (dateTo) url += `&date_to=${dateTo}`;
    ...
}

function filterPapers() {
    const dateFrom = document.getElementById('dateFrom').value;
    const dateTo = document.getElementById('dateTo').value;
    const category = document.getElementById('categoryFilter').value;
    const markedOnly = document.getElementById('markedOnly').checked;
    const sortBy = document.getElementById('sortBy').value;
    loadPapers(dateFrom, dateTo, category, markedOnly, sortBy);
}
```

---

## 📊 对比v2.0

| 功能 | v2.0 | v2.1 | 改进 |
|------|------|------|------|
| 日期筛选 | 单个日期 | 日期范围 | ✅ 更灵活 |
| 查询方式 | 精确匹配某一天 | 范围查询 | ✅ 支持跨度查询 |
| 用户体验 | 需要多次查询 | 一次查询多天 | ✅ 效率提升 |
| API参数 | `date` | `date_from`, `date_to` | ✅ 语义更清晰 |
| 兼容性 | - | 保留 `date` 参数 | ✅ 向后兼容 |

---

## 🎨 用户体验优化

### 1. 默认值设置
- **开始日期**：自动设置为昨天
- **结束日期**：自动设置为今天
- **原因**：大多数用户关心最近的论文

### 2. 重置功能
- 点击"重置"按钮
- 恢复为默认日期范围（昨天到今天）
- 清空其他筛选条件

### 3. 智能提示
- 日期格式自动验证
- 错误提示友好
- 支持键盘输入和日历选择

---

## 🔍 API示例

### 示例1：查询3天范围
```http
GET /api/papers?date_from=2026-03-01&date_to=2026-03-03&limit=100
```

**响应**：
```json
{
    "total": 50,
    "skip": 0,
    "limit": 100,
    "papers": [...]
}
```

### 示例2：查询某日期之后
```http
GET /api/papers?date_from=2026-03-03&limit=100
```

**说明**：查询3月3日至今的所有论文

### 示例3：查询某日期之前
```http
GET /api/papers?date_to=2026-02-28&limit=100
```

**说明**：查询2020-01-01至2026-02-28的所有论文

### 示例4：兼容旧版
```http
GET /api/papers?date=2026-03-03&limit=100
```

**说明**：仍然支持单个日期查询（精确匹配某一天）

---

## ⚠️ 注意事项

### 1. 日期格式
- 必须使用 `YYYY-MM-DD` 格式
- 例如：`2026-03-04`
- 错误格式会返回400错误

### 2. 日期范围
- 开始日期不能晚于结束日期（前端应该验证）
- 最早日期：2020-01-01
- 最晚日期：今天

### 3. 包含性
- 结束日期是包含的（inclusive）
- 例如：`date_to=2026-03-03` 会包含3月3日当天的论文

### 4. 时区
- 所有日期基于UTC时区
- 论文的 `published_date` 字段是UTC时间

---

## 📈 性能考虑

### 查询效率
- 日期范围查询使用数据库索引
- `published_date` 字段已建立索引
- 大范围查询（如30天）性能良好

### 推荐使用
- 日常使用：1-7天范围
- 回顾总结：7-30天范围
- 避免：超过90天的大范围查询

---

## 🚀 未来扩展

### 可能的增强功能
1. **快捷日期选择**
   - "最近7天"
   - "本月"
   - "上个月"
   
2. **日期范围预设**
   - 保存常用的日期范围
   - 一键切换
   
3. **日期验证**
   - 前端检查开始日期≤结束日期
   - 智能提示
   
4. **日历视图**
   - 在日历上标记有论文的日期
   - 点击日期快速查询

---

## ✅ 更新总结

### 改动文件
- ✅ `backend/main.py` - API支持日期范围参数
- ✅ `frontend/index_v2.html` - UI改为两个日期选择器
- ✅ `frontend/frontend_v2.js` - 传递日期范围参数
- ✅ `docs/DATE_RANGE_QUERY.md` - 功能说明文档

### 用户体验提升
- ✅ 查询更灵活（范围查询vs单日查询）
- ✅ 默认值更合理（昨天到今天）
- ✅ 支持多种查询方式
- ✅ 向后兼容旧版API

### 功能增强
- ✅ 支持跨多天查询
- ✅ 支持开放式范围（只设置一端）
- ✅ 智能默认值
- ✅ 友好的错误提示

---

**版本**：v2.1  
**更新日期**：2026-03-04  
**功能**：日期范围查询
