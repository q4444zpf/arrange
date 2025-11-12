#!/usr/bin/env python3
"""
后端API测试脚本
启动后端服务并运行基本功能测试
"""

import asyncio
import httpx
import time
import subprocess
import sys
import signal
import os

backend_process = None

def start_backend():
    """启动后端服务"""
    global backend_process
    print("🚀 启动后端服务...")
    backend_process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd="/workspace/backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # 等待服务启动
    time.sleep(3)
    print("✅ 后端服务已启动")

def stop_backend():
    """停止后端服务"""
    global backend_process
    if backend_process:
        print("\n🛑 停止后端服务...")
        backend_process.send_signal(signal.SIGTERM)
        backend_process.wait(timeout=5)
        print("✅ 后端服务已停止")

async def test_api():
    """测试API功能"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        print("\n" + "=" * 60)
        print("🧪 开始API测试")
        print("=" * 60)
        
        # 1. 测试根路径
        try:
            response = await client.get(f"{base_url}/")
            assert response.status_code == 200
            print("✅ 测试1: 根路径访问 - 通过")
        except Exception as e:
            print(f"❌ 测试1: 根路径访问 - 失败: {e}")
            return False
        
        # 2. 测试获取工具列表
        try:
            response = await client.get(f"{base_url}/api/tools/")
            assert response.status_code == 200
            tools = response.json()
            print(f"✅ 测试2: 获取工具列表 - 通过 (共{len(tools)}个工具)")
        except Exception as e:
            print(f"❌ 测试2: 获取工具列表 - 失败: {e}")
            return False
        
        # 3. 测试创建工具
        try:
            tool_data = {
                "name": "测试工具",
                "description": "这是一个测试工具",
                "category": "测试",
                "config": {"parameters": []},
                "code": "def execute(inputs, context):\n    return 'Hello World'"
            }
            response = await client.post(f"{base_url}/api/tools/", json=tool_data)
            assert response.status_code == 200
            tool = response.json()
            tool_id = tool["id"]
            print(f"✅ 测试3: 创建工具 - 通过 (ID: {tool_id})")
        except Exception as e:
            print(f"❌ 测试3: 创建工具 - 失败: {e}")
            return False
        
        # 4. 测试获取工作流列表
        try:
            response = await client.get(f"{base_url}/api/workflows/")
            assert response.status_code == 200
            workflows = response.json()
            print(f"✅ 测试4: 获取工作流列表 - 通过 (共{len(workflows)}个工作流)")
        except Exception as e:
            print(f"❌ 测试4: 获取工作流列表 - 失败: {e}")
            return False
        
        # 5. 测试创建工作流
        try:
            workflow_data = {
                "name": "测试工作流",
                "description": "测试工作流",
                "nodes": [
                    {
                        "id": "node_1",
                        "type": "custom",
                        "position": {"x": 100, "y": 100},
                        "data": {"type": "start", "label": "开始", "config": {}}
                    },
                    {
                        "id": "node_2",
                        "type": "custom",
                        "position": {"x": 100, "y": 200},
                        "data": {"type": "end", "label": "结束", "config": {}}
                    }
                ],
                "edges": [
                    {
                        "id": "edge_1",
                        "source": "node_1",
                        "target": "node_2"
                    }
                ],
                "variables": {}
            }
            response = await client.post(f"{base_url}/api/workflows/", json=workflow_data)
            assert response.status_code == 200
            workflow = response.json()
            workflow_id = workflow["id"]
            print(f"✅ 测试5: 创建工作流 - 通过 (ID: {workflow_id})")
        except Exception as e:
            print(f"❌ 测试5: 创建工作流 - 失败: {e}")
            return False
        
        # 6. 测试执行工作流
        try:
            execution_data = {
                "workflow_id": workflow_id,
                "input_data": {"test": "data"}
            }
            response = await client.post(f"{base_url}/api/execution/run", json=execution_data)
            assert response.status_code == 200
            result = response.json()
            print(f"✅ 测试6: 执行工作流 - 通过 (状态: {result['status']})")
        except Exception as e:
            print(f"❌ 测试6: 执行工作流 - 失败: {e}")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 所有API测试通过！")
        print("=" * 60)
        return True

def main():
    try:
        start_backend()
        result = asyncio.run(test_api())
        
        if result:
            print("\n✅ 后端验证成功！")
            print("\n📝 下一步:")
            print("1. 保持后端运行")
            print("2. 新终端运行: cd frontend && npm install && npm run dev")
            print("3. 访问: http://localhost:5173")
            print("\n按 Ctrl+C 停止后端服务")
            
            # 保持运行直到用户中断
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n收到中断信号")
        else:
            print("\n❌ 后端验证失败")
            return 1
            
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        stop_backend()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
