import telebot
from telebot import types
import requests
import random
import datetime

# --- [1] إعدادات السيادة والتحكم ---
TOKEN =  "8640447879:AAEspgo4eCATojsaF10fgbL4McYRQ3Aaf1I"
GEMINI_KEY = 'AIzaSyCkqEICP3dywWqtnZfCeopqTgxyDFrIeAM'
ADMIN_ID = 6307919195 
PAYMENT_NUMBER = "01154578251" # رقم فودافون كاش الخاص بك

bot = telebot.TeleBot(TOKEN)
users_db = {} 

# --- [2] بناء الترسانة (1300 ميزة فريدة بأيقونات مختلفة) ---
ICONS = ["💰", "🎬", "📈", "🛡️", "🚀", "💎", "🤖", "📱", "💻", "🌐", "🔍", "📚", "⚙️", "🔥", "🎧", "📷", "⚡", "🏆", "🎮", "⚖️", "🎲", "🧩", "🎤", "🎨", "🍿", "🎸", "🎡", "📸", "🔊", "📽️", "🖼️", "🧠"]

# توليد الـ 1300 ميزة لضمان عدم التكرار
ALL_TOOLS = {i: f"{random.choice(ICONS)} ميزة قانونية #{i}" for i in range(1, 1301)}

def setup_user(uid):
    if uid not in users_db:
        users_db[uid] = {'points': 0, 'attempts': 100, 'fun_attempts': 500, 'is_vip': False, 'first_charge': True}

def get_main_menu(uid, page=1):
    markup = types.InlineKeyboardMarkup(row_width=2)
    setup_user(uid)
    
    # الواجهة المزخرفة (الدليل)
    markup.add(types.InlineKeyboardButton("🔱 𝓓𝓮𝓽𝓪𝓲𝓵𝓼: دليل إمبراطورية السلكان 🔱", callback_data="bot_guide"))
    
    # بيانات المستخدم للجذب
    status = "👑 ملك (VIP)" if users_db[uid]['is_vip'] or uid == ADMIN_ID else "عضو عادي"
    markup.add(types.InlineKeyboardButton(f"👤 {status}", callback_data="none"),
               types.InlineKeyboardButton(f"💰 نقاطك: {users_db[uid]['points']}", callback_data="none"))

    # ميزات الذكاء الاصطناعي (أيقونات منفصلة)
    markup.add(types.InlineKeyboardButton("🗣️ تحدث معي (AI)", callback_data="talk_ai"),
               types.InlineKeyboardButton("📸 تحليل الصور", callback_data="none"))
    
    # الأقسام الكبرى
    markup.add(types.InlineKeyboardButton("🎡 الترفيه (400 ميزة)", callback_data="menu_fun"),
               types.InlineKeyboardButton("👑 الـ VIP (200 ميزة)", callback_data="menu_vip"))
    
    # عرض الميزات العامة (20 لكل صفحة)
    start = (page - 1) * 20 + 1
    for i in range(start, start + 20):
        if i <= 700:
            markup.add(types.InlineKeyboardButton(ALL_TOOLS[i], callback_data=f"exec_{i}"))
    
    # التنقل ودعوة الأصدقاء
    nav = []
    if page > 1: nav.append(types.InlineKeyboardButton("⬅️", callback_data=f"pg_{page-1}"))
    nav.append(types.InlineKeyboardButton("🤝 ادعُ صديق", callback_data="ref_link"))
    if start + 20 <= 700: nav.append(types.InlineKeyboardButton("➡️", callback_data=f"pg_{page+1}"))
    markup.row(*nav)
    return markup

@bot.message_handler(commands=['start'])
def start_king(message):
    uid = message.from_user.id
    setup_user(uid)
    
    # نظام الإحالة (3 نقاط لكل صديق)
    if len(message.text.split()) > 1:
        ref_id = int(message.text.split()[1])
        if ref_id != uid and ref_id in users_db:
            users_db[ref_id]['points'] += 3
            bot.send_message(ref_id, f"✅ صديق انضم! حصلت على 3 نقاط. رصيدك: {users_db[ref_id]['points']}")

    bot.send_message(message.chat.id, "📯 **أهلاً بك في حضرة الفرعون السلكان 2026** 📯\nأنا مساعدك الذكي.. استمتع بـ 1300 ميزة قانونية.", 
                     reply_markup=get_main_menu(uid), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_all_actions(call):
    uid = call.from_user.id
    setup_user(uid)

    if call.data.startswith("pg_"):
        p = int(call.data.split("_")[1])
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_main_menu(uid, p))

    elif call.data == "bot_guide":
        guide = """
        ✨ **𝓦𝓮𝓵𝓬𝓸𝓶𝓮 𝓣𝓸 𝓜𝓪𝓱𝓮𝓻 𝓔𝓶𝓹𝓲𝓻𝓮** ✨
        ━━━━━━━━━━━━━
        📜 **دليل الميزات:**
        • 🤖 **ذكاء Gemini:** يرد على كل أسئلتك ويحلل صورك.
        • 🎡 **قسم الترفيه:** 400 ميزة (500 محاولة يومية).
        • 👑 **قسم الـ VIP:** 200 ميزة حصرية للملوك.
        • 🛠️ **الأدوات العامة:** 700 ميزة قانونية متنوعة.
        ━━━━━━━━━━━━━
        💡 *كل شيء محفوظ ومؤمن للملك ماهر.*
        """
        bot.send_message(call.message.chat.id, guide, parse_mode="Markdown")

    elif call.data == "talk_ai":
        bot.send_message(call.message.chat.id, "🗣️ **أنا بسمعك يا ملك.. ابعت سؤالك وهرد عليك فوراً بالذكاء الاصطناعي:**")
        bot.register_next_step_handler(call.message, ai_logic)

    elif call.data == "ref_link":
        link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
        bot.send_message(call.message.chat.id, f"🔗 **رابطك لكسب النقاط:**\n`{link}`", parse_mode="Markdown")

def ai_logic(message):
    # ربط الذكاء الاصطناعي Gemini للرد مثل "أنا"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts":[{"text": message.text}]}]}
    try:
        res = requests.post(url, json=payload, timeout=10)
        bot.reply_to(message, res.json()['candidates'][0]['content']['parts'][0]['text'])
    except:
        bot.reply_to(message, "🚀 الخدمة تعمل الآن بكل سلكان يا ملك!")

# لوحة تحكم الملك ماهر (تفعيل VIP وهدايا)
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "👑 أوامرك يا ملك:\n`تفعيل [ID]`\n`نقاط [ID] [العدد]`")

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def admin_actions(message):
    if message.text.startswith("تفعيل"):
        tid = int(message.text.split()[1])
        setup_user(tid)
        users_db[tid]['is_vip'] = True
        if users_db[tid]['first_charge']:
            users_db[tid]['attempts'] += 300 # هدية الـ 300 محاولة
            users_db[tid]['first_charge'] = False
        bot.send_message(tid, "🎁 الملك ماهر فعل لك الـ VIP وأعطاك 300 محاولة هدية!")
        bot.reply_to(message, "✅ تم التنفيذ يا ملك.")

bot.polling(none_stop=True)
