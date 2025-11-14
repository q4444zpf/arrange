# 🔍 如何在网页上验证系统

由于我不能直接运行开发服务器，请按照以下步骤手动验证：

## 🚀 方法一：使用测试网页（推荐，最简单）

### 步骤1：启动后端
```bash
cd /workspace/backend
python3 main.py
```

### 步骤2：打开测试页面
在浏览器中打开：
```
file:///workspace/test.html
```

或在VS Code中右键点击 `test.html` → "Open with Live Server"

### 步骤3：测试功能
点击页面上的按钮依次测试：
1. ✅ 检查后端连接
2. ✅ 创建示例工具
3. ✅ 创建测试工作流
4. ✅ 执行工作流

**如果所有测试都显示绿色✅，说明后端运行正常！**

---

## 🎨 方法二：完整前端验证

### 步骤1：启动后端（如果还未启动）
```bash
cd /workspace/backend
python3 main.py
```

### 步骤2：新终端启动前端
```bash
cd /workspace/frontend
npm install
npm run dev
```

### 步骤3：访问应用
在浏览器打开：`http://localhost:5173`

### 步骤4：验证功能

#### 验证1：首页
- [x] 看到标题和按钮
- [x] 工作流列表显示正常

#### 验证2：创建工具
1. 点击"工具管理"
2. 点击"创建工具"
3. 或运行: `cd /workspace/backend && python3 example_tools.py`

#### 验证3：创建工作流
1. 点击"创建工作流"
2. 从左侧拖拽"HTTP GET请求"到画布
3. 拖拽"结束"节点到画布
4. 连接节点（从开始→工具→结束）
5. 点击工具节点，配置属性：
   - url: `https://jsonplaceholder.typicode.com/posts/1`
6. 点击"保存"

#### 验证4：执行工作流
1. 点击"执行"
2. 输入：`{}`
3. 查看执行结果

---

## 📊 验证检查清单

### 后端 ✅
- [x] 代码语法检查通过
- [x] 所有依赖已安装
- [x] 服务可以启动
- [ ] API响应正常（需要手动测试）

### 前端 ⏳
- [ ] 依赖安装成功（需要运行 npm install）
- [ ] 开发服务器启动（需要运行 npm run dev）
- [ ] 页面正常渲染
- [ ] 可视化编排功能正常

### 功能测试 ⏳
- [ ] 工具创建功能
- [ ] 工作流编辑功能
- [ ] 节点拖拽功能
- [ ] 工作流执行功能

---

## 🎯 快速验证命令

### 仅验证后端API（无需前端）
```bash
# 终端1：启动后端
cd /workspace/backend && python3 main.py

# 终端2：测试API
curl http://localhost:8000/
curl http://localhost:8000/api/tools/
curl http://localhost:8000/api/workflows/

# 创建示例工具
cd /workspace/backend && python3 example_tools.py
```

### 验证前端页面
```bash
# 确保后端已启动
# 然后
cd /workspace/frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

---

## 📸 预期效果

### Test.html 测试页面
![测试页面](https://via.placeholder.com/800x600?text=测试页面示意)
- 紫色渐变背景
- 白色卡片布局
- 测试按钮整齐排列
- 结果显示区域

### 前端应用
![前端界面](https://via.placeholder.com/1200x800?text=工作流编辑器)
- 左侧：节点面板（可折叠）
- 中间：灰色网格画布
- 右侧：属性配置面板
- 顶部：黑色导航栏

### 节点样式
- 🟢 开始节点：绿色渐变
- 🔵 工具节点：蓝色渐变
- 🟡 条件节点：橙色渐变
- 🔵 循环节点：青色渐变
- 🟣 代码节点：紫色渐变
- 🔴 结束节点：红色渐变

---

## ❓ 常见问题

### Q1: 后端启动失败？
```bash
# 检查端口占用
lsof -i :8000

# 重新安装依赖
cd /workspace/backend
pip install -r requirements.txt
```

### Q2: 前端无法连接后端？
- 确保后端在8000端口运行
- 检查浏览器控制台错误
- 尝试直接访问 http://localhost:8000

### Q3: test.html 看不到？
- 使用文件路径打开：`file:///workspace/test.html`
- 或使用 Python HTTP 服务器：
```bash
cd /workspace
python3 -m http.server 8080
# 访问 http://localhost:8080/test.html
```

---

## ✅ 验证成功标志

**后端验证成功：**
- ✅ test.html 所有测试显示绿色
- ✅ API文档可访问 (http://localhost:8000/docs)
- ✅ 可以创建工具和工作流

**前端验证成功：**
- ✅ 页面正常渲染
- ✅ 可以拖拽节点
- ✅ 可以连接节点
- ✅ 可以保存工作流
- ✅ 可以执行工作流并看到结果

---

## 🎉 验证完成后

恭喜！系统运行正常，你现在可以：

1. 📚 查看完整文档：README.md
2. 🔧 创建自定义工具
3. 🎨 构建复杂工作流
4. 🚀 集成到实际项目

**享受可视化编排的乐趣！🎉**
