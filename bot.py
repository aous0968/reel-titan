import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

TOKEN = "8352635837:AAGJSKwGK3h1bxTHzNIqG_0hj4uohZcK8Qw"


# تخزين بيانات المستخدمين
users = {}

# النصوص
texts = {
    "comedy": [
        "الحياة قصيرة… اضحك قبل ما الإنترنت يقطع.",
        "لو التفكير يحرق سعرات كنت صرت رياضي.",
        "أحياناً أفتح الثلاجة فقط لأرى الضوء.",
        "أنا مو كسول… أنا في وضع توفير الطاقة."
    ],
    "motivation": [
        "لا أحد سيصنع مستقبلك غيرك.",
        "كل يوم جديد فرصة جديدة.",
        "ابدأ حتى لو كان الطريق غير واضح.",
        "القوة الحقيقية تبدأ عندما ترفض الاستسلام."
    ],
    "love": [
        "وجودك يجعل العالم أكثر دفئاً.",
        "الحب ليس كلمة بل شعور يغيّر كل شيء.",
        "أنت أجمل صدفة حدثت في حياتي.",
        "قلبي يعرف طريقه إليك دائماً."
    ],
    "poetry": [
        "في عينيك بحرٌ من القصائد.",
        "قلبي يكتبك شعراً كل ليلة.",
        "بين الحروف أجدك دائماً.",
        "القصيدة أنت… والباقي كلمات."
    ],
    "sad": [
        "بعض الحزن لا يقال… فقط يُشعر.",
        "الصمت أحياناً يشرح كل شيء.",
        "ليس كل من يبتسم سعيداً.",
        "الذكريات الثقيلة لا تُرى."
    ],
    "depression": [
        "أصعب المعارك هي التي داخلنا.",
        "التعب الذي لا يُرى هو الأثقل.",
        "أحياناً نحتاج فقط أن نتوقف قليلاً.",
        "الهدوء الطويل قد يخفي ألف فكرة."
    ]
}

# أسماء المجالات بالعربي
categories_ar = {
    "comedy": "😂 كوميدي",
    "motivation": "🔥 تحفيزي",
    "love": "❤️ حب",
    "poetry": "✍️ شعر",
    "sad": "💔 حزن",
    "depression": "🖤 اكتئاب"
}

# أسماء المجالات بالإنجليزي
categories_en = {
    "comedy": "😂 Comedy",
    "motivation": "🔥 Motivation",
    "love": "❤️ Love",
    "poetry": "✍️ Poetry",
    "sad": "💔 Sad",
    "depression": "🖤 Depression"
}


def build_categories(lang):
    if lang == "ar":
        data = categories_ar
    else:
        data = categories_en

    keyboard = []
    for key, value in data.items():
        keyboard.append([InlineKeyboardButton(value, callback_data=f"cat_{key}")])

    return InlineKeyboardMarkup(keyboard)


def build_result_buttons(category):
    keyboard = [
        [InlineKeyboardButton("🔄 نص جديد", callback_data=f"again_{category}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data="back")]
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("العربية 🇸🇦", callback_data="lang_ar"),
            InlineKeyboardButton("English 🇺🇸", callback_data="lang_en")
        ]
    ]

    await update.message.reply_text(
        "اختر اللغة / Choose language",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "lang_ar":
        users[user_id] = {"lang": "ar"}
        text = "اختر المجال"
    else:
        users[user_id] = {"lang": "en"}
        text = "Choose category"

    lang = users[user_id]["lang"]

    await query.edit_message_text(
        text=text,
        reply_markup=build_categories(lang)
    )


async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE, category):
    query = update.callback_query
    user_id = query.from_user.id

    users[user_id]["category"] = category

    message = random.choice(texts[category])

    await query.edit_message_text(
        text=message,
        reply_markup=build_result_buttons(category)
    )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = users[user_id]["lang"]

    if lang == "ar":
        text = "اختر المجال"
    else:
        text = "Choose category"

    await query.edit_message_text(
        text=text,
        reply_markup=build_categories(lang)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("lang"):
        await select_language(update, context)

    elif data.startswith("cat_"):
        category = data.split("_")[1]
        await send_text(update, context, category)

    elif data.startswith("again_"):
        category = data.split("_")[1]
        await send_text(update, context, category)

    elif data == "back":
        await back_to_menu(update, context)


def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()