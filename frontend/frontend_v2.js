const API_BASE = 'http://localhost:8000/api';
let allPapers = [];

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    // 设置默认日期范围：最近7天到今天（更合理的默认值）
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    const today = new Date();
    
    document.getElementById('dateFrom').value = sevenDaysAgo.toISOString().split('T')[0];
    document.getElementById('dateTo').value = today.toISOString().split('T')[0];
    
    loadCategories();
    loadPapers();
    loadStats();
});

// 加载分类列表
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories`);
        const data = await response.json();
        const select = document.getElementById('categoryFilter');
        data.categories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('加载分类失败:', error);
    }
}

// 加载论文列表
async function loadPapers(dateFrom = '', dateTo = '', category = '', markedOnly = false, sortBy = 'date') {
    const loading = document.getElementById('loading');
    const container = document.getElementById('papersContainer');
    const errorDiv = document.getElementById('errorMessage');
    
    loading.style.display = 'block';
    container.innerHTML = '';
    errorDiv.innerHTML = '';
    
    try {
        let url = `${API_BASE}/papers?limit=100`;
        if (dateFrom) url += `&date_from=${dateFrom}`;
        if (dateTo) url += `&date_to=${dateTo}`;
        if (category) url += `&category=${encodeURIComponent(category)}`;
        if (markedOnly) url += `&marked_only=true`;
        if (sortBy) url += `&sort_by=${sortBy}`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('获取论文失败');
        
        const data = await response.json();
        allPapers = data.papers;
        
        document.getElementById('currentCount').textContent = allPapers.length;
        
        if (allPapers.length === 0) {
            container.innerHTML = `
                <div class="empty">
                    <div class="empty-icon">📄</div>
                    <div class="empty-text">暂无论文数据，请点击"手动获取最新论文"按钮或选择其他日期</div>
                </div>
            `;
        } else {
            renderPapers(allPapers);
        }
    } catch (error) {
        errorDiv.innerHTML = `<div class="error">加载失败: ${error.message}</div>`;
    } finally {
        loading.style.display = 'none';
    }
}

// 渲染论文列表
function renderPapers(papers) {
    const container = document.getElementById('papersContainer');
    container.innerHTML = papers.map(paper => renderPaperCard(paper)).join('');
}

// 渲染单个论文卡片
function renderPaperCard(paper) {
    const markedClass = paper.is_marked ? 'marked' : '';
    const markButtonClass = paper.is_marked ? 'marked' : '';
    const markButtonText = paper.is_marked ? '★ 已标记' : '☆ 标记';
    
    // 平台价值评分
    const platformValue = paper.platform_value;
    let valueScoreHtml = '';
    if (platformValue && platformValue.has_value) {
        const score = platformValue.score || 0;
        const scoreClass = score >= 70 ? 'high' : score >= 40 ? 'medium' : 'low';
        valueScoreHtml = `<span class="value-score ${scoreClass}">💎 价值分: ${score}</span>`;
    }
    
    return `
        <div class="paper-card ${markedClass}" data-paper-id="${paper.id}">
            <div class="paper-header">
                <div class="paper-header-left">
                    <div class="paper-title">${escapeHtml(paper.title)}</div>
                    ${paper.title_cn ? `<div class="paper-title-cn">${escapeHtml(paper.title_cn)}</div>` : ''}
                    <div class="paper-meta">
                        <span>📅 ${formatDate(paper.published_date)}</span>
                        <span>✍️ ${escapeHtml(paper.authors.split(',')[0])} 等</span>
                        ${paper.category ? `<span class="category-badge">${escapeHtml(paper.category)}</span>` : ''}
                        ${valueScoreHtml}
                    </div>
                </div>
                <button class="mark-button ${markButtonClass}" onclick="toggleMark(${paper.id}, event)">
                    ${markButtonText}
                </button>
            </div>
            
            <div class="tabs">
                <button class="tab active" onclick="switchTab(event, 'summary-${paper.id}')">摘要</button>
                <button class="tab" onclick="switchTab(event, 'interpretation-${paper.id}')">解读</button>
                ${paper.mindmap ? `<button class="tab" onclick="switchTab(event, 'mindmap-${paper.id}')">思维导图</button>` : ''}
                ${paper.platform_value ? `<button class="tab" onclick="switchTab(event, 'value-${paper.id}')">平台价值</button>` : ''}
            </div>
            
            <div id="summary-${paper.id}" class="tab-content active">
                <div class="section-content">${escapeHtml(paper.summary_cn || paper.abstract)}</div>
            </div>
            
            <div id="interpretation-${paper.id}" class="tab-content">
                ${renderInterpretation(paper)}
            </div>
            
            ${paper.mindmap ? `
            <div id="mindmap-${paper.id}" class="tab-content">
                ${renderMindmap(paper.mindmap)}
            </div>
            ` : ''}
            
            ${paper.platform_value ? `
            <div id="value-${paper.id}" class="tab-content">
                ${renderPlatformValue(paper.platform_value)}
            </div>
            ` : ''}
            
            <div class="paper-links">
                <a href="${paper.arxiv_url}" target="_blank" class="paper-link">arXiv页面</a>
                <a href="${paper.pdf_url}" target="_blank" class="paper-link">PDF下载</a>
            </div>
        </div>
    `;
}

// 渲染解读（结构化或原始）
function renderInterpretation(paper) {
    if (paper.structured_interpretation) {
        const interp = paper.structured_interpretation;
        return `
            <div class="structured-interpretation">
                ${interp.conclusion ? `
                <div class="structured-item">
                    <h4>📌 论文主要结论</h4>
                    <p>${escapeHtml(interp.conclusion)}</p>
                </div>
                ` : ''}
                
                ${interp.innovations ? `
                <div class="structured-item">
                    <h4>💡 主要创新点</h4>
                    <p>${escapeHtml(interp.innovations)}</p>
                </div>
                ` : ''}
                
                ${interp.experimental_data ? `
                <div class="structured-item">
                    <h4>📊 实验数据</h4>
                    <p>${escapeHtml(interp.experimental_data)}</p>
                </div>
                ` : ''}
                
                ${interp.methods ? `
                <div class="structured-item">
                    <h4>🔬 实验方法</h4>
                    <p>${escapeHtml(interp.methods)}</p>
                </div>
                ` : ''}
                
                ${interp.applications ? `
                <div class="structured-item">
                    <h4>🎯 应用场景</h4>
                    <p>${escapeHtml(interp.applications)}</p>
                </div>
                ` : ''}
                
                ${interp.limitations ? `
                <div class="structured-item">
                    <h4>⚠️ 局限性</h4>
                    <p>${escapeHtml(interp.limitations)}</p>
                </div>
                ` : ''}
            </div>
        `;
    } else {
        return `<div class="section-content">${escapeHtml(paper.interpretation || '暂无解读').split('\n').join('<br>')}</div>`;
    }
}

// 渲染思维导图
function renderMindmap(mindmapData) {
    if (!mindmapData) return '';
    
    function renderNode(node, level) {
        let html = `<div class="mindmap-node level-${level}">${escapeHtml(node.name)}</div>`;
        if (node.children && node.children.length > 0) {
            node.children.forEach(child => {
                html += renderNode(child, level + 1);
            });
        }
        return html;
    }
    
    return `<div class="mindmap">${renderNode(mindmapData, 0)}</div>`;
}

// 渲染平台价值
function renderPlatformValue(valueData) {
    if (!valueData) return '';
    
    const judgment = valueData.has_value ? 
        '<span class="value-judgment yes">✓ 有价值</span>' : 
        '<span class="value-judgment no">✗ 价值有限</span>';
    
    return `
        <div class="platform-value">
            <div class="value-header">
                ${judgment}
                <span class="value-score ${valueData.score >= 70 ? 'high' : valueData.score >= 40 ? 'medium' : 'low'}">
                    评分: ${valueData.score || 0}/100
                </span>
            </div>
            
            ${valueData.value_points && valueData.value_points.length > 0 ? `
            <div class="value-points">
                <h4 style="margin-bottom: 15px; color: #4caf50;">核心价值点：</h4>
                ${valueData.value_points.map(point => `
                    <div class="value-point">${escapeHtml(point)}</div>
                `).join('')}
            </div>
            ` : ''}
            
            ${valueData.reasoning ? `
            <div class="value-reasoning">
                <h4 style="margin-bottom: 10px; color: #ff9800;">综合评价：</h4>
                ${escapeHtml(valueData.reasoning)}
            </div>
            ` : ''}
        </div>
    `;
}

// 切换标签页
function switchTab(event, tabId) {
    const card = event.target.closest('.paper-card');
    
    // 切换按钮状态
    card.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    event.target.classList.add('active');
    
    // 切换内容
    card.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
}

// 切换标记状态
async function toggleMark(paperId, event) {
    event.stopPropagation();
    
    try {
        const response = await fetch(`${API_BASE}/papers/${paperId}/mark`, {
            method: 'PATCH'
        });
        
        if (!response.ok) throw new Error('标记失败');
        
        const result = await response.json();
        
        // 更新UI
        const card = document.querySelector(`[data-paper-id="${paperId}"]`);
        const button = card.querySelector('.mark-button');
        
        if (result.is_marked) {
            card.classList.add('marked');
            button.classList.add('marked');
            button.textContent = '★ 已标记';
        } else {
            card.classList.remove('marked');
            button.classList.remove('marked');
            button.textContent = '☆ 标记';
        }
        
        // 更新统计
        loadStats();
        
    } catch (error) {
        alert('标记操作失败: ' + error.message);
    }
}

// 加载统计数据
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        document.getElementById('totalPapers').textContent = data.total_papers;
        
        // 计算已标记数量
        const markedResponse = await fetch(`${API_BASE}/papers?marked_only=true&limit=1000`);
        const markedData = await markedResponse.json();
        document.getElementById('markedCount').textContent = markedData.total;
    } catch (error) {
        console.error('加载统计失败:', error);
    }
}

// 筛选论文
function filterPapers() {
    const dateFrom = document.getElementById('dateFrom').value;
    const dateTo = document.getElementById('dateTo').value;
    const category = document.getElementById('categoryFilter').value;
    const markedOnly = document.getElementById('markedOnly').checked;
    const sortBy = document.getElementById('sortBy').value;
    loadPapers(dateFrom, dateTo, category, markedOnly, sortBy);
}

// 重置筛选
function resetFilters() {
    // 重置为默认日期范围：最近7天到今天
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
    const today = new Date();
    
    document.getElementById('dateFrom').value = sevenDaysAgo.toISOString().split('T')[0];
    document.getElementById('dateTo').value = today.toISOString().split('T')[0];
    document.getElementById('categoryFilter').value = '';
    document.getElementById('markedOnly').checked = false;
    document.getElementById('sortBy').value = 'date';
    loadPapers();
}

// 手动获取最新论文
async function fetchNewPapers() {
    const fetchDays = document.getElementById('fetchDays').value;
    const daysText = fetchDays === '1' ? '1天' : `${fetchDays}天`;
    
    if (!confirm(`确定要获取最近${daysText}的论文吗？这可能需要几分钟时间。`)) return;
    
    const loading = document.getElementById('loading');
    const errorDiv = document.getElementById('errorMessage');
    
    loading.style.display = 'block';
    errorDiv.innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE}/fetch?days_back=${fetchDays}`, {
            method: 'POST'
        });
        
        if (!response.ok) throw new Error('获取论文失败');
        
        const data = await response.json();
        alert(data.message);
        
        // 重新加载数据
        await loadPapers();
        await loadStats();
    } catch (error) {
        errorDiv.innerHTML = `<div class="error">获取失败: ${error.message}</div>`;
    } finally {
        loading.style.display = 'none';
    }
}

// 工具函数
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN');
}
