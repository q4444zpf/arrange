from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tools, workflows, execution
from database import init_db

app = FastAPI(title="API编排引擎", version="1.0.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(tools.router, prefix="/api/tools", tags=["工具管理"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["工作流管理"])
app.include_router(execution.router, prefix="/api/execution", tags=["执行引擎"])

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "API编排引擎运行中"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
