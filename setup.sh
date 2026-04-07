#!/data/data/com.termux/files/usr/bin/bash

echo "🔮 Initializing Aroxia Installation Ritual..."

# Update packages
pkg update && pkg upgrade -y

# Install Python and essential tools
pkg install python git -y

# Install Aroxia's Spiritual Veins (Libraries)
pip install pyTelegramBotAPI google-generativeai groq

echo "✅ Spiritual environment prepared. Now run 'python AroxiaBot.py' to begin the setup."
