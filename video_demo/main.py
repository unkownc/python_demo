from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import yt_dlp
from pathlib import Path
import os

app = FastAPI()

# 配置静态文件和模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 配置下载目录
VIDEO_DIR = Path("downloads/video")
AUDIO_DIR = Path("downloads/audio")
VIDEO_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

def download_youtube_video(url):
    try:
        # yt-dlp 基础配置
        common_opts = {
            'cookiefile': r'www.youtube.com_cookies.txt',
            'quiet': False,
            'no_warnings': False,
            'verbose': True,
            'proxy': 'http://127.0.0.1:10809',
            'socket_timeout': 30,
            'retries': 3,
            'nocheckcertificate': True,
            'prefer_insecure': True
        }

        # 视频下载选项
        video_opts = {
            **common_opts,
            'format': 'best[ext=mp4][height<=720]/best[height<=720]/best',
            'outtmpl': str(VIDEO_DIR / '%(title)s.%(ext)s'),
        }

        # 音频下载选项
        audio_opts = {
            **common_opts,
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'outtmpl': str(AUDIO_DIR / '%(title)s.%(ext)s'),
        }

        # 获取视频信息
        with yt_dlp.YoutubeDL(common_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            duration = info['duration']
            thumbnail = info['thumbnail']
            author = info.get('uploader', 'Unknown')
            views = info.get('view_count', 0)

        # 下载视频
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])

        # 下载音频
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])

        # 获取下载后的文件路径
        video_file = next(VIDEO_DIR.glob(f"{title}.*"))
        audio_file = next(AUDIO_DIR.glob(f"{title}.*"))

        return {
            "status": "success",
            "title": title,
            "author": author,
            "duration": f"{duration // 60}:{duration % 60:02d}",
            "views": views,
            "thumbnail": thumbnail,
            "video_path": str(video_file.name),
            "audio_path": str(audio_file.name)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download")
async def download_video_route(request: Request, url: str = Form(...)):
    try:
        result = download_youtube_video(url)
        
        if result["status"] == "success":
            video_info = {
                "title": result["title"],
                "author": result["author"],
                "length": result["duration"],
                "views": result["views"],
                "thumbnail": result["thumbnail"]
            }
            
            return templates.TemplateResponse("result.html", {
                "request": request,
                "video_info": video_info,
                "video_path": f"/downloads/video/{result['video_path']}",
                "audio_path": f"/downloads/audio/{result['audio_path']}",
                "success": True
            })
        else:
            raise Exception(result["message"])
            
    except Exception as e:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "error": str(e),
            "success": False
        })

# 配置下载目录的静态文件服务
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads") 