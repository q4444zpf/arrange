#!/usr/bin/env python3
"""
代码验证脚本
检查后端代码的语法和依赖
"""

import sys
import subprocess
import os

def check_syntax(file_path):
    """检查Python文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        return True, None
    except SyntaxError as e:
        return False, str(e)

def check_imports():
    """检查必要的依赖是否可导入"""
    modules = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'sqlalchemy',
    ]
    
    missing = []
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    return missing

def main():
    print("=" * 60)
    print("🔍 开始验证后端代码")
    print("=" * 60)
    
    # 检查文件语法
    files_to_check = [
        'backend/main.py',
        'backend/database.py',
        'backend/models.py',
        'backend/routers/tools.py',
        'backend/routers/workflows.py',
        'backend/routers/execution.py',
        'backend/engine/executor.py',
    ]
    
    syntax_errors = []
    for file_path in files_to_check:
        full_path = os.path.join('/workspace', file_path)
        if os.path.exists(full_path):
            success, error = check_syntax(full_path)
            if success:
                print(f"✅ {file_path} - 语法正确")
            else:
                print(f"❌ {file_path} - 语法错误: {error}")
                syntax_errors.append((file_path, error))
        else:
            print(f"⚠️  {file_path} - 文件不存在")
    
    print("\n" + "=" * 60)
    print("📦 检查Python依赖")
    print("=" * 60)
    
    missing = check_imports()
    if missing:
        print(f"⚠️  缺少以下依赖: {', '.join(missing)}")
        print("   请运行: pip install -r backend/requirements.txt")
    else:
        print("✅ 所有主要依赖已安装")
    
    print("\n" + "=" * 60)
    print("📊 验证总结")
    print("=" * 60)
    
    if syntax_errors:
        print(f"❌ 发现 {len(syntax_errors)} 个语法错误")
        for file_path, error in syntax_errors:
            print(f"   - {file_path}: {error}")
        return 1
    elif missing:
        print("⚠️  代码语法正确，但需要安装依赖")
        return 2
    else:
        print("✅ 所有检查通过！可以启动服务")
        print("\n下一步:")
        print("1. 启动后端: cd backend && python3 main.py")
        print("2. 启动前端: cd frontend && npm install && npm run dev")
        print("3. 访问: http://localhost:5173")
        return 0

if __name__ == '__main__':
    sys.exit(main())
