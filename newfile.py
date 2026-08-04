
# Fill these values
TOKEN="8803295868:AAHtZCSFJIFnKqeyMDGWYCuCOxKS7lcynH0"
CHANNEL="@NetBazProxy"
LINK="https://gomusic.upera.tv/embed/3082207?ref=1T"
ADMIN_ID=8219393716

import json, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

USERS_FILE="users.json"
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE,"r") as f: return json.load(f)
    return []
def save_users(u):
    with open(USERS_FILE,"w") as f: json.dump(u,f)

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    users=load_users()
    uid=update.effective_user.id
    if uid not in users:
        users.append(uid); save_users(users)
    kb=[[InlineKeyboardButton("📢 عضویت در کانال",url=f"https://t.me/{CHANNEL.replace('@','')}")],
        [InlineKeyboardButton("✅ بررسی عضویت",callback_data="check")]]
    await update.message.reply_text("ابتدا عضو کانال شوید سپس بررسی عضویت را بزنید.",reply_markup=InlineKeyboardMarkup(kb))

async def check(update:Update, context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()
    m=await context.bot.get_chat_member(CHANNEL,q.from_user.id)
    if m.status in ["member","administrator","creator"]:
        await q.message.delete()
        await context.bot.send_message(q.message.chat_id,f"✅ تایید شد\n\n{LINK}")
    else:
        await q.answer("ابتدا عضو کانال شوید.",show_alert=True)

async def stats(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id!=ADMIN_ID: return
    await update.message.reply_text(f"👥 تعداد کاربران: {len(load_users())}")

app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("stats",stats))
app.add_handler(CallbackQueryHandler(check))
print("Bot is running...")
app.run_polling()
