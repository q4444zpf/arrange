# 🔧 可视化API编排引擎

一个强大的可视化工作流编排系统，支持拖拽式API编排、工具注册、条件分支、循环控制和自定义代码执行。界面和功能设计参考了Dify的智能体编排系统。

## ✨ 功能特性

- 🎨 **可视化编排**: 使用拖拽方式构建工作流，直观易用
- 🔧 **工具管理**: 支持自定义工具注册，使用Python编写工具逻辑
- 🔀 **条件分支**: 支持基于条件的流程分支
- 🔄 **循环控制**: 支持for和while循环
- 💻 **自定义代码**: 支持在流程中嵌入Python代码
- 📊 **执行监控**: 实时查看工作流执行日志和结果
- 💾 **持久化存储**: 工作流和工具配置持久化存储

## 🛠 技术栈

### 前端
- **Vue 3**: 渐进式JavaScript框架
- **Ant Design Vue**: UI组件库
- **Vue Flow**: 流程图可视化库
- **Pinia**: 状态管理
- **Vite**: 构建工具

### 后端
- **FastAPI**: 现代化Python Web框架
- **SQLAlchemy**: ORM框架
- **SQLite**: 轻量级数据库
- **Pydantic**: 数据验证

## 📦 项目结构

```
/workspace/
├── backend/                 # 后端Python服务
│   ├── main.py             # FastAPI应用入口
│   ├── database.py         # 数据库模型和连接
│   ├── models.py           # Pydantic模型
│   ├── requirements.txt    # Python依赖
│   ├── routers/            # API路由
│   │   ├── tools.py        # 工具管理API
│   │   ├── workflows.py    # 工作流管理API
│   │   └── execution.py    # 执行引擎API
│   └── engine/             # 执行引擎
│       └── executor.py     # 工作流执行器
│
└── frontend/               # 前端Vue3应用
    ├── package.json        # npm依赖配置
    ├── vite.config.js      # Vite配置
    ├── index.html          # HTML入口
    └── src/
        ├── main.js         # 应用入口
        ├── App.vue         # 根组件
        ├── router/         # 路由配置
        ├── stores/         # Pinia状态管理
        ├── api/            # API接口
        ├── views/          # 页面组件
        │   ├── Home.vue            # 首页
        │   ├── WorkflowEditor.vue  # 工作流编辑器
        │   └── ToolManagement.vue  # 工具管理
        └── components/     # 通用组件
            ├── CustomNode.vue      # 自定义节点
            └── NodeProperties.vue  # 节点属性面板
```

## 🚀 快速开始

### 1. 安装依赖

**后端依赖:**
```bash
cd backend
pip install -r requirements.txt
```

**前端依赖:**
```bash
cd frontend
npm install
```

### 2. 启动服务

**启动后端服务:**
```bash
cd backend
python main.py
```
后端服务将在 `http://localhost:8000` 启动

**启动前端服务:**
```bash
cd frontend
npm run dev
```
前端应用将在 `http://localhost:5173` 启动

### 3. 访问应用

打开浏览器访问: `http://localhost:5173`

## 📖 使用指南

### 创建工具

1. 点击右上角 **"工具管理"** 按钮
2. 点击 **"创建工具"**
3. 填写工具信息:
   - 工具名称
   - 工具描述
   - 分类
   - 输入参数配置（JSON格式）
   - Python执行代码
4. 点击 **"确定"** 保存

**示例工具代码:**
```python
def execute(inputs, context):
    """
    HTTP GET请求工具
    """
    import requests
    url = inputs.get('url')
    response = requests.get(url)
    return response.json()
```

### 创建工作流

1. 在首页点击 **"创建工作流"**
2. 从左侧节点面板拖拽节点到画布
3. 连接节点构建流程
4. 点击节点配置属性（右侧面板）
5. 点击 **"保存"** 保存工作流
6. 点击 **"执行"** 运行工作流

### 节点类型说明

#### 🟢 开始节点
- 工作流的起点
- 每个工作流必须有一个开始节点

#### 🔴 结束节点
- 工作流的终点
- 可配置输出变量

#### 🔵 工具节点
- 执行已注册的工具
- 配置输入参数（支持变量引用）
- 设置输出变量名

#### 🟡 条件分支节点
- 根据条件选择分支
- 支持Python表达式
- 有true和false两个出口

#### 🔵 循环节点
- 支持for循环和while循环
- for循环: 遍历数组
- while循环: 条件循环（需设置最大迭代次数）

#### 🟣 代码节点
- 执行自定义Python代码
- 可访问上下文变量
- 设置输出变量

### 变量引用

在配置中使用 `{{变量名}}` 引用变量:
```
{{input_data}}
{{tool_output}}
{{loop_index}}
```

## 🎯 示例工作流

### 示例1: HTTP API调用流程

1. **开始节点**
2. **工具节点**: HTTP GET请求（获取用户列表）
3. **循环节点**: 遍历用户列表
4. **工具节点**: 处理每个用户数据
5. **结束节点**: 输出处理结果

### 示例2: 数据处理流程

1. **开始节点**
2. **代码节点**: 数据预处理
3. **条件分支**: 检查数据是否有效
   - True分支 → **工具节点**: 保存数据
   - False分支 → **代码节点**: 记录错误
4. **结束节点**

## 🔌 API文档

启动后端服务后，访问以下地址查看自动生成的API文档:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 主要API端点

#### 工具管理
- `GET /api/tools/` - 获取所有工具
- `POST /api/tools/` - 创建工具
- `GET /api/tools/{id}` - 获取工具详情
- `DELETE /api/tools/{id}` - 删除工具

#### 工作流管理
- `GET /api/workflows/` - 获取所有工作流
- `POST /api/workflows/` - 创建工作流
- `GET /api/workflows/{id}` - 获取工作流详情
- `PUT /api/workflows/{id}` - 更新工作流
- `DELETE /api/workflows/{id}` - 删除工作流

#### 执行引擎
- `POST /api/execution/run` - 执行工作流
- `GET /api/execution/logs/{id}` - 获取执行日志

## 🔒 安全注意事项

⚠️ **重要**: 当前版本的代码执行功能使用Python的`exec()`函数，在生产环境中存在安全风险。建议:

1. 在隔离的沙箱环境中运行
2. 限制可导入的模块
3. 添加资源限制（CPU、内存、执行时间）
4. 实施代码审核机制
5. 使用更安全的代码执行方案（如RestrictedPython）

## 🚧 开发计划

- [ ] 工具版本管理
- [ ] 工作流版本控制
- [ ] 更多内置工具
- [ ] 工作流调试模式
- [ ] 定时任务调度
- [ ] Webhook触发
- [ ] 更强的安全沙箱
- [ ] 团队协作功能
- [ ] 工作流模板市场

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题或建议，请通过Issue联系我们。

---

**享受可视化编排的乐趣! 🎉**
