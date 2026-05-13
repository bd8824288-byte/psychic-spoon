import telebot
from telebot import types
import requests
import datetime
import random
import json
import os

# --- [1] إعدادات السيادة المطلقة (الملك ماهر) ---
# التوكن ومفتاح الذكاء الاصطناعي الخاص بك
TOKEN = '8640447879:AAHWzsx1JeqVrpbcXBOuqTD33P2svbgk91s'
GEMINI_KEY = 'AIzaSyCkqEICP3dywWqtnZfCeopqTgxyDFrIeAM'
ADMIN_ID = 6307919195 # معرف الملك ماهر
PAYMENT_NUMBER = "01154578251" # رقم فودافون كاش للاشتراك

bot = telebot.TeleBot(TOKEN)
users_db = {} # قاعدة البيانات المؤقتة

# --- [2] الترسانة الشاملة (500 ميزة: هكر + أفلام + مال + علم) ---
MEGA_TOOLS = {
    1: "🎬 أحدث الأفلام العربية 2026", 2: "🍿 أفلام أكشن أجنبية مترجمة", 3: "🎥 مسلسلات تركية مدبلجة",
    4: "📺 قنوات بث مباشر Bein", 5: "🎵 تحميل أغاني Spotify HQ", 6: "🎬 سحب أفلام EgyBest",
    7: "☣️ اختراق الثغرات الأمنية", 8: "🔍 فحص بورتات السيرفر", 9: "🔑 تخمين باسووردات SSH",
    10: "📱 مراقبة الأجهزة المخترقة", 11: "🛡️ نظام حماية الفرعون", 12: "🕵️ جمع معلومات استخباراتية",
    13: "📍 تتبع الـ IP بدقة", 14: "🔓 فك حظر واتساب", 15: "🔐 تشفير فيروسات الفدية",
    16: "💰 استثمار الذهب بمصر", 17: "💵 سعر الدولار (سوق سوداء)", 18: "🤑 ربح 100 جنيه يومياً",
    19: "📈 توصيات تداول حصرية", 20: "🏦 أسرار البنوك الإلكترونية",
    21: "📡 اختراق رادارات القرب", 22: "💾 استعادة ملفات تيرمكس", 23: "📸 فك تشفير صور EXIF",
    24: "📝 كتابة سكربتات تخمين", 25: "🛰️ تتبع تحركات الأهداف", 26: "🌋 فحص ملفات الـ Root",
    27: "📧 صنع إيميلات لا نهائية", 28: "📱 تفعيل أرقام تليجرام", 29: "🕵️ بحث عكسي بالصور",
    30: "🛑 منع تتبع الشركات", 31: "🚀 تسريع سيرفرات VPS", 32: "🔋 معايرة أجهزة الـ Android",
    33: "🌡️ مراقبة حرارة السيرفر", 34: "👽 أدوات التخفي التقني", 35: "🤖 صنع بوتات احترافية",
}

for i in range(36, 501):
    icon = random.choice(["☣️", "💰", "📈", "🛡️", "🚀", "🎬", "🕵️", "💎"])
    cat = random.choice(["هكر", "ربح", "تداول", "حماية", "تقنية", "أفلام"])
    MEGA_TOOLS[i] = f"{icon} {cat} أداة رقم {i} 💎"

# --- [3] نظام الإدارة والهدية (300 محاولة) ---
def check_user(uid):
    if uid not in users_db:
        users_db[uid] = {
            'attempts': 300, 
            'points': 50,
            'status': 'Active',
            'last_reset': datetime.date.today().isoformat()
        }
    elif users_db[uid]['last_reset'] != datetime.date.today().isoformat():
        users_db[uid]['attempts'] = 100 
        users_db[uid]['last_reset'] = datetime.date.today().isoformat()

