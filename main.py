import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import edge_tts

# Bot Token
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Mujhe koi bhi text bhejo, main use realistic AI voice mein convert kar dunga.")

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    status_msg = await update.message.reply_text("Voice generate ho rahi hai, kripya wait karein...")
    
    output_file = "voice.mp3"
    
    # High-quality voice selection (Hindi / English blend)
    communicate = edge_tts.Communicate(text, "hi-IN-SwaraNeural")
    await communicate.save(output_file)
    
    # Send Voice Note
    with open(output_file, 'rb') as audio:
        await update.message.reply_voice(voice=audio)
        
    await status_msg.delete()
    if os.path.exists(output_file):
        os.remove(output_file)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
  
