# 🚀 快速启动指南

## 1分钟快速体验

### 方式一：使用启动脚本（推荐）

```bash
# 赋予执行权限并运行
chmod +x start.sh
./start.sh
```

### 方式二：手动启动

#### 步骤1: 启动后端服务

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py
```

后端服务将在 `http://localhost:8000` 启动

#### 步骤2: 启动前端服务（新终端）

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端应用将在 `http://localhost:5173` 启动

## 快速测试

### 1. 创建示例工具

后端服务启动后，运行示例工具脚本：

```bash
cd backend
python example_tools.py
```

这将创建10个示例工具，包括：
- HTTP GET/POST请求
- 文本处理（转大写、分割）
- 数学计算
- JSON解析
- 数组过滤
- 延时等待
- 随机数生成
- 当前时间

### 2. 创建第一个工作流

1. 访问 `http://localhost:5173`
2. 点击 **"创建工作流"**
3. 从左侧面板拖拽节点到画布：
   - 开始节点（自动添加）
   - HTTP GET请求工具
   - 代码节点
   - 结束节点
4. 连接节点
5. 配置节点属性
6. 点击保存

### 3. 执行工作流

1. 点击 **"执行"** 按钮
2. 输入JSON格式的输入数据：
```json
{
  "url": "https://jsonplaceholder.typicode.com/posts/1"
}
```
3. 查看执行结果和日志

## 示例工作流

### 示例1: 简单API调用

```
[开始] → [HTTP GET请求] → [结束]
```

配置：
- HTTP GET请求节点：
  - url: `{{url}}` 或直接填写URL
  - 输出变量: `api_result`

### 示例2: 数据处理流程

```
[开始] → [代码节点：生成数据] → [条件分支] → [结束]
                                    ├─ True → [处理A]
                                    └─ False → [处理B]
```

### 示例3: 循环处理

```
[开始] → [代码：创建数组] → [循环节点] → [工具：处理项] → [结束]
```

配置循环节点：
- 循环类型: for
- 迭代变量: `items`
- 循环变量: `item`

## API文档

访问 `http://localhost:8000/docs` 查看完整的API文档

## 常见问题

### Q: 端口被占用怎么办？

**后端端口修改:**
编辑 `backend/main.py`，修改最后一行的端口号：
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # 改成其他端口
```

**前端端口修改:**
编辑 `frontend/vite.config.js`，修改server配置：
```javascript
server: {
  port: 5174  // 改成其他端口
}
```

### Q: 前端无法连接后端？

检查 `frontend/vite.config.js` 中的代理配置是否正确：
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',  // 确保端口正确
    changeOrigin: true
  }
}
```

### Q: 工具执行报错？

1. 检查工具代码是否有语法错误
2. 确保使用了正确的输入参数
3. 查看执行日志了解详细错误信息

## 下一步

1. 探索更多节点类型（条件、循环、代码）
2. 创建自定义工具
3. 构建复杂的工作流
4. 阅读完整文档 `README.md`

---

**开始您的编排之旅! 🎉**
