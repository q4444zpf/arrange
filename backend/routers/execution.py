from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db, Workflow, Tool, ExecutionLog
from models import ExecutionRequest, ExecutionResponse
from engine.executor import WorkflowExecutor
from datetime import datetime

router = APIRouter()

@router.post("/run", response_model=ExecutionResponse)
async def execute_workflow(request: ExecutionRequest, db: AsyncSession = Depends(get_db)):
    """执行工作流"""
    # 获取工作流
    result = await db.execute(select(Workflow).where(Workflow.id == request.workflow_id))
    workflow = result.scalar_one_or_none()
    if not workflow:
        raise HTTPException(status_code=404, detail="工作流不存在")
    
    # 创建执行日志
    execution_log = ExecutionLog(
        workflow_id=request.workflow_id,
        status="running",
        input_data=request.input_data,
        logs=[]
    )
    db.add(execution_log)
    await db.commit()
    await db.refresh(execution_log)
    
    try:
        # 执行工作流
        executor = WorkflowExecutor(workflow, db)
        result = await executor.execute(request.input_data)
        
        # 更新执行日志
        execution_log.status = "completed"
        execution_log.output_data = result["output"]
        execution_log.logs = result["logs"]
        execution_log.completed_at = datetime.utcnow()
        
    except Exception as e:
        execution_log.status = "failed"
        execution_log.logs = [{"level": "error", "message": str(e)}]
        execution_log.completed_at = datetime.utcnow()
        raise HTTPException(status_code=500, detail=f"工作流执行失败: {str(e)}")
    
    finally:
        await db.commit()
        await db.refresh(execution_log)
    
    return execution_log

@router.get("/logs/{execution_id}", response_model=ExecutionResponse)
async def get_execution_log(execution_id: int, db: AsyncSession = Depends(get_db)):
    """获取执行日志"""
    result = await db.execute(select(ExecutionLog).where(ExecutionLog.id == execution_id))
    log = result.scalar_one_or_none()
    if not log:
        raise HTTPException(status_code=404, detail="执行日志不存在")
    return log
