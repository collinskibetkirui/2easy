import os
from dotenv import load_dotenv
import random
import string

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8849937805:AAG3tDyqxeH7PIquW3n2p2LN_NA7SVgiGzk")
VIP_CHANNEL_ID = int(os.getenv("VIP_CHANNEL_ID", "-1001234567890"))
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "Twoeasysupport")

SHOP_CATEGORIES = {
    "bank_logs": {"name": "🏦 Bank Logs (Demo)", "emoji": "🏦"},
    "coinbase": {"name": "💰 Coinbase (Demo)", "emoji": "💰"},
    "cashapp": {"name": "💵 CashApp (Demo)", "emoji": "💵"},
    "paypal": {"name": "💳 PayPal (Demo)", "emoji": "💳"},
    "fullz": {"name": "📋 Fullz (Demo)", "emoji": "📋"},
    "cc": {"name": "💳 Credit Cards (Demo)", "emoji": "💳"},
    "non_vbv": {"name": "🔓 Non-VBV Cards (Demo)", "emoji": "🔓"},
    "dumps": {"name": "💾 Dumps (Demo)", "emoji": "💾"},
    "shopwithscrip": {"name": "🛍️ Gift Cards (Demo)", "emoji": "🛍️"},
}

PAYMENT_METHODS = {
    "btc": {"name": "Bitcoin (BTC)", "symbol": "₿"},
    "usdt": {"name": "USDT (TRC20)", "symbol": "💲"},
    "ltc": {"name": "LiteCoin (LTC)", "symbol": "Ł"},
    "doge": {"name": "Dogecoin (DOGE)", "symbol": "Ð"},
}

WALLET_ADDRESSES = {
    "btc": "3KXxcezpun9AJbNSg88PmD1HTH5s7inRXx",
    "usdt": "TWpr3drUQPBCLpHsbmHHsFwPwqM4X1PZEY",
    "ltc": "MPyWXR8WGNZS9gx4D1WFqoUtF4KSGczJMv",
    "doge": "DDxz1EUymydsBs2VC5ipNVNUSFkAS8DpEE",
}

# ---- Country‑specific bank lists ----
BANK_LISTS = {
    "USA": [
        "Chase Bank", "Bank of America", "Wells Fargo", "Citibank", "US Bank",
        "Goldman Sachs", "Morgan Stanley", "PNC Bank", "TD Bank USA", "Capital One",
        "Fifth Third Bank", "KeyBank", "Huntington Bank", "Regions Bank", "M&T Bank",
        "Truist Bank", "First Citizens Bank", "Ally Bank", "Synchrony Bank", "Discover Bank",
        "Barclays US", "HSBC US", "Santander US", "BMO Harris", "State Street",
        "Northern Trust", "BBVA USA", "Comerica Bank", "Zions Bank", "CIT Bank"
    ],
    "UK": [
        "HSBC UK", "Barclays", "Lloyds Bank", "NatWest", "Santander UK",
        "Monzo", "Revolut", "Starling Bank", "Metro Bank", "Coutts",
        "Nationwide", "TSB Bank", "Co-operative Bank", "Virgin Money", "Clydesdale Bank"
    ],
    "Canada": [
        "TD Canada Trust", "RBC Royal Bank", "Scotiabank", "BMO Bank of Montreal",
        "CIBC", "National Bank of Canada", "Tangerine", "EQ Bank",
        "Simplii Financial", "Manulife Bank", "Canadian Western Bank", "Laurentian Bank"
    ],
    "Australia": [
        "Commonwealth Bank", "Westpac", "ANZ Bank", "NAB", "Macquarie Bank",
        "Bendigo Bank", "Bank of Queensland", "Suncorp Bank",
        "AMP Bank", "Greater Bank", "MyState Bank", "ME Bank"
    ]
}

def random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "icloud.com"]
    return f"demo_{''.join(random.choices(string.ascii_lowercase, k=8))}@{random.choice(domains)}"

def random_card():
    brand = random.choice(["Visa", "Mastercard"])
    prefix = "4" if brand == "Visa" else "5"
    number = prefix + ''.join(random.choices(string.digits, k=15))
    expiry = f"{random.randint(1,12):02d}/{random.randint(25,29)}"
    cvv = ''.join(random.choices(string.digits, k=3))
    return {"brand": brand, "number": number, "expiry": expiry, "cvv": cvv}

def random_cookies():
    return f"session_id={''.join(random.choices(string.ascii_letters + string.digits, k=24))}; _ga={''.join(random.choices(string.ascii_letters + string.digits, k=16))}; _gid={''.join(random.choices(string.ascii_letters + string.digits, k=16))}"

def random_address(country):
    if country == "USA":
        return f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} St, {random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])}, {random.choice(['NY', 'CA', 'IL', 'TX', 'AZ'])} {random.randint(10000, 99999)}"
    elif country == "UK":
        return f"{random.randint(1, 999)} {random.choice(['High', 'Station', 'Church', 'Park', 'Victoria'])} Rd, {random.choice(['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'])}, {random.choice(['SW1A', 'M1', 'B1', 'LS1', 'G1'])} {random.randint(1, 9)}{random.choice(['AA', 'AB', 'BA', 'BB'])}"
    elif country == "Canada":
        return f"{random.randint(100, 9999)} {random.choice(['Main', 'King', 'Queen', 'Bay', 'Bloor'])} St, {random.choice(['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'])}, {random.choice(['ON', 'BC', 'QC', 'AB', 'ON'])} {random.choice(['M5V', 'V6Z', 'H3Z', 'T2P', 'K1P'])} {random.randint(1, 9)}{random.choice(['A', 'B', 'C', 'D'])}"
    else:
        return f"{random.randint(1, 999)} {random.choice(['George', 'Elizabeth', 'William', 'King', 'Queen'])} St, {random.choice(['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'])}, {random.choice(['NSW', 'VIC', 'QLD', 'WA', 'SA'])} {random.randint(1000, 9999)}"

