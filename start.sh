#!/bin/bash

echo "=========================================="
echo "  AB测试论文阅读系统 - 启动脚本"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python版本："
python3 --version
echo ""

# 检查是否在项目根目录
if [ ! -d "backend" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 进入backend目录
cd backend

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "❌ 错误：未找到requirements.txt"
    exit 1
fi

# 检查.env文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告：未找到.env文件，AI功能将无法使用"
    echo "请创建.env文件并添加AI配置："
    echo ""
    echo "方式1 - 使用OpenAI:"
    echo "  AI_PROVIDER=openai"
    echo "  AI_API_KEY=你的API密钥"
    echo ""
    echo "方式2 - 使用通义千问（推荐国内用户）:"
    echo "  AI_PROVIDER=qwen"
    echo "  AI_API_KEY=你的API密钥"
    echo ""
    echo "方式3 - 使用DeepSeek（最便宜）:"
    echo "  AI_PROVIDER=deepseek"
    echo "  AI_API_KEY=你的API密钥"
    echo ""
    echo "详细配置请查看: docs/AI_PROVIDERS.md"
    echo ""
    read -p "是否继续启动？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查并安装依赖
echo "📦 检查Python依赖..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "安装依赖中..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖已满足"
fi
echo ""

# 初始化数据库
echo "🗄️  初始化数据库..."
python3 -c "from models import init_db; init_db()"
if [ $? -eq 0 ]; then
    echo "✅ 数据库初始化成功"
else
    echo "❌ 数据库初始化失败"
    exit 1
fi
echo ""

# 启动后端服务
echo "🚀 启动后端服务..."
echo "后端API地址: http://localhost:8000"
echo "API文档地址: http://localhost:8000/docs"
echo ""
echo "提示："
echo "  - 按 Ctrl+C 停止服务"
echo "  - 前端页面：在浏览器中打开 frontend/index.html"
echo "  - 首次使用请点击页面上的'手动获取最新论文'按钮"
echo ""
echo "=========================================="
echo ""

# 启动FastAPI服务
python3 main.py
