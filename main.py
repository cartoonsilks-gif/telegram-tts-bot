import os
import asyncio
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import edge_tts

TOKEN = os.environ.get("BOT_TOKEN")

# Emotional & Deep Male Voice
VOICE = "hi-IN-MadhurNeural"

def polish_text_for_human_feel(raw_text: str) -> str:
    """
    Cleans, fixes formatting, and formats punctuation so AI TTS reads
    it with human-like rhythm, emotion, and proper emotional pauses.
    """
    text = raw_text.strip()
    
    # Clean bracket tags if user writes [pause]
    text = re.sub(r'\[pause.*?\]', '...', text, flags=re.IGNORECASE)
    
    # Normalize multiple dots/commas to create natural emotional breath-breaks
    text = re.sub(r'\.{2,}', '... ', text)
    text = re.sub(r',+', ', ', text)
    
    # Ensure spaces after punctuation for smooth pronunciation
    text = re.sub(r'([।!?,])([^\s])', r'\1 \2', text)
    
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! Mujhe koi bhi Hindi text ya shayari script bhejo.\n\n"
        "Main use bilkul deep, human-like emotional male voice-over mein convert kar dunga!"
    )

async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text
    status_msg = await update.message.reply_text("🎙️ Generating emotional human-like voice-over...")
    
    # Polish text for natural human rhythm
    polished_script = polish_text_for_human_feel(raw_text)
    
    output_file = f"voice_{update.message.message_id}.mp3"
    
    try:
        # Rate = -12% (Slow & emotional feel like video)
        # Pitch = -5Hz (Deeper, warmer tone)
        communicate = edge_tts.Communicate(
            text=polished_script,
            voice=VOICE,
            rate="-12%",
            pitch="-5Hz"
        )
        
        await communicate.save(output_file)
        
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
    
