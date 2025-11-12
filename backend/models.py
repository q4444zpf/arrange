from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class NodeType(str, Enum):
    START = "start"
    END = "end"
    TOOL = "tool"
    CONDITION = "condition"
    LOOP = "loop"
    CODE = "code"

class ToolConfig(BaseModel):
    name: str
    description: str
    category: str
    parameters: List[Dict[str, Any]]
    outputs: List[Dict[str, Any]]
    code: str

class ToolCreate(BaseModel):
    name: str
    description: str
    category: str
    config: Dict[str, Any]
    code: str

class ToolResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    config: Dict[str, Any]
    created_at: datetime

class NodeData(BaseModel):
    type: NodeType
    label: str
    tool_id: Optional[int] = None
    config: Dict[str, Any] = Field(default_factory=dict)

class WorkflowNode(BaseModel):
    id: str
    type: str
    data: NodeData
    position: Dict[str, float]

class WorkflowEdge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class WorkflowCreate(BaseModel):
    name: str
    description: str = ""
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)

class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    variables: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

class ExecutionRequest(BaseModel):
    workflow_id: int
    input_data: Dict[str, Any] = Field(default_factory=dict)

class ExecutionResponse(BaseModel):
    id: int
    workflow_id: int
    status: str
    output_data: Optional[Dict[str, Any]] = None
    logs: List[Dict[str, Any]]
    started_at: datetime
    completed_at: Optional[datetime] = None
