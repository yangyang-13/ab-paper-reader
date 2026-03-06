@echo off
chcp 65001 >nul
echo ==========================================
echo   AB测试论文阅读系统 - 启动脚本
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python版本：
python --version
echo.

REM 检查是否在项目根目录
if not exist "backend" (
    echo ❌ 错误：请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 进入backend目录
cd backend

REM 检查.env文件
if not exist ".env" (
    echo ⚠️  警告：未找到.env文件，AI功能将无法使用
    echo 请创建.env文件并添加AI配置：
    echo.
    echo 方式1 - 使用OpenAI:
    echo   AI_PROVIDER=openai
    echo   AI_API_KEY=你的API密钥
    echo.
    echo 方式2 - 使用通义千问（推荐国内用户）:
    echo   AI_PROVIDER=qwen
    echo   AI_API_KEY=你的API密钥
    echo.
    echo 方式3 - 使用DeepSeek（最便宜）:
    echo   AI_PROVIDER=deepseek
    echo   AI_API_KEY=你的API密钥
    echo.
    echo 详细配置请查看: docs\AI_PROVIDERS.md
    echo.
    set /p CONTINUE="是否继续启动？(y/n) "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

REM 安装依赖
echo 📦 检查Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

REM 初始化数据库
echo 🗄️  初始化数据库...
python -c "from models import init_db; init_db()"
if errorlevel 1 (
    echo ❌ 数据库初始化失败
    pause
    exit /b 1
)
echo ✅ 数据库初始化成功
echo.

REM 启动后端服务
echo 🚀 启动后端服务...
echo 后端API地址: http://localhost:8000
echo API文档地址: http://localhost:8000/docs
echo.
echo 提示：
echo   - 按 Ctrl+C 停止服务
echo   - 前端页面：在浏览器中打开 frontend\index.html
echo   - 首次使用请点击页面上的'手动获取最新论文'按钮
echo.
echo ==========================================
echo.

REM 启动FastAPI服务
python main.py

pause
