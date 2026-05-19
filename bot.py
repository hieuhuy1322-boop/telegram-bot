from telethon import TelegramClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import random

# ===== CONFIG =====
api_id = 31013160
api_hash = '16cd203faf218319e61e175d129bfd3816cd203faf218319e61e175d129bfd38'
BOT_TOKEN = "8887759451:AAHj9i0QSyHHw1QeS6ldMa601khfVlCK3Ko"

group = None
send_time = 10
delete_time = 5
running = False

texts = [
    "đúng là quả trứng vô ơn đấy",
    "hôm nay tự nhiên thấy mọi thứ chán thật",
    "đêm nay chắc lại ngủ muộn nữa rồi",
    "nhiều lúc chỉ muốn im lặng cả ngày"
]

client = TelegramClient("session", api_id, api_hash)

# ===== AUTO SEND =====
async def auto_send():
    global running
    while running:
        try:
            text = random.choice(texts)
            msg = await client.send_message(group, text)
            print("Đã gửi:", text)

            await asyncio.sleep(delete_time)
            await client.delete_messages(group, msg.id)

            await asyncio.sleep(send_time)

        except Exception as e:
            print("Lỗi:", e)
            await asyncio.sleep(5)

# ===== BOT COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot sẵn sàng!")

async def setgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global group
    group = context.args[0]
    await update.message.reply_text(f"Đã set nhóm: {group}")

async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global send_time
    send_time = int(context.args[0])
    await update.message.reply_text(f"Delay: {send_time}s")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    running = True
    asyncio.create_task(auto_send())
    await update.message.reply_text("Đã chạy")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    running = False
    await update.message.reply_text("Đã dừng")

# ===== MAIN =====
async def main():
    await client.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setgroup", setgroup))
    app.add_handler(CommandHandler("settime", settime))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("stop", stop))

    print("Bot đang chạy...")

    await app.initialize()
    await app.start()
    await app.bot.initialize()

    # polling thủ công (KHÔNG dùng run_polling)
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(9999)

# ===== RUN =====
if __name__ == "__main__":
    asyncio.run(main())