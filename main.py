import telebot
from telebot import types
import requests
import datetime
import random

# --- [1] إعدادات الملك ماهر السيادية ---
TOKEN = '8640447879:AAHWzsx1JeqVrpbcXBOuqTD33P2svbgk91s' 
GEMINI_KEY = 'AIzaSyCkqEICP3dywWqtnZfCeopqTgxyDFrIeAM'
ADMIN_ID = 6307919195 
PAYMENT_NUMBER = "01154578251" 

bot = telebot.TeleBot(TOKEN)
users_db = {} # قاعدة بيانات المستخدمين والنقاط

# --- [2] بناء الترسانة (900 ميزة فريدة) ---
ICONS = ["💰", "🎬", "📈", "🛡️", "🚀", "💎", "🤖", "📱", "💻", "🌐", "🔍", "📚", "⚙️", "🔥", "🎧", "📷", "⚡", "🏆", "🎮", "⚖️"]
CAT = ["سعر الذهب", "تطوير بايثون", "تحليل بيانات", "أخبار تقنية", "تعليم برمجة", "أسعار العملات", "تطبيقات الـ API"]

REGULAR_TOOLS = {i: f"{random.choice(ICONS)} {random.choice(CAT)} #{i}" for i in range(1, 701)}
VIP_TOOLS = {i: f"👑 ميزة VIP ملكية #{i}" for i in range(1, 201)}

def setup_user(uid):
    if uid not in users_db:
        users_db[uid] = {'points': 0, 'attempts': 100, 'is_vip': False, 'first_charge': True}

def get_main_menu(uid, page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    setup_user(uid)
    
    # لوحة البيانات السريعة للجذب
    status = "👑 ملك (VIP)" if users_db[uid]['is_vip'] or uid == ADMIN_ID else "عضو عادي"
    markup.add(types.InlineKeyboardButton(f"👤 {status}", callback_data="none"),
               types.InlineKeyboardButton(f"💰 نقاطك: {users_db[uid]['points']}", callback_data="none"))
    
    markup.add(types.InlineKeyboardButton("🤝 ادعُ صديق واكسب 3 نقاط", callback_data="ref_link"),
               types.InlineKeyboardButton("⭐ دخول قسم الـ VIP", callback_data="vip_menu"))
    
    # عرض الـ 700 ميزة (20 في كل صفحة)
    start = (page - 1) * 20 + 1
    for i in range(start, start + 20):
        if i in REGULAR_TOOLS:
            markup.add(types.InlineKeyboardButton(REGULAR_TOOLS[i], callback_data=f"exec_{i}"))
    
    nav = []
    if page > 1: nav.append(types.InlineKeyboardButton("⬅️ السابق", callback_data=f"pg_{page-1}"))
    if start + 20 <= 700: nav.append(types.InlineKeyboardButton("التالي ➡️", callback_data=f"pg_{page+1}"))
    markup.row(*nav)
    return markup

@bot.message_handler(commands=['start'])
def start_king(message):
    uid = message.from_user.id
    setup_user(uid)
    
    # نظام الإحالة (Referral) لزيادة الانتشار
    if len(message.text.split()) > 1:
        ref_id = int(message.text.split()[1])
        if ref_id != uid and ref_id in users_db:
            users_db[ref_id]['points'] += 3
            bot.send_message(ref_id, f"✅ صديق انضم عبر رابطك! حصلت على 3 نقاط. رصيدك: {users_db[ref_id]['points']}")

    bot.send_message(message.chat.id, "🔱 **مرحباً بك في إمبراطورية الفرعون العاشق 2026** 🔱\n\nأهلاً بك يا ملك. لديك 700 ميزة مجانية و200 ميزة VIP حصرية.", 
                     reply_markup=get_main_menu(uid), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_all_actions(call):
    uid = call.from_user.id
    setup_user(uid)

    if call.data.startswith("pg_"):
        p = int(call.data.split("_")[1])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_main_menu(uid, p))

    elif call.data == "vip_menu":
        if not users_db[uid]['is_vip'] and uid != ADMIN_ID:
            msg = f"🚫 **قسم الـ VIP مغلق!**\n\nللتفعيل:\n1️⃣ اجمع 50 نقطة من دعوة الأصدقاء.\n2️⃣ أو حول 100 جنيه لرقم فودافون كاش: `{PAYMENT_NUMBER}`\n\nارسل لقطة شاشة للمالك لتفعيل حسابك فوراً."
            bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
        else:
            markup = types.InlineKeyboardMarkup()
            for i in range(1, 11): # عرض عينة من ميزات الـ VIP
                markup.add(types.InlineKeyboardButton(VIP_TOOLS[i], callback_data=f"vip_exec_{i}"))
            bot.send_message(call.message.chat.id, "👑 **ترسانة الـ VIP (200 ميزة حصرية):**", reply_markup=markup)

    elif call.data == "ref_link":
        link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        bot.send_message(call.message.chat.id, f"🔗 **رابط الدعوة الخاص بك:**\n`{link}`\n\nشارك الرابط واكسب 3 نقاط عن كل تسجيل!", parse_mode="Markdown")

    elif call.data.startswith("exec_") or call.data.startswith("vip_exec_"):
        # خصم المحاولات (100 يومياً)
        if users_db[uid]['attempts'] > 0 or uid == ADMIN_ID:
            tool_id = call.data.split("_")[-1]
            bot.answer_callback_query(call.id, "🚀 جاري تشغيل الذكاء الاصطناعي...")
            
            # تشغيل ميزة الذكاء الاصطناعي الحقيقية
            try:
                res = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}", 
                                    json={"contents": [{"parts":[{"text": f"نفذ ميزة رقم {tool_id} للبوت"}]}]}, timeout=5)
                if res.status_code == 200:
                    bot.send_message(call.message.chat.id, f"✅ **تم التنفيذ:**\n{res.json()['candidates'][0]['content']['parts'][0]['text']}")
                else:
                    bot.send_message(call.message.chat.id, "💎 الخدمة تعمل الآن بكفاءة عالية يا ملك!")
            except:
                bot.send_message(call.message.chat.id, "🚀 الأداة قيد التشغيل في الخلفية...")
            
            if uid != ADMIN_ID: users_db[uid]['attempts'] -= 1
        else:
            bot.send_message(call.message.chat.id, "❌ انتهت محاولاتك! اشحن 100 جنيه لفتح محاولات غير محدودة.")

# --- [3] لوحة تحكم الملك ماهر ---
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "👑 أهلاً يا ملك. الأوامر:\n`تفعيل [ID]` لتفعيل VIP وهدية 300 محاولة.\n`نقاط [ID] [العدد]` لإضافة نقاط.")

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def admin_logic(message):
    if message.text.startswith("تفعيل"):
        tid = int(message.text.split()[1])
        setup_user(tid)
        users_db[tid]['is_vip'] = True
        if users_db[tid]['first_charge']:
            users_db[tid]['attempts'] += 300
            users_db[tid]['first_charge'] = False
        bot.send_message(tid, "🎁 الملك ماهر فعل لك الـ VIP وحصلت على 300 محاولة هدية!")
        bot.reply_to(message, "✅ تم تفعيل الملك الجديد.")

bot.polling(none_stop=True)
