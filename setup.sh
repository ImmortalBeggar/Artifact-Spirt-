#!/data/data/com.termux/files/usr/bin/bash

echo "🔮 Initializing Aroxia Artifact Spirit: Public Installation..."

# 1. Update the Environment
pkg update && pkg upgrade -y

# 2. Install Build Dependencies (The Troubleshooting Shield)
echo "🛡️ Strengthening the Spiritual Veins (Dependencies)..."
pkg install python git libxml2 libxslt -y

# 3. Handle the 'grpcio' Demon for Termux
# This installs the pre-compiled version so the phone doesn't crash during build
pkg install tur-repo -y
pkg install python-grpcio -y

# 4. Install the Main Libraries
echo "📜 Fetching the AI Scripts..."
pip install pyTelegramBotAPI google-generativeai groq

echo "✅ Ritual Complete. Run 'python AroxiaBot.py' to ignite the spirit."
