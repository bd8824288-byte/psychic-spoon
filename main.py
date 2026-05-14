import telebot
from telebot import types
import requests
import random
import os

# --- [1] إعدادات السيادة المطلقة ---
TOKEN = "8738795425:AAG1m5eqcpYeLv48q1A737rhq3wNREIPn98"
GEMINI_KEY = 'AIzaSyCkqEICP3dywWqtnZfCeopqTgxyDFrIeAM'
ADMIN_ID = 6307919195 
CASH_NUMBER = "01154578251"

bot = telebot.TeleBot(TOKEN)
users_db = {} 

ICONS = ["💰", "🎬", "🛡️", "🚀", "💎", "🤖", "📱", "💻", "🌐", "🔍", "📚", "⚙️", "🔥", "🎧", "📷", "⚡", "🏆", "🎮", "⚖️", "🎲"]

def setup_user(uid):
    if uid not in users_db:
        # 100 محاولة يومية + نظام النقاط + حالة الـ VIP
        users_db[uid] = {'points': 0, 'attempts': 100, 'is_vip': False, 'joined': True}

def get_main_menu(uid, page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    setup_user(uid)
    
    # واجهة الملك
    status = "👑 VIP الملك" if users_db[uid]['is_vip'] or uid == ADMIN_ID else "👤 عضو عادي"
    markup.add(types.InlineKeyboardButton(f"{status} | نقاطك: {users_db[uid]['points']}", callback_data="none"))
    markup.add(types.InlineKeyboardButton(f"🎟️ المحاولات المتبقية: {users_db[uid]['attempts']}", callback_data="none"))
    
    # تقسيم الـ 1300 ميزة في صفحات
    start = (page - 1) * 20 + 1
    for i in range(start, start + 20):
        if i <= 1300:
            icon = random.choice(ICONS)
            markup.add(types.InlineKeyboardButton(f"{icon} ميزة #{i}", callback_data=f"exec_{i}"))
    
    # أزرار التحكم
    nav = [types.InlineKeyboardButton("🤝 اكسب نقاط", callback_data="ref_link")]
    if page > 1: nav.insert(0, types.InlineKeyboardButton("⬅️", callback_data=f"pg_{page-1}"))
    if start + 20 <= 1300: nav.append(types.InlineKeyboardButton("➡️", callback_data=f"pg_{page+1}"))
    markup.row(*nav)
    return markup

@bot.message_handler(commands=['start'])
def start_king(message):
    uid = message.from_user.id
    setup_user(uid)
    
    # نظام الإحالة (3 نقاط)
    if len(message.text.split()) > 1:
        ref_id = int(message.text.split()[1])
        if ref_id != uid and ref_id in users_db:
            users_db[ref_id]['points'] += 3
            bot.send_message(ref_id, "✅ صديق انضم عبر رابطك! حصلت على 3 نقاط.")

    bot.send_message(message.chat.id, "📯 **أهلاً بك في محراب الفرعون العاشق 2026**\nالـ 1300 ميزة تعمل الآن بالذكاء الاصطناعي الكامل.", 
                     reply_markup=get_main_menu(uid))

@bot.callback_query_handler(func=lambda call: True)
def handle_actions(call):
    uid = call.from_user.id
    setup_user(uid)

    if call.data.startswith("pg_"):
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_main_menu(uid, int(call.data.split("_")[1])))

    elif call.data.startswith("exec_"):
        f_id = int(call.data.split("_")[1])
        
        # فحص الصلاحيات
        if users_db[uid]['attempts'] > 0 or users_db[uid]['is_vip'] or uid == ADMIN_ID:
            if not users_db[uid]['is_vip'] and uid != ADMIN_ID: users_db[uid]['attempts'] -= 1
            
            # تفعيل الروح بالذكاء الاصطناعي Gemini لكل زرار
            bot.answer_callback_query(call.id, "جاري تحضير القوة الفرعونية... ⚡")
            
            prompt = f"أنت الفرعون المساعد الذكي لماهر. المستخدم ضغط على الميزة رقم {f_id}. قدم له خدمة حقيقية (مثل: معلومة، نصيحة تقنية، كود برمجي، ذكر، أو وظيفة رقمية) بناءً على هذا الرقم."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
            
            try:
                res = requests.post(url, json={"contents": [{"parts":[{"text": prompt}]}]})
                ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                bot.send_message(call.message.chat.id, f"🔱 **الميزة الملكية #{f_id}:**\n\n{ans}")
            except:
                bot.send_message(call.message.chat.id, f"✅ الميزة {f_id} نشطة، لكن هناك ضغط على الخدمة. جرب مرة أخرى يا ملك!")
        else:
            bot.send_message(call.message.chat.id, f"❌ انتهت محاولاتك! اشحن VIP (100 ج) لفتح الـ 1300 ميزة. ابعت لـ `{CASH_NUMBER}`")

    elif call.data == "ref_link":
        link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        bot.send_message(call.message.chat.id, f"🔗 **شارك رابطك واكسب 3 نقاط عن كل صديق:**\n`{link}`")

# --- [2] لوحة تحكم الإمبراطور (خاصة بـ ماهر فقط) ---
@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def admin_commands(message):
    text = message.text
    if text.startswith("تفعيل"):
        try:
            tid = int(text.split()[1])
            setup_user(tid)
            users_db[tid]['is_vip'] = True
            users_db[tid]['attempts'] += 300
            bot.send_message(tid, "🎁 الملك ماهر فعل لك الـ VIP وأعطاك 300 محاولة هدية!")
            bot.reply_to(message, f"✅ تم تفعيل العضو {tid} بنجاح.")
        except: bot.reply_to(message, "الـ ID غلط يا ملك.")
        
    elif text.startswith("نقاط"):
        try:
            _, tid, amt = text.split()
            tid, amt = int(tid), int(amt)
            setup_user(tid)
            users_db[tid]['points'] += amt
            bot.reply_to(message, f"✅ تم إضافة {amt} نقطة للعضو {tid}.")
        except: pass

bot.polling(none_stop=True)
