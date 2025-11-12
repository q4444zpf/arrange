from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db, Workflow
from models import WorkflowCreate, WorkflowResponse
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(workflow: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    """创建工作流"""
    db_workflow = Workflow(
        name=workflow.name,
        description=workflow.description,
        nodes=workflow.nodes,
        edges=workflow.edges,
        variables=workflow.variables
    )
    db.add(db_workflow)
    await db.commit()
    await db.refresh(db_workflow)
    return db_workflow

@router.get("/", response_model=List[WorkflowResponse])
async def get_workflows(db: AsyncSession = Depends(get_db)):
    """获取所有工作流"""
    result = await db.execute(select(Workflow))
    workflows = result.scalars().all()
    return workflows

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(workflow_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个工作流"""
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    return workflow

@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(workflow_id: int, workflow: WorkflowCreate, db: AsyncSession = Depends(get_db)):
    """更新工作流"""
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    db_workflow = result.scalar_one_or_none()
    if not db_workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    db_workflow.name = workflow.name
    db_workflow.description = workflow.description
    db_workflow.nodes = workflow.nodes
    db_workflow.edges = workflow.edges
    db_workflow.variables = workflow.variables
    db_workflow.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(db_workflow)
    return db_workflow

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: int, db: AsyncSession = Depends(get_db)):
    """删除工作流"""
    result = await db.execute(select(Workflow).where(Workflow.id == workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    await db.delete(workflow)
    await db.commit()
    return {"message": "工作流已删除"}
