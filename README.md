# Social Media MP3 Downloader — Telegram Bot

Link එකක් send කලාම (YouTube, Instagram, TikTok, Facebook, Twitter/X, SoundCloud වගේ sites) MP3 එකක් හැදලා ආපහු send කරන Telegram bot එකක්.

## 1. Bot Token එක ගන්නා විදිය

1. Telegram එකේ **@BotFather** එකට message කරන්න
2. `/newbot` type කරලා instructions follow කරන්න
3. එයා දෙන **token** එක save කරගන්න (මේ වගේ පේනවා: `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

## 2. ffmpeg install කරගන්න (mp3 convert කරන්න මේක ඕන)

**Windows:** https://ffmpeg.org/download.html වලින් download කරලා PATH එකට add කරන්න
**Mac:** `brew install ffmpeg`
**Linux (Ubuntu/Debian):** `sudo apt install ffmpeg`

## 3. Python packages install කරගන්න

```bash
pip install -r requirements.txt
```

## 4. Token එක set කරන්න

**Mac/Linux:**
```bash
export BOT_TOKEN="ඔයාගේ-token-එක-මෙතන-දාන්න"
```

**Windows (PowerShell):**
```powershell
$env:BOT_TOKEN="ඔයාගේ-token-එක-මෙතන-දාන්න"
```

## 5. Bot එක run කරන්න

```bash
python bot.py
```

Bot එක run වෙනකොට terminal එකේ "Bot starting..." කියලා පේනවා. දැන් Telegram එකේ ඔයාගේ bot එකට ගිහින් `/start` කරලා, ඕනම link එකක් paste කරන්න!

## දැනගන්න වටින දේවල්

- **File size limit**: Telegram bot API එකෙන් 50MB ට වඩා වැඩි files send කරන්න බෑ. ලොකු videos වල audio ලොකු වෙන්න පුළුවන්.
- **Private/removed content**: Private accounts, age-restricted, ან delete කරපු content download කරන්න බෑ.
- **Legal**: ඔයාගේම content, download කරන්න permission තියෙන content, හෝ personal use සඳහා විතරක් පාවිච්චි කරන්න. Copyright තියෙන content redistribute කරන එක බොහෝ platform වල terms of service වලට පටහැනියි.
- **Deploy කරන්න**: 24/7 run කරගන්න ඕන නම් Railway, Render, VPS (DigitalOcean/AWS) වගේ තැනක deploy කරන්න පුළුවන්. Local computer එකේ run කරනකොට, computer එක off වුනාම bot එකත් off වෙනවා.