# ---- Generate bank logs with extended fields ----
def generate_bank_logs(count=100):
    items = []
    for _ in range(count):
        country = random.choice(list(BANK_LISTS.keys()))
        bank = random.choice(BANK_LISTS[country])
        balance = random.randint(2200, 87000)
        price = random.randint(50, 2300)
        items.append({
            "bank": bank,
            "country": country,
            "balance": f"${balance:,}",
            "price": price,
            "email": random_email(),
            "password": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            "routing_number": ''.join(random.choices(string.digits, k=9)),
            "account_number": ''.join(random.choices(string.digits, k=10)),
            "full_name": f"{random.choice(['John','Mary','Robert','Jennifer','David','Linda','James','Patricia','Michael','Barbara'])} {random.choice(['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez'])}",
            "address": random_address(country),
            "cookies": random_cookies(),
            "card_brand": random.choice(["Visa", "Mastercard"]),
            "card_number": ''.join(random.choices(string.digits, k=16)),
            "card_expiry": f"{random.randint(1,12):02d}/{random.randint(25,29)}",
            "card_cvv": ''.join(random.choices(string.digits, k=3))
        })
    return items

# ---- Other categories (no country) ----
def generate_items(category, count=100, balance_min=2200, balance_max=87000, price_min=50, price_max=2300):
    items = []
    for _ in range(count):
        balance = random.randint(balance_min, balance_max)
        price = random.randint(price_min, price_max)
        item = {"balance": f"${balance:,}", "price": price}
        if category == "paypal":
            item["type"] = random.choice(["Business", "Verified Personal", "Premier"])
        elif category in ("cc", "non_vbv"):
            item["brand"] = random.choice(["Visa", "Mastercard", "Amex", "Discover"])
        elif category == "dumps":
            item["brand"] = random.choice(["Visa", "Mastercard", "Amex"])
            item["type"] = random.choice(["Classic", "Gold", "Platinum", "World", "Elite"])
        elif category == "shopwithscrip":
            platforms = ["Amazon", "Walmart", "Target", "Best Buy", "Starbucks", "Uber", "DoorDash", "Netflix", "Spotify", "Google Play", "Apple Store", "Sephora", "Nike", "Adidas", "Steam", "PlayStation", "Xbox", "eBay", "Etsy", "Wayfair", "Chewy", "Lowes", "Home Depot", "Macy's", "Kohl's"]
            item["platform"] = random.choice(platforms)
        elif category == "fullz":
            item["type"] = "Complete Profile"
        items.append(item)
    return items

DEMO_ITEMS = {
    "bank_logs": generate_bank_logs(100),
    "coinbase": generate_items("coinbase", 100),
    "cashapp": generate_items("cashapp", 100),
    "paypal": generate_items("paypal", 100),
    "fullz": generate_items("fullz", 100),
    "cc": generate_items("cc", 100),
    "non_vbv": generate_items("non_vbv", 100),
    "dumps": generate_items("dumps", 100),
    "shopwithscrip": generate_items("shopwithscrip", 100, balance_min=10, balance_max=500, price_min=5, price_max=100),
}

def format_item_message(category, item):
    cat_name = SHOP_CATEGORIES.get(category, {}).get("name", category)
    message = f"""
🎉 *DEMO {cat_name.upper()} DELIVERED!*

📌 *Type:* {cat_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    if category == "bank_logs":
        message += f"""
🏦 *Bank:* {item.get('bank', 'N/A')}
🌍 *Country:* {item.get('country', 'N/A')}
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 *Email Access:*
   • Email: `{item.get('email', 'N/A')}`
   • Password: `{item.get('password', 'N/A')}`

🏦 *Account Details:*
   • Routing Number: `{item.get('routing_number', 'N/A')}`
   • Account Number: `{item.get('account_number', 'N/A')}`
   • Full Name: {item.get('full_name', 'N/A')}
   • Address: {item.get('address', 'N/A')}

🍪 *Cookies:*
`{item.get('cookies', 'N/A')}`

💳 *Debit Card:*
   • Brand: {item.get('card_brand', 'N/A')}
   • Number: `{item.get('card_number', 'N/A')}`
   • Expiry: {item.get('card_expiry', 'N/A')}
   • CVV: `{item.get('card_cvv', 'N/A')}`
"""
    elif category == "coinbase":
        message += f"""
💰 *Balance:* {item.get('balance', 'N/A')}
📌 *Type:* Coinbase Account
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "cashapp":
        message += f"""
💰 *Balance:* {item.get('balance', 'N/A')}
📌 *Type:* CashApp Account
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "paypal":
        message += f"""
💰 *Balance:* {item.get('balance', 'N/A')}
📌 *Type:* {item.get('type', 'PayPal Account')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "fullz":
        message += f"""
📋 *Fullz Profile*
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "cc":
        message += f"""
💳 *Card:* {item.get('brand', 'N/A')}
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "non_vbv":
        message += f"""
🔓 *Non-VBV Card:* {item.get('brand', 'N/A')}
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "dumps":
        message += f"""
💾 *Dumps:* {item.get('brand', 'N/A')} - {item.get('type', 'N/A')}
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "shopwithscrip":
        message += f"""
🛍️ *Platform:* {item.get('platform', 'N/A')}
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    message += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ *IMPORTANT:* This is DEMO content for educational purposes only.
🔒 Do not use for any illegal activity.
📞 Support: @{SUPPORT_USERNAME}
"""
    return message