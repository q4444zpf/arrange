from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db, Tool
from models import ToolCreate, ToolResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=ToolResponse)
async def create_tool(tool: ToolCreate, db: AsyncSession = Depends(get_db)):
    """创建新工具"""
    db_tool = Tool(
        name=tool.name,
        description=tool.description,
        category=tool.category,
        config=tool.config,
        code=tool.code
    )
    db.add(db_tool)
    await db.commit()
    await db.refresh(db_tool)
    return db_tool

@router.get("/", response_model=List[ToolResponse])
async def get_tools(db: AsyncSession = Depends(get_db)):
    """获取所有工具"""
    result = await db.execute(select(Tool))
    tools = result.scalars().all()
    return tools

@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(tool_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个工具"""
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    return tool

@router.delete("/{tool_id}")
async def delete_tool(tool_id: int, db: AsyncSession = Depends(get_db)):
    """删除工具"""
    result = await db.execute(select(Tool).where(Tool.id == tool_id))
    tool = result.scalar_one_or_none()
    if not tool:
        raise HTTPException(status_code=404, detail="工具不存在")
    await db.delete(tool)
    await db.commit()
    return {"message": "工具已删除"}
