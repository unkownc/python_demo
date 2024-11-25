import yt_dlp
from pathlib import Path


def download_youtube_video(url):
    try:
        # 创建下载目录
        video_path = Path("downloads/video")
        audio_path = Path("downloads/audio")
        video_path.mkdir(parents=True, exist_ok=True)
        audio_path.mkdir(parents=True, exist_ok=True)

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

        print("开始下载视频...")
        print(f"使用cookies文件: {common_opts['cookiefile']}")

        # 视频下载选项
        video_opts = {
            **common_opts,
            'format': 'best[ext=mp4][height<=720]/best[height<=720]/best',
            'outtmpl': str(video_path / '%(title)s.%(ext)s'),
        }

        # 音频下载选项
        audio_opts = {
            **common_opts,
            'format': 'bestaudio[ext=m4a]/bestaudio',
            'outtmpl': str(audio_path / '%(title)s.%(ext)s'),
        }

        # 获取视频信息
        print("正在获取视频信息...")
        with yt_dlp.YoutubeDL(common_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            duration = info['duration']
            thumbnail = info['thumbnail']

            print(f"视频标题: {title}")
            print(f"视频时长: {duration // 60}:{duration % 60:02d}")
            print(f"缩略图URL: {thumbnail}")

        # 下载视频
        print("\n开始下载视频文件...")
        with yt_dlp.YoutubeDL(video_opts) as ydl:
            ydl.download([url])

        # 下载音频
        print("\n开始下载音频文件...")
        with yt_dlp.YoutubeDL(audio_opts) as ydl:
            ydl.download([url])

        # 获取下载后的文件路径
        video_file = next(video_path.glob(f"{title}.*"))
        audio_file = next(audio_path.glob(f"{title}.*"))

        print("\n下载完成!")
        print(f"视频文件: {video_file}")
        print(f"音频文件: {audio_file}")

        return {
            "status": "success",
            "title": title,
            "duration": f"{duration // 60}:{duration % 60:02d}",
            "thumbnail": thumbnail,
            "video_path": str(video_file),
            "audio_path": str(audio_file)
        }

    except Exception as e:
        print(f"\n下载过程中出错: {str(e)}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    # 测试URL
    test_url = "https://www.youtube.com/watch?v=_KFzaJSxBcY"

    print("YouTube视频下载测试")
    print("-" * 50)
    print(f"测试URL: {test_url}")
    print("-" * 50)

    result = download_youtube_video(test_url)

    if result["status"] == "success":
        print("\n测试成功!")
        print("-" * 50)
        print(f"标题: {result['title']}")
        print(f"时长: {result['duration']}")
        print(f"视频文件: {result['video_path']}")
        print(f"音频文件: {result['audio_path']}")
    else:
        print("\n测试失败!")
        print("-" * 50)
        print(f"错误信息: {result['message']}")