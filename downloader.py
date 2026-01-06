# 📥 نظام تحميل الفيديوهات المتقدم
# ================================

import os
import re
import asyncio
import time
from urllib.parse import urlparse
from config import SUPPORTED_PLATFORMS, MAX_FILE_SIZE_MB, DOWNLOAD_TIMEOUT

# محاولة استيراد yt-dlp
try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False
    print("⚠️ yt-dlp غير مثبت. قم بتثبيته: pip install yt-dlp")


class VideoDownloader:
    def __init__(self):
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        self.cleanup_old_files()  # تنظيف عند البدء
    
    def is_supported_url(self, url: str) -> bool:
        """التحقق من أن الرابط مدعوم"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower().replace("www.", "")
            
            for platform in SUPPORTED_PLATFORMS:
                if platform in domain:
                    return True
            return False
        except:
            return False
    
    def extract_url(self, text: str) -> str:
        """استخراج الرابط من النص"""
        # أنماط متعددة للروابط
        patterns = [
            r'https?://[^\s<>"{}|\\^`\[\]]+',
            r'www\.[^\s<>"{}|\\^`\[\]]+',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                url = match.group(0)
                # إضافة https:// إذا كان يبدأ بـ www
                if url.startswith('www.'):
                    url = 'https://' + url
                # تنظيف الرابط
                url = url.rstrip('.,;:!?')
                return url
        return None
    
    def get_platform_name(self, url: str) -> str:
        """معرفة اسم المنصة مع أيقونة"""
        domain = urlparse(url).netloc.lower()
        
        platforms = {
            "youtube": "🎬 YouTube",
            "youtu.be": "🎬 YouTube",
            "tiktok": "📱 TikTok",
            "instagram": "📸 Instagram",
            "twitter": "🐦 Twitter",
            "x.com": "🐦 X",
            "facebook": "📘 Facebook",
            "fb.watch": "📘 Facebook",
            "reddit": "🔴 Reddit",
            "vimeo": "📹 Vimeo",
            "dailymotion": "🎥 Dailymotion",
            "twitch": "🎮 Twitch",
            "pinterest": "📌 Pinterest",
            "snapchat": "👻 Snapchat",
        }
        
        for key, name in platforms.items():
            if key in domain:
                return name
        
        return "🌐 Unknown"
    
    async def download_video(self, url: str, user_id: int) -> dict:
        """
        تحميل الفيديو مع دعم متقدم
        Returns: {"success": bool, "file_path": str, "title": str, "error": str}
        """
        if not YT_DLP_AVAILABLE:
            return {
                "success": False,
                "error": "yt-dlp غير مثبت"
            }
        
        # تنظيف الملفات القديمة للمستخدم
        self._cleanup_user_files(user_id)
        
        timestamp = int(time.time())
        output_template = os.path.join(
            self.download_dir,
            f"{user_id}_{timestamp}_%(title).40s.%(ext)s"
        )
        
        max_size = MAX_FILE_SIZE_MB * 1024 * 1024  # تحويل إلى bytes
        
        ydl_opts = {
            # استخدام format يتجنب الحاجة لـ ffmpeg - فيديو واحد بدون دمج
            'format': 'best[ext=mp4][vcodec!*=av01]/best[ext=mp4]/best[vcodec!*=av01]/best',
            'outtmpl': output_template,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 3,
            # منع أي عملية تحتاج ffmpeg
            'postprocessors': [],
            'prefer_free_formats': False,
            'check_formats': False,
            # تحسينات للمنصات المختلفة
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            },
            # خيارات إضافية
            'ignoreerrors': False,
            'no_color': True,
            'geo_bypass': True,
            'nocheckcertificate': True,
        }
        
        # إعدادات خاصة لكل منصة
        domain = urlparse(url).netloc.lower()
        
        # YouTube يحتاج إعدادات خاصة لتجنب ffmpeg
        if 'youtube' in domain or 'youtu.be' in domain:
            # صيغ YouTube الجاهزة بدون ffmpeg
            ydl_opts['format'] = 'best[ext=mp4][height<=720]/best[ext=mp4]/18/22/best'
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        elif 'tiktok' in domain:
            # TikTok إعدادات خاصة
            ydl_opts['format'] = 'best'
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://www.tiktok.com/',
                'Accept': '*/*',
            }
            ydl_opts['extractor_args'] = {'tiktok': {'api_hostname': 'api22-normal-c-useast1a.tiktokv.com'}}
        elif 'instagram' in domain:
            ydl_opts['format'] = 'best'
        elif 'twitter' in domain or 'x.com' in domain:
            ydl_opts['format'] = 'best'
        
        try:
            # تشغيل التحميل مع timeout
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    lambda: self._download_sync(url, ydl_opts)
                ),
                timeout=DOWNLOAD_TIMEOUT
            )
            return result
            
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "انتهت مهلة التحميل. جرب فيديو أقصر."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _download_sync(self, url: str, ydl_opts: dict) -> dict:
        """تحميل متزامن"""
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if info is None:
                    return {"success": False, "error": "فشل في استخراج معلومات الفيديو"}
                
                title = info.get('title', 'video')
                # تنظيف العنوان
                title = re.sub(r'[<>:"/\\|?*]', '', title)[:100]
                
                file_path = ydl.prepare_filename(info)
                
                # البحث عن الملف (قد يكون بامتداد مختلف)
                if not os.path.exists(file_path):
                    base_path = os.path.splitext(file_path)[0]
                    for ext in ['.mp4', '.webm', '.mkv', '.mov', '.avi', '.flv']:
                        if os.path.exists(base_path + ext):
                            file_path = base_path + ext
                            break
                
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    max_size = MAX_FILE_SIZE_MB * 1024 * 1024
                    
                    if file_size > max_size:
                        os.remove(file_path)
                        return {
                            "success": False,
                            "error": f"الفيديو كبير جداً ({file_size // (1024*1024)}MB). الحد الأقصى {MAX_FILE_SIZE_MB}MB"
                        }
                    
                    return {
                        "success": True,
                        "file_path": file_path,
                        "title": title,
                        "duration": info.get('duration', 0),
                        "platform": info.get('extractor', 'Unknown'),
                        "thumbnail": info.get('thumbnail'),
                        "view_count": info.get('view_count', 0),
                    }
                else:
                    return {"success": False, "error": "الملف لم يتم تحميله بشكل صحيح"}
                    
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            
            if "video unavailable" in error_msg or "not available" in error_msg:
                return {"success": False, "error": "الفيديو غير متوفر أو محذوف"}
            elif "private" in error_msg:
                return {"success": False, "error": "الفيديو خاص"}
            elif "sign in" in error_msg or "login" in error_msg:
                return {"success": False, "error": "الفيديو يتطلب تسجيل الدخول"}
            elif "copyright" in error_msg:
                return {"success": False, "error": "الفيديو محمي بحقوق النشر"}
            elif "age" in error_msg:
                return {"success": False, "error": "الفيديو مقيد بالعمر"}
            elif "geo" in error_msg or "country" in error_msg:
                return {"success": False, "error": "الفيديو غير متاح في منطقتك"}
            else:
                return {"success": False, "error": f"خطأ: {str(e)[:150]}"}
        except Exception as e:
            return {"success": False, "error": str(e)[:150]}
    
    def cleanup_file(self, file_path: str):
        """حذف الملف بعد الإرسال"""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file: {e}")
    
    def _cleanup_user_files(self, user_id: int):
        """حذف ملفات المستخدم القديمة"""
        try:
            prefix = f"{user_id}_"
            for filename in os.listdir(self.download_dir):
                if filename.startswith(prefix):
                    file_path = os.path.join(self.download_dir, filename)
                    try:
                        os.remove(file_path)
                    except:
                        pass
        except:
            pass
    
    def cleanup_old_files(self, max_age_hours: int = 1):
        """حذف الملفات القديمة"""
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(self.download_dir):
                file_path = os.path.join(self.download_dir, filename)
                if os.path.isfile(file_path):
                    file_age = current_time - os.path.getmtime(file_path)
                    if file_age > max_age_seconds:
                        try:
                            os.remove(file_path)
                        except:
                            pass
        except:
            pass


# إنشاء instance
downloader = VideoDownloader()
