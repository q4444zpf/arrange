"""
示例工具脚本
运行此脚本将在数据库中创建一些示例工具
"""

import asyncio
import httpx

async def create_example_tools():
    """创建示例工具"""
    
    base_url = "http://localhost:8000"
    
    tools = [
        {
            "name": "HTTP GET请求",
            "description": "发送HTTP GET请求并返回JSON响应",
            "category": "API",
            "config": {
                "parameters": [
                    {"name": "url", "type": "string", "required": True, "description": "请求URL"}
                ],
                "outputs": [
                    {"name": "result", "type": "object", "description": "响应数据"}
                ]
            },
            "code": """def execute(inputs, context):
    import httpx
    url = inputs.get('url')
    response = httpx.get(url)
    return response.json()"""
        },
        {
            "name": "HTTP POST请求",
            "description": "发送HTTP POST请求",
            "category": "API",
            "config": {
                "parameters": [
                    {"name": "url", "type": "string", "required": True},
                    {"name": "data", "type": "object", "required": True}
                ]
            },
            "code": """def execute(inputs, context):
    import httpx
    url = inputs.get('url')
    data = inputs.get('data', {})
    response = httpx.post(url, json=data)
    return response.json()"""
        },
        {
            "name": "文本处理-转大写",
            "description": "将文本转换为大写",
            "category": "文本处理",
            "config": {
                "parameters": [
                    {"name": "text", "type": "string", "required": True}
                ]
            },
            "code": """def execute(inputs, context):
    text = inputs.get('text', '')
    return text.upper()"""
        },
        {
            "name": "文本处理-分割",
            "description": "按分隔符分割文本",
            "category": "文本处理",
            "config": {
                "parameters": [
                    {"name": "text", "type": "string", "required": True},
                    {"name": "separator", "type": "string", "required": False}
                ]
            },
            "code": """def execute(inputs, context):
    text = inputs.get('text', '')
    sep = inputs.get('separator', ',')
    return text.split(sep)"""
        },
        {
            "name": "数学计算-加法",
            "description": "计算两个数的和",
            "category": "数据处理",
            "config": {
                "parameters": [
                    {"name": "a", "type": "number", "required": True},
                    {"name": "b", "type": "number", "required": True}
                ]
            },
            "code": """def execute(inputs, context):
    a = float(inputs.get('a', 0))
    b = float(inputs.get('b', 0))
    return a + b"""
        },
        {
            "name": "JSON解析",
            "description": "解析JSON字符串",
            "category": "数据处理",
            "config": {
                "parameters": [
                    {"name": "json_str", "type": "string", "required": True}
                ]
            },
            "code": """def execute(inputs, context):
    import json
    json_str = inputs.get('json_str', '{}')
    return json.loads(json_str)"""
        },
        {
            "name": "数组过滤",
            "description": "根据条件过滤数组",
            "category": "数据处理",
            "config": {
                "parameters": [
                    {"name": "array", "type": "array", "required": True},
                    {"name": "key", "type": "string", "required": True},
                    {"name": "value", "type": "any", "required": True}
                ]
            },
            "code": """def execute(inputs, context):
    array = inputs.get('array', [])
    key = inputs.get('key')
    value = inputs.get('value')
    
    result = []
    for item in array:
        if isinstance(item, dict) and item.get(key) == value:
            result.append(item)
    return result"""
        },
        {
            "name": "延时等待",
            "description": "等待指定秒数",
            "category": "其他",
            "config": {
                "parameters": [
                    {"name": "seconds", "type": "number", "required": True}
                ]
            },
            "code": """def execute(inputs, context):
    import time
    seconds = float(inputs.get('seconds', 1))
    time.sleep(seconds)
    return f"等待了{seconds}秒""""
        },
        {
            "name": "生成随机数",
            "description": "生成指定范围的随机数",
            "category": "其他",
            "config": {
                "parameters": [
                    {"name": "min", "type": "number", "required": True},
                    {"name": "max", "type": "number", "required": True}
                ]
            },
            "code": """def execute(inputs, context):
    import random
    min_val = int(inputs.get('min', 0))
    max_val = int(inputs.get('max', 100))
    return random.randint(min_val, max_val)"""
        },
        {
            "name": "当前时间",
            "description": "获取当前时间戳和格式化时间",
            "category": "其他",
            "config": {
                "parameters": []
            },
            "code": """def execute(inputs, context):
    from datetime import datetime
    now = datetime.now()
    return {
        "timestamp": now.timestamp(),
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S")
    }"""
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for tool in tools:
            try:
                response = await client.post(f"{base_url}/api/tools/", json=tool)
                if response.status_code == 200:
                    print(f"✅ 创建工具成功: {tool['name']}")
                else:
                    print(f"❌ 创建工具失败: {tool['name']} - {response.text}")
            except Exception as e:
                print(f"❌ 创建工具失败: {tool['name']} - {str(e)}")

if __name__ == "__main__":
    print("开始创建示例工具...")
    print("请确保后端服务已启动 (python main.py)")
    print("-" * 50)
    asyncio.run(create_example_tools())
    print("-" * 50)
    print("完成!")
