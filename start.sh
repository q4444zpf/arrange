#!/bin/bash

echo "🚀 启动API编排引擎"
echo "================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未找到Node.js，请先安装Node.js"
    exit 1
fi

echo "📦 安装后端依赖..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "📦 安装前端依赖..."
cd ../frontend
npm install

echo ""
echo "✅ 依赖安装完成!"
echo ""
echo "================================"
echo "启动服务:"
echo "1. 后端: cd backend && python main.py"
echo "2. 前端: cd frontend && npm run dev"
echo ""
echo "然后访问: http://localhost:5173"
echo "================================"
