# Grow A Garden Discord Bot (ntfy.sh based notifications)

This is a Python-based Discord bot designed to monitor stock updates from specific Grow A Garden Discord channels and send real-time notifications via [ntfy.sh](https://ntfy.sh).

---

## UPDATES: 
- v1.1.0 (June 17, 2025)
- v1.1.1 (June 21, 2025)
  
---

### 🆕 What's New in v1.1.1

✅ Priority Items Separated:
Moved ```default_priority_items``` and ```high_priority_items``` to a new file: ```notify_items.py```
→ Makes priority list management cleaner and more maintainable.

🔁 Updated Priority Lists:
Replaced old items with updated stock alert items:

Default Priority: Now includes Prickly Pear, Bell Pepper, Kiwi, etc.
High Priority: Now includes Tanning Mirror, Paradise Egg, Feijoa, etc.

✨ Minor Code Cleanup:
Imported priority items instead of hardcoding them inside the main script.

---

## 📦 Features

- ✅ Tracks specific channels (e.g., stock, egg, honey, weather).
- ✅ Identifies priority items and sends notifications.
- ✅ Colored console output for easy visual tracking.
- ✅ Lightweight, no database required.
- ✅ Uses [ntfy.sh](https://ntfy.sh) for push notifications.
- ✅ Support for Discord timestamp formatting (<t:...:R>) conversion.
- ✅ Time logs for stock events.

---

## 🛠 Requirements

- Python 3.8+
- Required packages:

```pip install discord.py requests```

---

## ⚙️ Setup Instructions

1. Clone the Repository

```
$ git clone https://github.com/yourusername/grow-a-garden-bot.git
$ cd grow-a-garden-bot
```

2. Install Dependencies

```$ pip install discord.py requests```

3. Configure the Bot

Edit the config.py file:

```
DISCORD_TOKEN = "your_discord_bot_token"

CHANNEL_IDS = {
    channelid1: "Stock",
    channelid2: "Weather",
    channelid3: "Egg Stock",
    channelid4: "Honey Stock"
}

NTFY_TOPIC = "your-ntfy-topic-name"
```

##### Replace "your_discord_bot_token" with your bot's token.

##### Replace channel IDs.

##### Replace your-ntfy-topic-name with your topic on ntfy.sh.

> Optional: You can use .env instead of config.py for security.

---

## 🚀 Run the Bot

```python main.py```

---

## 🔔 How Notifications Work

Items in default_priority_items or high_priority_items will trigger a notification.

Notifications are sent to your ntfy.sh topic.

High-priority items will use a higher notification level.

---

## Images (from v1.0.0)

ntfy.sh app (image 1)
![](https://i.ibb.co/Ngsb6PkK/Screenshot-20250603-180545-ntfy.jpg)

phone notifications (image 2)
![](https://i.ibb.co/wNFcRwZT/Screenshot-20250604-155333-One-UI-Home.jpg)

running main.py (image 3)
![](https://i.ibb.co/pBryXsPT/20250612-175531.jpg)

output from main.py (image 4)
![](https://i.ibb.co/7tXYjBrF/Screenshot-20250612-174444-Termux.jpg)


---

## 🤝 Credits

Built by Jim

[For Grow A Garden stock monitoring and alerting.]

[If you want GaG notifications without doing all this, use 'gag2-jim' as the topic name.]
