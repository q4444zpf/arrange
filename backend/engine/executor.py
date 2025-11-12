from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import Tool
import json
import traceback

class WorkflowExecutor:
    """工作流执行引擎"""
    
    def __init__(self, workflow, db: AsyncSession):
        self.workflow = workflow
        self.db = db
        self.context = {}  # 执行上下文，存储变量
        self.logs = []
        
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行工作流"""
        self.context = {**self.workflow.variables, **input_data}
        self.log("info", f"开始执行工作流: {self.workflow.name}")
        
        # 查找起始节点
        start_node = self._find_start_node()
        if not start_node:
            raise ValueError("未找到起始节点")
        
        # 从起始节点开始执行
        result = await self._execute_node(start_node["id"])
        
        self.log("info", "工作流执行完成")
        return {
            "output": result,
            "logs": self.logs,
            "context": self.context
        }
    
    def _find_start_node(self):
        """查找起始节点"""
        for node in self.workflow.nodes:
            if node.get("data", {}).get("type") == "start":
                return node
        return None
    
    async def _execute_node(self, node_id: str) -> Any:
        """执行单个节点"""
        node = self._get_node_by_id(node_id)
        if not node:
            raise ValueError(f"节点不存在: {node_id}")
        
        node_type = node["data"]["type"]
        self.log("info", f"执行节点: {node['data']['label']} (类型: {node_type})")
        
        result = None
        
        if node_type == "start":
            result = await self._execute_start_node(node)
        elif node_type == "end":
            result = await self._execute_end_node(node)
        elif node_type == "tool":
            result = await self._execute_tool_node(node)
        elif node_type == "condition":
            result = await self._execute_condition_node(node)
        elif node_type == "loop":
            result = await self._execute_loop_node(node)
        elif node_type == "code":
            result = await self._execute_code_node(node)
        else:
            raise ValueError(f"未知节点类型: {node_type}")
        
        # 查找下一个节点
        next_nodes = self._get_next_nodes(node_id)
        if next_nodes:
            # 如果是条件节点，result包含要执行的分支
            if node_type == "condition" and isinstance(result, dict) and "next_node" in result:
                next_node_id = result["next_node"]
                if next_node_id:
                    return await self._execute_node(next_node_id)
            else:
                # 执行第一个下游节点
                return await self._execute_node(next_nodes[0])
        
        return result
    
    async def _execute_start_node(self, node: Dict) -> Any:
        """执行起始节点"""
        return self.context
    
    async def _execute_end_node(self, node: Dict) -> Any:
        """执行结束节点"""
        config = node["data"].get("config", {})
        output_key = config.get("output_key", "result")
        return self.context.get(output_key, self.context)
    
    async def _execute_tool_node(self, node: Dict) -> Any:
        """执行工具节点"""
        tool_id = node["data"].get("tool_id")
        config = node["data"].get("config", {})
        
        if not tool_id:
            raise ValueError("工具节点未配置工具ID")
        
        # 获取工具
        result = await self.db.execute(select(Tool).where(Tool.id == tool_id))
        tool = result.scalar_one_or_none()
        if not tool:
            raise ValueError(f"工具不存在: {tool_id}")
        
        # 准备输入参数
        inputs = {}
        for key, value in config.get("inputs", {}).items():
            # 支持变量引用 {{variable}}
            if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
                var_name = value[2:-2].strip()
                inputs[key] = self.context.get(var_name, value)
            else:
                inputs[key] = value
        
        # 执行工具代码
        try:
            # 创建安全的执行环境
            exec_globals = {
                "__builtins__": __builtins__,
                "context": self.context,
                "inputs": inputs,
                "json": json
            }
            exec(tool.code, exec_globals)
            
            # 获取执行结果
            if "execute" in exec_globals:
                result = exec_globals["execute"](inputs, self.context)
            else:
                result = exec_globals.get("result", None)
            
            # 保存结果到上下文
            output_key = config.get("output_key", f"tool_{node['id']}_output")
            self.context[output_key] = result
            
            self.log("success", f"工具执行成功: {tool.name}")
            return result
            
        except Exception as e:
            self.log("error", f"工具执行失败: {tool.name}, 错误: {str(e)}")
            self.log("error", traceback.format_exc())
            raise
    
    async def _execute_condition_node(self, node: Dict) -> Dict:
        """执行条件节点"""
        config = node["data"].get("config", {})
        condition = config.get("condition", "")
        
        # 评估条件
        try:
            # 替换变量
            eval_condition = condition
            for key, value in self.context.items():
                eval_condition = eval_condition.replace(f"{{{{{key}}}}}", str(value))
            
            # 执行条件判断
            result = eval(eval_condition, {"__builtins__": {}}, self.context)
            
            # 根据结果选择分支
            edges = self._get_edges_from_node(node["id"])
            for edge in edges:
                handle = edge.get("sourceHandle", "")
                if (result and handle == "true") or (not result and handle == "false"):
                    self.log("info", f"条件判断: {condition} = {result}, 选择分支: {handle}")
                    return {"next_node": edge["target"]}
            
            return {"next_node": None}
            
        except Exception as e:
            self.log("error", f"条件判断失败: {str(e)}")
            raise
    
    async def _execute_loop_node(self, node: Dict) -> Any:
        """执行循环节点"""
        config = node["data"].get("config", {})
        loop_type = config.get("loop_type", "for")  # for, while
        
        results = []
        
        if loop_type == "for":
            # for循环
            items_key = config.get("items_key", "items")
            items = self.context.get(items_key, [])
            item_var = config.get("item_var", "item")
            
            for idx, item in enumerate(items):
                self.context[item_var] = item
                self.context["loop_index"] = idx
                
                # 执行循环体（下游节点）
                next_nodes = self._get_next_nodes(node["id"])
                if next_nodes:
                    result = await self._execute_node(next_nodes[0])
                    results.append(result)
            
            self.log("info", f"for循环执行完成，迭代次数: {len(items)}")
            
        elif loop_type == "while":
            # while循环
            condition = config.get("condition", "")
            max_iterations = config.get("max_iterations", 100)
            iteration = 0
            
            while iteration < max_iterations:
                # 评估条件
                if not eval(condition, {"__builtins__": {}}, self.context):
                    break
                
                self.context["loop_index"] = iteration
                
                # 执行循环体
                next_nodes = self._get_next_nodes(node["id"])
                if next_nodes:
                    result = await self._execute_node(next_nodes[0])
                    results.append(result)
                
                iteration += 1
            
            self.log("info", f"while循环执行完成，迭代次数: {iteration}")
        
        return results
    
    async def _execute_code_node(self, node: Dict) -> Any:
        """执行代码节点"""
        config = node["data"].get("config", {})
        code = config.get("code", "")
        
        try:
            # 创建执行环境
            exec_globals = {
                "__builtins__": __builtins__,
                "context": self.context,
                "json": json
            }
            
            # 执行代码
            exec(code, exec_globals)
            
            # 获取结果
            result = exec_globals.get("result", None)
            
            # 更新上下文
            if "context" in exec_globals:
                self.context.update(exec_globals["context"])
            
            output_key = config.get("output_key", f"code_{node['id']}_output")
            self.context[output_key] = result
            
            self.log("success", "代码节点执行成功")
            return result
            
        except Exception as e:
            self.log("error", f"代码节点执行失败: {str(e)}")
            self.log("error", traceback.format_exc())
            raise
    
    def _get_node_by_id(self, node_id: str) -> Dict:
        """根据ID获取节点"""
        for node in self.workflow.nodes:
            if node["id"] == node_id:
                return node
        return None
    
    def _get_next_nodes(self, node_id: str) -> List[str]:
        """获取下游节点ID列表"""
        next_nodes = []
        for edge in self.workflow.edges:
            if edge["source"] == node_id:
                next_nodes.append(edge["target"])
        return next_nodes
    
    def _get_edges_from_node(self, node_id: str) -> List[Dict]:
        """获取从节点出发的所有边"""
        edges = []
        for edge in self.workflow.edges:
            if edge["source"] == node_id:
                edges.append(edge)
        return edges
    
    def log(self, level: str, message: str):
        """记录日志"""
        self.logs.append({
            "level": level,
            "message": message,
            "timestamp": str(datetime.now())
        })

from datetime import datetime
