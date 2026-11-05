import os, re, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from sqlalchemy import select
from .db import SessionLocal
from .models import Merchant, Product, Order

log = logging.getLogger(__name__)
application = None

def slugify(value):
    value = re.sub(r'[^a-zA-Z0-9]+', '-', value.strip().lower()).strip('-')
    return (value or "dukaan")[:100]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍️ Alaabaha suuqa", callback_data="market")],
        [InlineKeyboardButton("🏪 Iska diiwaangeli dukaan", callback_data="register")],
        [InlineKeyboardButton("ℹ️ Sida uu u shaqeeyo", callback_data="help")],
    ]
    await update.message.reply_text(
        "Ku soo dhawoow SL Market!\nSuuq ay ganacsatada Somaliland iyo Soomaaliya ku soo bandhigaan alaabtooda.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "help":
        await q.edit_message_text("Ganacsade: iska diiwaangeli dukaankaaga. Macmiil: ka dhex raadi alaabaha suuqa.")
    elif q.data == "register":
        context.user_data["registering"] = True
        await q.edit_message_text("Fadlan soo qor magaca dukaankaaga. Tusaale: Hargeisa Fashion")
    elif q.data == "market":
        with SessionLocal() as db:
            items = db.scalars(select(Product).where(Product.available == True).order_by(Product.created_at.desc()).limit(15)).all()
            if not items:
                await q.edit_message_text("Weli alaab lama soo gelin. Ganacsade noqo oo dukaankaaga diiwaangeli.")
                return
            text = "🛍️ Alaabaha suuqa:\n\n" + "\n".join([f"#{p.id} · {p.title} — {p.price} {p.currency}" for p in items])
            await q.edit_message_text(text)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("registering"):
        await update.message.reply_text("Isticmaal /start si aad u aragto adeegyada SL Market.")
        return
    name = update.message.text.strip()[:120]
    if len(name) < 2:
        await update.message.reply_text("Magaca dukaanku aad buu u gaaban yahay. Mar kale qor.")
        return
    tg_id = update.effective_user.id
    with SessionLocal() as db:
        existing = db.scalar(select(Merchant).where(Merchant.telegram_id == tg_id))
        if existing:
            existing.name = name
            await update.message.reply_text(f"Magaca dukaankaaga waa la cusboonaysiiyey: {name}")
        else:
            slug = f"{slugify(name)}-{tg_id}"
            merchant = Merchant(telegram_id=tg_id, name=name, shop_slug=slug)
            db.add(merchant)
            await update.message.reply_text(f"Waad ku mahadsan tahay! Dukaanka '{name}' waa la diiwaangeliyey. Qaybta alaab-gelinta ayaa lagu darayaa tallaabada xigta.")
        db.commit()
    context.user_data["registering"] = False

async def start_bot():
    global application
    token = os.getenv("BOT_TOKEN")
    if not token:
        log.warning("BOT_TOKEN missing: Telegram bot was not started.")
        return
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(buttons))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    log.info("SL Market Telegram bot started.")
