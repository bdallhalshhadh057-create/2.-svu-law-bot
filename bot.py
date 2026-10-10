import telebot
import requests
import time

# 🎯 ضع رموزك السرية الحقيقية هنا مباشرة بين الإشارات المفردة
TELEGRAM_TOKEN = '8759883213:AAEBmd8e2nx3wUxdjDInk9__M-kR9ILC9PE'
GEMINI_API_KEY = 'AQ.Ab8RN6LWZznIPo4-M9EIdRzl45vKIAG0xUEIVdWqmwU1Vq6lGQ
'

# تنظيف الاتصال وفصل المنصة القديمة تلقائياً قبل البدء
try:
    print("⏳ جاري تنظيف الاتصال وفصل المنصة القديمة تلقائياً...")
    temp_bot = telebot.TeleBot(TELEGRAM_TOKEN)
    temp_bot.delete_webhook(drop_pending_updates=True)
    print("✅ تم فصل المنصة القديمة بنجاح! البوت مستعد لذكاء Gemini.")
    time.sleep(1)
except Exception as e:
    pass

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# التوجيه الأكاديمي التخصصي لتبسيط منهاج الحقوق في الجامعة الافتراضية السورية
system_prompt = (
    "أنت بروفيسور ومدرس أكاديمي خبير في كلية الحقوق بالجامعة الافتراضية السورية.\n"
    "عند الإجابة على أسئلة الطلاب، يجب أن تلتزم بدقة بالأساليب الاحترافية التالية:\n"
    "1. [المفاهيم]: استخرج المصطلحات القانونية المحورية وحددها أكاديمياً بدقة.\n"
    "2. [الشرح المبسط]: قدم شرحاً سهلاً وسلساً يسهل استيعابه دون الإخلال بالمعنى القانوني السوري.\n"
    "3. [الأمثلة الحية]: أرفق مع كل قاعدة قانونية مثالاً تطبيقياً واقعياً (قضية افتراضية) من واقع المحاكم السورية.\n"
    "4. [المخطط البصري]: ارسم هيكلية الأفكار على شكل مخطط نصي شجري منظم ومفهوم.\n"
    "5. [التركيز الامتحاني]: ركز على النقاط الخلافية المتكررة في الامتحانات، وصغ في النهاية سؤال أتمتة (MCQ) احترافياً.\n\n"
    "تنبيه صارم: التزم فقط بالحقائق والمناهج القانونية السورية المعتمدة ولا تخترع معلومات خارجها."
)

def ask_gemini_ai(user_message):
    # الاتصال المباشر بخادم جوجل الرسمي لتشغيل نموذج Gemini 2.5 Flash أو Gemini 1.5 Pro
    url = f"https://googleapis.com{GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\n\nسؤال الطالب المباشر:\n{user_message}"}
                ]
            }
        ]
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"⚠️ عذراً، واجهت مشكلة في معالجة الطلب عبر خادم Gemini. الرمز: {response.status_code}"
    except Exception as e:
        return "❌ خطأ في الاتصال بالبيانات الأكاديمية."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "⚖️ مرحباً بك في موسوعة الحقوق الشاملة SVU الذكية المدعومة بذكاء Gemini!\n\n"
        "أنا مساعدك الأكاديمي لتبسيط المنهاج بالاعتماد على الكتب والصوتيات المعتمدة.\n"
        "💬 أرسل لي أي سؤال أو فكرة معقدة، وسأقوم بشرحها لك بالأمثلة والمخططات فوراً!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_student_chat(message):
    chat_id = message.chat.id
    user_query = message.text
    bot.send_chat_action(chat_id, 'typing')
    
    bot_reply = ask_gemini_ai(user_query)
    bot.reply_to(message, bot_reply, parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
  
