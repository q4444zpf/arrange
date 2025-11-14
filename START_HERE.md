# 🚀 从这里开始

欢迎使用 **可视化API编排引擎**！

## ⚡ 快速验证（推荐）

### 方法1: 使用测试网页（最简单）

1. **启动后端服务**
```bash
cd /workspace/backend
python3 main.py
```

2. **打开测试页面**
在浏览器中打开: `file:///workspace/test.html`

或者在终端运行:
```bash
# Linux/Mac
open /workspace/test.html
# 或
xdg-open /workspace/test.html
```

3. **点击测试按钮**
   - ✅ 检查后端连接
   - ✅ 创建示例工具
   - ✅ 创建测试工作流
   - ✅ 执行工作流

### 方法2: 完整体验

1. **终端1 - 启动后端**
```bash
cd /workspace/backend
python3 main.py
```
访问: http://localhost:8000/docs 查看API文档

2. **终端2 - 启动前端**
```bash
cd /workspace/frontend
npm install
npm run dev
```
访问: http://localhost:5173 使用完整应用

3. **终端3 - 创建示例工具**
```bash
cd /workspace/backend
python3 example_tools.py
```

## 📋 详细验证步骤

如果需要详细的手动验证步骤，请查看:
- **MANUAL_VERIFICATION.md** - 完整的验证检查清单

## 📚 完整文档

- **README.md** - 系统完整文档
- **QUICKSTART.md** - 快速启动指南

## 🎯 核心功能

✨ **可视化编排**: 拖拽式工作流构建
🔧 **工具管理**: 自定义Python工具
🔀 **条件分支**: 基于条件的流程控制
🔄 **循环控制**: for/while循环支持
💻 **代码执行**: 内嵌Python代码
📊 **执行监控**: 实时日志和结果追踪

## 🛠 技术栈

- **前端**: Vue 3 + Ant Design Vue + Vue Flow
- **后端**: Python + FastAPI + SQLAlchemy

## ❓ 遇到问题？

### 后端无法启动
```bash
# 检查依赖
cd /workspace/backend
pip install -r requirements.txt

# 检查端口
lsof -i :8000
```

### 前端无法访问
```bash
# 重新安装依赖
cd /workspace/frontend
rm -rf node_modules
npm install
```

### 数据库问题
```bash
# 删除并重建数据库
rm /workspace/backend/workflow.db
# 重启后端服务
```

## 🎉 开始使用

选择上面的验证方法之一，立即开始体验可视化API编排！

---

**问题或建议？** 请查看文档或创建Issue
