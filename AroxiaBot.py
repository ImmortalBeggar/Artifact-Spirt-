import os
import sys
import time
import json
import random
import socket
import telebot
import google.generativeai as genai
from groq import Groq
from collections import deque

# ==========================================
# 1. THE RITUAL OF CONFIGURATION
# ==========================================
CONFIG_FILE = "config.json"

def initial_setup():
    print("\n--- 🔮 Aroxia Artifact Spirit: Initial Setup ---")
    config = {}
    config['TELEGRAM_TOKEN'] = input("Enter Telegram Bot Token: ").strip()
    config['SMITH_ID'] = int(input("Enter your Numeric Telegram User ID: ").strip())
    config['MASTER_CORE'] = input("Enter Primary Gemini API Key: ").strip()
    config['GROQ_KEY'] = input("Enter Backup Groq API Key: ").strip()
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print("✅ Configuration sealed in config.json.\n")
    return config

if not os.path.exists(CONFIG_FILE):
    cfg = initial_setup()
else:
    with open(CONFIG_FILE, 'r') as f:
        cfg = json.load(f)

# Apply Config
TELEGRAM_TOKEN = cfg['TELEGRAM_TOKEN']
SMITH_ID = cfg['SMITH_ID']
MASTER_CORE = cfg['MASTER_CORE']
GROQ_KEY = cfg['GROQ_KEY']

bot = telebot.TeleBot(TELEGRAM_TOKEN)
model = genai.GenerativeModel('gemini-2.5-flash')
groq_client = Groq(api_key=GROQ_KEY)

# ==========================================
# 2. SECT TREASURY & TALISMANS
# ==========================================
def load_treasury():
    try:
        with open("sect_treasury.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return [MASTER_CORE] # Default to Master Core if empty

KEY_POOL = load_treasury()

TALISMAN_BANTER = [
    "💤 *The true Archivist is resting. This is a Paper Talisman.*",
    "My spiritual energy is depleted. I am currently functioning on vibes alone.",
    "The heavenly network is currently severed. Meditate on the Dao."
]

# ==========================================
# 3. CORE LOGIC & PRIVILEGE
# ==========================================
def is_privileged_user(message):
    if message.from_user.id == SMITH_ID: return True
    if message.chat.type in ['group', 'supergroup']:
        try:
            admins = bot.get_chat_administrators(message.chat.id)
            return any(admin.user.id == message.from_user.id for admin in admins)
        except: return False
    return False

chat_memory = {}
def get_memory(chat_id):
    if chat_id not in chat_memory: chat_memory[chat_id] = deque(maxlen=15)
    return chat_memory[chat_id]

# ==========================================
# 4. MAIN CHAT HANDLER (TRIPLE-TIER)
# ==========================================
@bot.message_handler(func=lambda message: message.text is not None and not message.text.startswith('/'))
def handle_all_messages(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    user_text = message.text
    
    # Ignore group noise unless mentioned
    if message.chat.type != 'private' and f"@{bot.get_me().username}" not in user_text:
        return

    clean_text = user_text.replace(f"@{bot.get_me().username}", "").strip()
    memory = get_memory(chat_id)
    memory.append(f"{user_name}: {clean_text}")
    
    history_transcript = "\n".join(memory)
    mega_prompt = f"You are Aroxia, an Artifact Spirit. History:\n{history_transcript}\nRespond to {user_name}:"

    try:
        bot.send_chat_action(chat_id, 'typing')
        privileged = is_privileged_user(message)
        
        # TIER 1: GEMINI
        genai.configure(api_key=MASTER_CORE if privileged else random.choice(KEY_POOL))
        response = model.generate_content(mega_prompt, request_options={"timeout": 60})
        final_reply = response.text + f"\n\n---\n🔮 **Core:** `[████████░░]`\n*Source: Gemini*"

    except Exception as e:
        # TIER 2: GROQ FAILOVER
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": mega_prompt}],
                model="llama3-8b-8192"
            )
            final_reply = chat_completion.choices[0].message.content + f"\n\n---\n🔮 **Core:** `[████░░░░░░]`\n*Source: Groq Backup*"
        except:
            final_reply = random.choice(TALISMAN_BANTER)

    memory.append(f"Aroxia: {final_reply}")
    bot.reply_to(message, final_reply, parse_mode="Markdown")

# ==========================================
# 5. EXECUTION
# ==========================================
if __name__ == "__main__":
    print("🛡️ Aroxia Public Clone is Active.")
    bot.polling(non_stop=True)
