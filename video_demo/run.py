import uvicorn
import os

def check_directories():
    """确保必要的目录存在"""
    directories = [
        'static',
        'templates',
        'downloads',
        'downloads/video',
        'downloads/audio'
    ]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

if __name__ == "__main__":
    # 检查并创建必要的目录
    check_directories()
    
    # 配置并启动服务器
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True,
        reload_dirs=["templates", "static"],
        log_level="info"
    ) 