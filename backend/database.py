from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./workflow.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Tool(Base):
    __tablename__ = "tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    category = Column(String(50))
    config = Column(JSON)  # 工具配置（输入/输出参数等）
    code = Column(Text)  # 工具执行代码
    created_at = Column(DateTime, default=datetime.utcnow)

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(Text)
    nodes = Column(JSON)  # 节点列表
    edges = Column(JSON)  # 连接关系
    variables = Column(JSON)  # 全局变量
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExecutionLog(Base):
    __tablename__ = "execution_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, index=True)
    status = Column(String(20))  # running, completed, failed
    input_data = Column(JSON)
    output_data = Column(JSON)
    logs = Column(JSON)  # 执行日志
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with async_session_maker() as session:
        yield session
