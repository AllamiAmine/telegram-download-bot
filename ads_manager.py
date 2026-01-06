# 📢 نظام إدارة الإعلانات المتقدم
# ================================

import json
import random
from datetime import datetime, date
from config import ADS_LIST, MAX_ADS_PER_USER_DAILY, STATS_FILE

# ملف المستخدمين
USERS_FILE = "users.json"


class AdsManager:
    def __init__(self):
        self.stats = self.load_stats()
        self.users = self.load_users()
        self.user_ad_count = {}
        self.last_ad_index = {}
    
    def load_stats(self):
        """تحميل الإحصائيات"""
        try:
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "total_downloads": 0,
                "total_ads_shown": 0,
                "ad_clicks": {},
                "daily_stats": {},
                "user_stats": {}
            }
    
    def save_stats(self):
        """حفظ الإحصائيات"""
        try:
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving stats: {e}")
    
    def load_users(self):
        """تحميل بيانات المستخدمين"""
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_users(self):
        """حفظ بيانات المستخدمين"""
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def register_user(self, user_id: int, first_name: str = None, username: str = None):
        """تسجيل مستخدم جديد"""
        user_id = str(user_id)
        today = str(date.today())
        
        if user_id not in self.users:
            self.users[user_id] = {
                "first_name": first_name,
                "username": username,
                "first_use": today,
                "last_use": today,
                "total_downloads": 0
            }
            self.save_users()
        else:
            self.users[user_id]["last_use"] = today
            if first_name:
                self.users[user_id]["first_name"] = first_name
            if username:
                self.users[user_id]["username"] = username
            self.save_users()
    
    def get_user_stats(self, user_id: int) -> dict:
        """الحصول على إحصائيات المستخدم"""
        user_id = str(user_id)
        
        if user_id in self.users:
            downloads = self.users[user_id].get("total_downloads", 0)
            first_use = self.users[user_id].get("first_use", "غير معروف")
            
            # حساب المستوى
            if downloads >= 100:
                level = "💎 ماسي"
            elif downloads >= 50:
                level = "🥇 ذهبي"
            elif downloads >= 20:
                level = "🥈 فضي"
            elif downloads >= 5:
                level = "🥉 برونزي"
            else:
                level = "⭐ مبتدئ"
            
            return {
                "downloads": downloads,
                "first_use": first_use,
                "level": level
            }
        
        return {
            "downloads": 0,
            "first_use": "لم تستخدم البوت بعد",
            "level": "⭐ مبتدئ"
        }
    
    def get_active_ads(self):
        """جلب الإعلانات النشطة"""
        return [ad for ad in ADS_LIST if ad.get("active", True)]
    
    def get_next_ad(self, user_id: int):
        """جلب الإعلان التالي (كلاسيكي)"""
        user_id = str(user_id)
        today = str(date.today())
        
        if user_id not in self.user_ad_count:
            self.user_ad_count[user_id] = {"date": today, "count": 0}
        
        if self.user_ad_count[user_id]["date"] != today:
            self.user_ad_count[user_id] = {"date": today, "count": 0}
        
        if self.user_ad_count[user_id]["count"] >= MAX_ADS_PER_USER_DAILY:
            return None
        
        active_ads = self.get_active_ads()
        if not active_ads:
            return None
        
        last_index = self.last_ad_index.get(user_id, -1)
        
        if len(active_ads) == 1:
            ad_index = 0
        else:
            available_indices = [i for i in range(len(active_ads)) if i != last_index]
            ad_index = random.choice(available_indices)
        
        self.last_ad_index[user_id] = ad_index
        self.user_ad_count[user_id]["count"] += 1
        
        return active_ads[ad_index]
    
    def get_smart_ad(self, user_id: int):
        """جلب إعلان ذكي بناءً على الأولوية"""
        user_id = str(user_id)
        today = str(date.today())
        
        # التحقق من الحد اليومي
        if user_id not in self.user_ad_count:
            self.user_ad_count[user_id] = {"date": today, "count": 0}
        
        if self.user_ad_count[user_id]["date"] != today:
            self.user_ad_count[user_id] = {"date": today, "count": 0}
        
        if self.user_ad_count[user_id]["count"] >= MAX_ADS_PER_USER_DAILY:
            return None
        
        active_ads = self.get_active_ads()
        if not active_ads:
            return None
        
        # ترتيب حسب الأولوية
        sorted_ads = sorted(active_ads, key=lambda x: x.get("priority", 999))
        
        # اختيار إعلان مختلف
        last_index = self.last_ad_index.get(user_id, -1)
        
        # 70% اختيار حسب الأولوية، 30% عشوائي
        if random.random() < 0.7 and len(sorted_ads) > 0:
            # اختيار من أعلى الأولويات
            top_ads = sorted_ads[:min(2, len(sorted_ads))]
            ad = random.choice(top_ads)
        else:
            # اختيار عشوائي
            ad = random.choice(active_ads)
        
        # تحديث العدادات
        ad_index = active_ads.index(ad) if ad in active_ads else 0
        self.last_ad_index[user_id] = ad_index
        self.user_ad_count[user_id]["count"] += 1
        
        return ad
    
    def record_ad_shown(self, user_id: int, ad_id: str):
        """تسجيل عرض الإعلان"""
        today = str(date.today())
        
        self.stats["total_ads_shown"] += 1
        
        if today not in self.stats["daily_stats"]:
            self.stats["daily_stats"][today] = {
                "downloads": 0,
                "ads_shown": 0,
                "clicks": 0
            }
        
        self.stats["daily_stats"][today]["ads_shown"] += 1
        
        if ad_id not in self.stats["ad_clicks"]:
            self.stats["ad_clicks"][ad_id] = {"shown": 0, "clicks": 0}
        
        self.stats["ad_clicks"][ad_id]["shown"] += 1
        
        self.save_stats()
    
    def record_download(self, user_id: int):
        """تسجيل عملية تحميل"""
        today = str(date.today())
        user_id = str(user_id)
        
        self.stats["total_downloads"] += 1
        
        if today not in self.stats["daily_stats"]:
            self.stats["daily_stats"][today] = {
                "downloads": 0,
                "ads_shown": 0,
                "clicks": 0
            }
        
        self.stats["daily_stats"][today]["downloads"] += 1
        
        # تحديث إحصائيات المستخدم
        if user_id not in self.stats["user_stats"]:
            self.stats["user_stats"][user_id] = {
                "total_downloads": 0,
                "first_use": today
            }
        
        self.stats["user_stats"][user_id]["total_downloads"] += 1
        
        # تحديث ملف المستخدمين
        if user_id in self.users:
            self.users[user_id]["total_downloads"] = self.users[user_id].get("total_downloads", 0) + 1
            self.save_users()
        
        self.save_stats()
    
    def record_click(self, ad_id: str):
        """تسجيل نقرة على الإعلان"""
        today = str(date.today())
        
        if ad_id in self.stats["ad_clicks"]:
            self.stats["ad_clicks"][ad_id]["clicks"] += 1
        
        if today in self.stats["daily_stats"]:
            self.stats["daily_stats"][today]["clicks"] += 1
        
        self.save_stats()
    
    def get_stats_report(self):
        """تقرير الإحصائيات (كلاسيكي)"""
        today = str(date.today())
        today_stats = self.stats["daily_stats"].get(today, {
            "downloads": 0,
            "ads_shown": 0,
            "clicks": 0
        })
        
        total_shown = self.stats["total_ads_shown"]
        total_clicks = sum(ad.get("clicks", 0) for ad in self.stats["ad_clicks"].values())
        ctr = (total_clicks / total_shown * 100) if total_shown > 0 else 0
        
        report = f"""📊 **إحصائيات Bot**

📅 **اليوم ({today}):**
• التحميلات: {today_stats['downloads']}
• الإعلانات: {today_stats['ads_shown']}
• النقرات: {today_stats.get('clicks', 0)}

📈 **الإجمالي:**
• التحميلات: {self.stats['total_downloads']}
• الإعلانات: {self.stats['total_ads_shown']}
• CTR: {ctr:.1f}%
• المستخدمين: {len(self.users)}"""
        
        return report
    
    def get_admin_report(self):
        """تقرير المشرف المتقدم"""
        today = str(date.today())
        today_stats = self.stats["daily_stats"].get(today, {
            "downloads": 0,
            "ads_shown": 0,
            "clicks": 0
        })
        
        total_shown = self.stats["total_ads_shown"]
        total_clicks = sum(ad.get("clicks", 0) for ad in self.stats["ad_clicks"].values())
        ctr = (total_clicks / total_shown * 100) if total_shown > 0 else 0
        
        # حساب متوسط التحميلات
        days = len(self.stats["daily_stats"]) or 1
        avg_downloads = self.stats["total_downloads"] / days
        
        report = f"""👑 **لوحة تحكم المشرف**

━━━━━━━━━━━━━━━━━
📅 **إحصائيات اليوم ({today}):**
├ 📥 التحميلات: {today_stats['downloads']}
├ 📢 الإعلانات: {today_stats['ads_shown']}
└ 👆 النقرات: {today_stats.get('clicks', 0)}

━━━━━━━━━━━━━━━━━
📈 **الإحصائيات الكلية:**
├ 📥 إجمالي التحميلات: {self.stats['total_downloads']}
├ 📢 إجمالي الإعلانات: {self.stats['total_ads_shown']}
├ 📊 نسبة النقر (CTR): {ctr:.1f}%
├ 👥 المستخدمين: {len(self.users)}
└ 📉 متوسط التحميلات/يوم: {avg_downloads:.1f}

━━━━━━━━━━━━━━━━━
💰 **أداء الإعلانات:**"""
        
        for ad_id, ad_stats in self.stats["ad_clicks"].items():
            shown = ad_stats.get("shown", 0)
            clicks = ad_stats.get("clicks", 0)
            ad_ctr = (clicks / shown * 100) if shown > 0 else 0
            status = "🟢" if ad_ctr > 2 else "🟡" if ad_ctr > 0.5 else "🔴"
            report += f"\n{status} {ad_id}: {clicks}/{shown} ({ad_ctr:.1f}%)"
        
        return report


# إنشاء instance
ads_manager = AdsManager()
