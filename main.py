import os
import asyncio
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import edge_tts

# Bot Token from Environment Variable
TOKEN = os.environ.get("BOT_TOKEN")

# Male Voice Setup (Madhur = Hindi Male)
VOICE = "hi-IN-MadhurNeural"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! Mujhe koi bhi text ya script bhejo, main use Male Voice mein convert kar dunga.")

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    status_msg = await update.message.reply_text("🎙️ Generating Male Voice-over...")
    
    # Process custom tags for emotions/pauses
    # Replace [pause] or [pause=2s] with SSML break tag
    processed_text = re.sub(r'\[pause\]', '<break time="1s"/>', text, flags=re.IGNORECASE)
    processed_text = re.sub(r'\[pause=(\d+)s\]', r'<break time="\1s"/>', processed_text, flags=re.IGNORECASE)
    
    output_file = f"voice_{update.message.message_id}.mp3"
    
    try:
        # Check if text contains SSML tags
        if "<break" in processed_text:
            ssml_text = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='hi-IN'>{processed_text}</speak>"
            communicate = edge_tts.Communicate(ssml_text, VOICE)
        else:
            communicate = edge_tts.Communicate(text, VOICE)
            
        await communicate.save(output_file)
        
        # Send voice message
        with open(output_file, 'rb') as audio:
            await update.message.reply_voice(voice=audio)
            
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"Error generating voice: {str(e)}")
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_speech))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
