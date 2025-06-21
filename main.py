import discord
import re
import requests
from config import DISCORD_TOKEN, CHANNEL_IDS, NTFY_TOPIC
from datetime import datetime
from notify_items import default_priority_items, high_priority_items

color_map = {
    "Carrot": "\033[92m", "Strawberry": "\033[92m", "Blueberry": "\033[92m", "Orange": "\033[92m",
    "Tomato": "\033[92m", "Corn": "\033[92m", "Daffodil": "\033[92m",
    "Watermelon": "\033[93m", "Pumpkin": "\033[93m", "Apple": "\033[93m", "Bamboo": "\033[93m",
    "Coconut": "\033[33m", "Cactus": "\033[33m", "Dragon": "\033[33m", "Mango": "\033[33m",
    "Grape": "\033[95m", "Mushroom": "\033[95m", "Pepper": "\033[95m", "Cacao": "\033[95m",
    "Beanstalk": "\033[96m",
    "Watering": "\033[92m", "Trowel": "\033[92m", "Recall": "\033[92m",
    "Basic": "\033[93m",
    "Advanced": "\033[95m",
    "Lightning": "\033[33m", "Godly": "\033[33m",
    "Harvest": "\033[35m", "Master": "\033[35m", "Favorite": "\033[35m",
    "Common Egg": "\033[92m", "Uncommon Egg": "\033[92m",
    "Legendary Egg": "\033[95m", "Bug Egg": "\033[91m", "Mythical Egg": "\033[33m",
    "Flower Seed Pack": "\033[92m",
    "Nectarine Seed": "\033[33m",
    "Hive Fruit Seed": "\033[93m",
    "Honey Sprinkler": "\033[33m",
    "Bee Egg": "\033[33m",
    "Bee Crate": "\033[95m",
    "Brick Stack": "\033[92m",
    "Compost Bin": "\033[92m",
    "Log": "\033[92m",
    "Wood Pile": "\033[92m",
    "Torch": "\033[92m",
    "Circle Tile": "\033[92m",
    "Path Tile": "\033[92m",
    "Rock Pile": "\033[92m",
    "Pottery": "\033[92m",
    "Rake": "\033[92m",
    "Umbrella": "\033[92m",
    "Log Bench": "\033[94m",
    "Brown Bench": "\033[94m",
    "White Bench": "\033[94m",
    "Hay Bale": "\033[94m",
    "Stone Pad": "\033[94m",
    "Stone Table": "\033[94m",
    "Wood Fence": "\033[94m",
    "Wood Flooring": "\033[94m",
    "Mini TV": "\033[94m",
    "Viney Beam": "\033[94m",
    "Light On Ground": "\033[94m",
    "Water Trough": "\033[94m",
    "Shovel Grave": "\033[94m",
    "Stone Lantern": "\033[94m",
    "Bookshelf": "\033[94m",
    "Axe Stump": "\033[94m",
    "Stone Pillar": "\033[95m",
    "Wood Table": "\033[95m",
    "Canopy": "\033[95m",
    "Campfire": "\033[95m",
    "Cooking Pot": "\033[95m",
    "Clothesline": "\033[95m",
    "Wood Arbour": "\033[93m",
    "Metal Arbour": "\033[93m",
    "Bird Bath": "\033[95m",
    "Lamp Post": "\033[95m",
    "Wind Chime": "\033[95m",
    "Well": "\033[93m",
    "Ring Walkway": "\033[93m",
    "Tractor": "\033[93m",
    "Honey Comb": "\033[33m",
    "Honey Torch": "\033[33m",
    "Bee Chair": "\033[33m",
    "Honey Walkway": "\033[33m",
    "Gnome Crate": "\033[33m",
    "Sign Crate": "\033[33m",
    "Bloodmoon Crate": "\033[33m",
    "Twilight Crate": "\033[33m",
    "Mysterious Crate": "\033[33m",
    "Fun Crate": "\033[33m",
    "Monster Mash Trophy": "\033[91m"
}

RESET_COLOR = "\033[0m"

previous_stock = set()
current_stock = set()
items_to_notify = []

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

client = discord.Client(intents=intents)

def extract_items(text):
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = re.sub(r"<:[^:]+:\d+>", "", line)
        line = re.sub(r"[*_~`]", "", line)
        line = line.strip()
        if " x" in line.lower():
            cleaned.append(line)
    return cleaned

def colorize_text(text, color_code):
    return f"{color_code}{text}{RESET_COLOR}"

def send_ntfy_notification(title, message, priority="default"):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    headers = {
        "Title": title,
        "Priority": "5" if priority == "high" else "3"
    }
    try:
        requests.post(url, data=message.encode('utf-8'), headers=headers)
    except Exception as e:
        print(f"Failed to send notification: {e}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user} ({client.user.id})")

combined_items = default_priority_items + high_priority_items

def replace_discord_timestamps(text):
    matches = re.findall(r"<t:(\d+):R>", text)
    for ts in matches:
        try:
            dt = datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")
            text = text.replace(f"<t:{ts}:R>", f"({dt})")
        except:
            continue
    return text

@client.event
async def on_message(message):
    global current_stock, previous_stock, items_to_notify

    if message.channel.id not in CHANNEL_IDS:
        return

    channel_name = CHANNEL_IDS[message.channel.id]
    any_stock_found = False

    # Clear before processing the whole message
    current_stock.clear()
    items_to_notify.clear()

    for embed in message.embeds:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if channel_name == "Weather":
            weather_title = replace_discord_timestamps(re.sub(r"[*_~`]", "", embed.title or 'Weather Update'))
            weather_desc = replace_discord_timestamps(embed.description or '')
            print(f"\n╭── Weather Alert ──╮")
            if weather_title:
                print(f"│ {weather_title}")
            if weather_desc:
                for line in weather_desc.splitlines():
                    print(f"│ {line.strip()}")
            print("╰────────────────────╯")  # Removed invalid dynamic line length
            weather_msg = f"{weather_title}\n{weather_desc}"
            send_ntfy_notification("Weather Alert", weather_msg.strip())
            continue

        for field in embed.fields:
            stock_items = extract_items(field.value)
            if not stock_items:
                continue
            any_stock_found = True
            print(f"\n╭── {field.name.strip()} ──╮| {timestamp}")
            for item_text in stock_items:
                current_stock.add(item_text)

                for notify_item in combined_items:
                    if notify_item.lower() in item_text.lower() and item_text not in previous_stock:
                        items_to_notify.append(item_text)

                item_color = None
                for item_name, color in color_map.items():
                    if item_name.lower() in item_text.lower():
                        item_color = color
                        break

                if item_color:
                    print(colorize_text(f"│ • {item_text}", item_color))
                else:
                    print(f"│ • {item_text}")
            print("╰" + "─" * (len(field.name.strip()) + 6) + "╯")

    if any_stock_found and items_to_notify:
        for item in items_to_notify:
            priority = "high" if any(h.lower() in item.lower() for h in high_priority_items) else "default"
            send_ntfy_notification("Grow A Garden: New Stock", f"{item} is now on stock!", priority=priority)

    previous_stock = current_stock.copy()

client.run(DISCORD_TOKEN)