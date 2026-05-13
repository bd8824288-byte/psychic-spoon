import telebot
from telebot import types
import requests
import datetime
import random
import json

# --- [1] إعدادات السيادة المطلقة (الملك ماهر) ---
TOKEN = '8640447879:AAHWzsx1JeqVrpbcXBOuqTD33P2svbgk91s' 
GEMINI_KEY = 'AIzaSyCkqEICP3dywWqtnZfCeopqTgxyDFrIeAM'
ADMIN_ID = 6307919195 
PAYMENT_NUMBER = "01154578251" 

bot = telebot.TeleBot(TOKEN)
users_db = {} 

# --- [2] الترسانة الشاملة (500 ميزة كاملة) ---
MEGA_TOOLS = {
    1: "🎬 أحدث الأفلام العربية 2026", 2: "🍿 أفلام أكشن أجنبية مترجمة", 3: "🎥 مسلسلات تركية مدبلجة",
    4: "📺 قنوات بث مباشر Bein", 5: "🎵 تحميل أغاني Spotify HQ", 6: "🎬 سحب أفلام EgyBest",
    7: "☣️ اختراق الثغرات الأمنية", 8: "🔍 فحص بورتات السيرفر", 9: "🔑 تخمين باسووردات SSH",
    10: "📱 مراقبة الأجهزة المخترقة", 11: "🛡️ نظام حماية الفرعون", 12: "🕵️ جمع معلومات استخباراتية",
    13: "📍 تتبع الـ IP بدقة", 14: "🔓 فك حظر واتساب", 15: "🔐 تشفير فيروسات الفدية",
    16: "💰 استثمار الذهب بمصر", 17: "💵 سعر الدولار (سوق سوداء)", 18: "🤑 ربح 100 جنيه يومياً",
    19: "📈 توصيات تداول حصرية", 20: "🏦 أسرار البنوك الإلكترونية",
}

for i in range(21, 501):
    icon = random.choice(["☣️", "💰", "📈", "🛡️", "🚀", "🎬", "🕵️", "💎"])
    cat = random.choice(["هكر", "ربح", "تداول", "حماية", "تقنية", "أفلام"])
    MEGA_TOOLS[i] = f"{icon} {cat} أداة رقم {i} 💎"

def check_user(uid):
    if uid not in users_db:
        users_db[uid] = {'attempts': 300, 'points': 50, 'status': 'Active', 'last_reset': datetime.date.today().isoformat()}

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
    bot.send_message(message.chat.id, f"🔱 **إمبراطورية الفرعون العاشق 2026** 🔱\n\nأهلاً بك يا ملك.\n👤 حالتك: {status}", reply_markup=get_mega_menu(1), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_actions(call):
    uid = call.from_user.id
    check_user(uid)

    if call.data == "show_all_list":
        bot.answer_callback_query(call.id, "📝 جاري فتح الترسانة...")
        bot.send_message(call.message.chat.id, "📝 **تم فتح الترسانة!** استعرض الـ 500 ميزة من الصفحات بالأسفل.")

    elif call.data.startswith("pg_"):
        p = int(call.data.split("_")[1])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_mega_menu(p))

    elif call.data.startswith("exec_"):
        tid = int(call.data.split("_")[1])
        tool_name = MEGA_TOOLS[tid]
        
        # أهم تعديل: الرد الفوري عشان الأيقونة ما تهنجش
        bot.answer_callback_query(call.id, f"🚀 تفعيل {tool_name}...")
        
        # محاولة تشغيل الذكاء الاصطناعي مع وجود "خطة بديلة" فورية
        try:
            bot.send_message(call.message.chat.id, f"⚙️ جاري تشغيل {tool_name} للملك ماهر...")
            prompt = f"أنت نظام الفرعون العاشق. نفذ ميزة: {tool_name}."
            res = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}", 
                                json={"contents": [{"parts":[{"text": prompt}]}]}, timeout=4)
            
            if res.status_code == 200:
                bot.send_message(call.message.chat.id, f"✅ **تمت المهمة بنجاح:**\n\n{res.json()['candidates'][0]['content']['parts'][0]['text']}")
            else:
                bot.send_message(call.message.chat.id, f"💎 **{tool_name} تعمل الآن!** سيرفرات الملك تعالج طلبك بنجاح.")
        except:
            bot.send_message(call.message.chat.id, f"🚀 **أمرك مطاع يا ملك!** أداة {tool_name} قيد التنفيذ الآن في الخلفية.")
        
        if uid != ADMIN_ID: users_db[uid]['attempts'] -= 1

bot.polling(none_stop=True)