# --- [4] لوحة تحكم الملك (Admin Panel) ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📊 عرض إحصائيات المستخدمين", callback_data="adm_stats"),
            types.InlineKeyboardButton("💰 إضافة نقاط لشخص", callback_data="adm_add_pts"),
            types.InlineKeyboardButton("🚫 حظر مستخدم نهائياً", callback_data="adm_ban")
        )
        bot.send_message(message.chat.id, "🛠️ **لوحة تحكم الملك ماهر:**", reply_markup=markup, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ هذا الأمر للملك فقط.")

# --- [5] القوائم والصفحات ---
def get_mega_menu(page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("🔱 كشف الترسانة الكاملة (500 ميزة) 🔱", callback_data="show_all_list"))
    
    start = (page - 1) * 20 + 1
    for i in range(start, start + 20):
        if i in MEGA_TOOLS:
            markup.add(types.InlineKeyboardButton(MEGA_TOOLS[i], callback_data=f"exec_{i}"))
    
    nav = []
    if page > 1: nav.append(types.InlineKeyboardButton("⬅️ السابق", callback_data=f"pg_{page-1}"))
    if page < 25: nav.append(types.InlineKeyboardButton("التالي ➡️", callback_data=f"pg_{page+1}"))
    markup.row(*nav)
    return markup

@bot.message_handler(commands=['start'])
def start_bot(message):
    uid = message.from_user.id
    check_user(uid)
    status = "👑 الملك (VIP)" if uid == ADMIN_ID else f"المحاولات: {users_db[uid]['attempts']}"
    
    msg = f"🔱 **إمبراطورية الملك ماهر 2026** 🔱\n\nأهلاً بك يا فرعون. تم دمج كل ميزات الهكر والاستثمار والأفلام.\n\n🎁 هدية أول مرة: 300 محاولة مجانية.\n👤 حالتك: {status}\n💰 نقاطك: {users_db[uid]['points']}"
    bot.send_message(message.chat.id, msg, reply_markup=get_mega_menu(1), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_actions(call):
    uid = call.from_user.id
    check_user(uid)

    if call.data == "show_all_list":
        features_txt = "📝 **ترسانة الملك ماهر الكاملة:**\n\n"
        for i in range(1, 41): features_txt += f"{i}- {MEGA_TOOLS[i]}\n"
        bot.send_message(call.message.chat.id, features_txt + "\n... تفقد باقي الـ 500 ميزة في الصفحات!")

    elif call.data.startswith("pg_"):
        p = int(call.data.split("_")[1])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_mega_menu(p))

    elif call.data.startswith("exec_"):
        if users_db[uid]['attempts'] <= 0 and uid != ADMIN_ID:
            msg = f"⛔ انتهت محاولاتك!\n\nلفتح 300 محاولة جديدة:\n1️⃣ ادفع 100 جنيه للرقم: {PAYMENT_NUMBER}\n2️⃣ أو استبدل 50 نقطة بـ 200 محاولة."
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔄 استبدال النقاط", callback_data="buy_points"))
            bot.send_message(call.message.chat.id, msg, reply_markup=markup)
            return

        tid = int(call.data.split("_")[1])
        bot.answer_callback_query(call.id, f"🚀 تفعيل {MEGA_TOOLS[tid]}")
        
        try:
            prompt = f"أنت نظام إمبراطورية الملك ماهر. نفذ الميزة: {MEGA_TOOLS[tid]}. قدم روابط أفلام أو خيارات تقنية احترافية."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            res = requests.post(url, json={"contents": [{"parts":[{"text": prompt}]}]})
            bot.send_message(call.message.chat.id, f"🌟 **تقرير الملك ماهر:**\n\n{res.json()['candidates'][0]['content']['parts'][0]['text']}")
            if uid != ADMIN_ID: users_db[uid]['attempts'] -= 1
        except:
            bot.send_message(call.message.chat.id, "⚠️ هناك ضغط على السيرفر، الملك سيصلحه!")

    elif call.data == "buy_points":
        if users_db[uid]['points'] >= 50:
            users_db[uid]['points'] -= 50
            users_db[uid]['attempts'] += 200
            bot.send_message(call.message.chat.id, "✅ تم شحن 200 محاولة بنجاح!")
        else:
            bot.answer_callback_query(call.id, "❌ نقاطك غير كافية!", show_alert=True)

# --- [6] تشغيل الإمبراطورية ---
print("🚀 كود الملك ماهر الكامل انطلق الآن!")
bot.infinity_polling()
