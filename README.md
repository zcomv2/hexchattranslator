# hexchattranslator
HexChat Translator is a Python script that translates in real-time the messages you write in HexChat into English and Japanese using Google Translate.

📢 Features:

Automatically translates any message sent with /say.

Supports translation from Spanish to English and Japanese.

No additional package installation required.

Works quickly and smoothly within HexChat.


🛠 Installation

1️⃣ Download the script

Copy the translator.py file into your HexChat scripts directory.

If you don't have a scripts directory, you can create one and copy the file there. For example:

mkdir -p ~/.config/hexchat/addons
cd ~/.config/hexchat/addons
wget https://github.com/your_username/HexChat-Translator/raw/main/translator.py


2️⃣ Load the script in HexChat

Open HexChat and run this command:

/py load ~/.config/hexchat/addons/translator.py

If everything is fine, you will see this message in the console:

HexChat Translator v15.1 loaded successfully. Using Google Translate.
🔥 DEBUG: Script started without errors. Ready to translate.

3️⃣ Basic usage

To translate a message, use /say before the text:

/say hello final test

Result in the chat:

[ES] hello final test
[EN] Hello final test
[JA] こんにちは最終テスト

4️⃣ To reload or update the script

If you need to reload the script after modifying it:

/py unload translator.py
/py load ~/.config/hexchat/addons/translator.py

5️⃣ To load the script automatically on HexChat startup (Optional)

If you want the script to load automatically when HexChat starts, copy the file to the startup folder:

cp ~/.config/hexchat/addons/translator.py ~/.config/hexchat/addons/

🛠 Troubleshooting

🔥 1️⃣ The script does not load

Ensure that HexChat has Python 3 support.

Verify that the translator.py file is in the correct path.

Run /py list to see the loaded scripts.

🛠 2️⃣ The script loads but does not translate

Make sure to use /say before the message.

Check your Internet connection, as it uses Google Translate.

Try reloading the script with:

/py unload translator.py

/py load ~/.config/hexchat/addons/translator.py

⚠ 3️⃣ Error: "[Error in connection]"

Google Translate may be temporarily blocking your IP.

Wait a few minutes and try again.

Try using a VPN if the problem persists.

[ CodeName: #Doraemon ]
