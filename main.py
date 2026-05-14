import telebot
from telebot import types
import requests
import random

# --- [1] إعدادات السيادة والتحكم ---
TOKEN = "8738795425:AAG1m5eqcpYeLv48q1A737rhq3wNREIPn98"
GEMINI_KEY = 'AIzaSyCkqEICP3dywWqtnZfCeopqTgxyDFrIeAM'
ADMIN_ID = 6307919195 
PAYMENT_NUMBER = "01154578251"

bot = telebot.TeleBot(TOKEN)
users_db = {} 

# أيقونات الميزات
ICONS = ["💰", "🎬", "📈", "🛡️", "🚀", "💎", "🤖", "📱", "💻", "🌐", "🔍", "📚", "⚙️", "🔥", "🎧", "📷", "⚡", "🏆", "🎮", "⚖️", "🎲", "🧩", "🎤", "🎨", "🍿", "🎸", "🎡", "📸", "🔊", "📽️", "🖼️", "🧠"]
ALL_TOOLS = {i: f"{random.choice(ICONS)} ميزة قانونية #{i}" for i in range(1, 1301)}

def setup_user(uid):
    if uid not in users_db:
        users_db[uid] = {'points': 0, 'attempts': 100, 'is_vip': False, 'first_charge': True}

def get_main_menu(uid, page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    setup_user(uid)
    status = "👑 ملك (VIP)" if users_db[uid]['is_vip'] or uid == ADMIN_ID else "عضو عادي"
    markup.add(types.InlineKeyboardButton(f"👤 {status}", callback_data="none"),
               types.InlineKeyboardButton(f"💰 نقاطك: {users_db[uid]['points']}", callback_data="none"))
    markup.add(types.InlineKeyboardButton("🗣️ تحدث معي (AI)", callback_data="talk_ai"))
    
    start = (page - 1) * 20 + 1
    for i in range(start, start + 20):
        if i <= 1300:
            markup.add(types.InlineKeyboardButton(ALL_TOOLS[i], callback_data=f"exec_{i}"))
    
    nav = [types.InlineKeyboardButton("🤝 ادعُ صديق", callback_data="ref_link")]
    if page > 1: nav.insert(0, types.InlineKeyboardButton("⬅️", callback_data=f"pg_{page-1}"))
    if start + 20 <= 1300: nav.append(types.InlineKeyboardButton("➡️", callback_data=f"pg_{page+1}"))
    markup.row(*nav)
    return markup

@bot.message_handler(commands=['start'])
def start_king(message):
    uid = message.from_user.id
    setup_user(uid)
    bot.send_message(message.chat.id, "📯 **أهلاً بك في حضرة الفرعون العاشق 2026**", 
                     reply_markup=get_main_menu(uid), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_actions(call):
    uid = call.from_user.id
    setup_user(uid)

    if call.data.startswith("pg_"):
        p = int(call.data.split("_")[1])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_main_menu(uid, p))

    elif call.data.startswith("exec_"):
        f_id = int(call.data.split("_")[1])
        # --- تحديث أول 50 ميزة قانونية ---
        if 1 <= f_id <= 50:
            if f_id == 1: msg = "📖 سورة البقرة بصوت المعيقلي جاهزة في الترسانة."
            elif f_id == 10: msg = "💰 سعر الدولار اليوم في مصر حوالي 48.60 ج.م."
            elif f_id == 16: msg = "🌤️ الجو في مصر النهاردة مشمس وجميل يا فرعون."
            else: msg = f"🛠️ الميزة {f_id} قانونية وجاهزة للعمل."
            bot.send_message(call.message.chat.id, msg)
        else:
            bot.answer_callback_query(call.id, "الميزات من 51 لـ 1300 قيد التحديث في الدفعة الجاية!")

    elif call.data == "talk_ai":
        bot.send_message(call.message.chat.id, "🗣️ ابعت سؤالك وهرد عليك بالذكاء الاصطناعي:")
        bot.register_next_step_handler(call.message, ai_logic)

    elif call.data == "ref_link":
        link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        bot.send_message(call.message.chat.id, f"🔗 رابطك:\n`{link}`")

def ai_logic(message):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    try:
        res = requests.post(url, json={"contents": [{"parts":[{"text": message.text}]}]})
        bot.reply_to(message, res.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        bot.reply_to(message, "🚀 الخدمة مهنجة شوية يا ملك!")

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "👑 أوامر الملك:\n`تفعيل ID`\n`نقاط ID العدد`")

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def admin_actions(message):
    if message.text.startswith("تفعيل"):
        tid = int(message.text.split()[1])
        setup_user(tid)
        users_db[tid]['is_vip'] = True
        users_db[tid]['attempts'] += 300
        bot.send_message(tid, "🎁 الملك ماهر فعل لك الـ VIP!")
    elif message.text.startswith("نقاط"):
        _, tid, amt = message.text.split()
        users_db[int(tid)]['points'] += int(amt)
        bot.reply_to(message, "✅ تم توزيع النقاط.")

bot.polling(none_stop=True)
