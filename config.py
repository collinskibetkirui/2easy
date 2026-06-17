import os
from dotenv import load_dotenv
import random
import string
from datetime import datetime, timedelta

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

# ---- Helper functions ----
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

def random_ssn():
    return ''.join(random.choices(string.digits, k=9))

def random_dob():
    start = datetime(1950, 1, 1)
    end = datetime(2005, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def random_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def random_education():
    schools = ["High School Diploma", "Some College", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "PhD"]
    majors = ["Business Administration", "Computer Science", "Engineering", "Nursing", "Psychology", "Economics", "Biology", "Mathematics"]
    return f"{random.choice(schools)} in {random.choice(majors)}"

# ---- Generate bank logs with realistic pricing ----
def generate_bank_logs(count=100):
    items = []
    for _ in range(count):
        country = random.choice(list(BANK_LISTS.keys()))
        bank = random.choice(BANK_LISTS[country])
        balance = random.randint(800, 25000)
        price_percent = random.uniform(0.04, 0.15)
        price = round(balance * price_percent / 5) * 5
        price = max(50, min(1500, price))
        items.append({
            "bank": bank,
            "country": country,
            "balance": f"${balance:,.2f}",
            "price": int(price),
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

# ---- Generate Fullz with realistic pricing ----
def generate_fullz(count=100):
    items = []
    for _ in range(count):
        ssn = random_ssn()
        dob = random_dob()
        first = random.choice(['John','Mary','Robert','Jennifer','David','Linda','James','Patricia','Michael','Barbara','William','Elizabeth','Thomas','Susan','Charles','Karen','Joseph','Nancy','Christopher','Lisa'])
        last = random.choice(['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez','Hernandez','Lopez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin','Lee'])
        full_name = f"{first} {last}"
        street = f"{random.randint(100, 9999)} {random.choice(['Main','Oak','Pine','Maple','Cedar','Elm','Washington','Jefferson','Lincoln','Madison'])} {random.choice(['St','Ave','Rd','Blvd','Dr','Ln','Ct'])}"
        city = random.choice(['New York','Los Angeles','Chicago','Houston','Phoenix','Philadelphia','San Antonio','San Diego','Dallas','Austin'])
        state = random.choice(['NY','CA','IL','TX','PA','AZ','FL','OH','GA','NC'])
        zip_code = random.randint(10000, 99999)
        address = f"{street}, {city}, {state} {zip_code}"
        email = f"{first.lower()}{last.lower()}{random.randint(10,99)}@outlook.com"
        password = random_password()

        include_education = random.random() < 0.6
        education = random_education() if include_education else None

        # Price: $20 base, +$10 per extra field, education adds $20
        base_price = 20
        extra = 0
        if address: extra += 1
        if email: extra += 1
        if password: extra += 1
        if education: extra += 2
        price = min(120, base_price + extra * 10)
        price = round(price / 5) * 5

        item = {
            "ssn": ssn,
            "dob": dob,
            "full_name": full_name,
            "address": address,
            "email": email,
            "password": password,
            "price": price
        }
        if education:
            item["education"] = education
        items.append(item)
    return items

# ---- Generate Coinbase / CashApp / PayPal with realistic pricing ----
def generate_accounts(category, count=100, balance_min=200, balance_max=10000):
    items = []
    for _ in range(count):
        balance = random.randint(balance_min, balance_max)
        price_percent = random.uniform(0.05, 0.15)
        price = round(balance * price_percent / 5) * 5
        price = max(20, min(500, price))
        item = {"balance": f"${balance:,.2f}", "price": int(price)}
        if category == "paypal":
            item["type"] = random.choice(["Business", "Verified Personal", "Premier"])
        items.append(item)
    return items

# ---- Generate Credit Cards / Non-VBV with realistic pricing ----
def generate_cards(category, count=100):
    items = []
    brands = ["Visa", "Mastercard", "Amex", "Discover"]
    for _ in range(count):
        balance = random.randint(500, 8000)
        price_percent = random.uniform(0.05, 0.15)
        price = round(balance * price_percent / 5) * 5
        price = max(25, min(400, price))
        item = {"brand": random.choice(brands), "balance": f"${balance:,.2f}", "price": int(price)}
        if category == "non_vbv":
            item["non_vbv"] = True
        items.append(item)
    return items

# ---- Generate Dumps with fixed pricing ----
def generate_dumps(count=100):
    types = ["Classic", "Gold", "Platinum", "World", "Elite"]
    prices = {"Classic": 30, "Gold": 60, "Platinum": 90, "World": 120, "Elite": 150}
    brands = ["Visa", "Mastercard", "Amex"]
    items = []
    for _ in range(count):
        dtype = random.choice(types)
        item = {
            "brand": random.choice(brands),
            "type": dtype,
            "price": prices[dtype],
            "balance": f"${random.randint(1000, 8000):,}"  # placeholder balance
        }
        items.append(item)
    return items

# ---- Generate Gift Cards with realistic pricing ----
def generate_giftcards(count=100):
    platforms = ["Amazon", "Walmart", "Target", "Best Buy", "Starbucks", "Uber", "DoorDash", "Netflix", "Spotify", "Google Play", "Apple Store", "Sephora", "Nike", "Adidas", "Steam", "PlayStation", "Xbox", "eBay", "Etsy", "Wayfair", "Chewy", "Lowes", "Home Depot", "Macy's", "Kohl's"]
    items = []
    for _ in range(count):
        balance = random.randint(10, 500)
        discount = random.uniform(0.05, 0.20)  # 5-20% discount
        price = round(balance * (1 - discount) / 5) * 5
        price = max(5, min(475, price))
        items.append({
            "platform": random.choice(platforms),
            "balance": f"${balance:,.2f}",
            "price": int(price)
        })
    return items

DEMO_ITEMS = {
    "bank_logs": generate_bank_logs(100),
    "coinbase": generate_accounts("coinbase", 100),
    "cashapp": generate_accounts("cashapp", 100),
    "paypal": generate_accounts("paypal", 100),
    "fullz": generate_fullz(100),
    "cc": generate_cards("cc", 100),
    "non_vbv": generate_cards("non_vbv", 100),
    "dumps": generate_dumps(100),
    "shopwithscrip": generate_giftcards(100),
}

# ---- Format item message for delivery ----
def format_item_message(category, item):
    cat_name = SHOP_CATEGORIES.get(category, {}).get("name", category)
    message = f"""
🎉 *DEMO {cat_name.upper()} DELIVERED!*

📌 *Type:* {cat_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    if category == "bank_logs":
        features = "✅ Online Access • ✅ Account/Routing Number • ✅ Name & Address • ✅ Email Access • ✅ Debit Card Details • ✅ Cookies details"
        message += f"""
🏦 *Bank:* {item.get('bank', 'N/A')}
🌍 *Country:* {item.get('country', 'N/A')}
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
📋 *Features:* {features}

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
    elif category == "fullz":
        message += f"""
📋 *Fullz Profile*

🔐 *SSN:* `{item.get('ssn', 'N/A')}`
🎂 *DOB:* {item.get('dob', 'N/A')}
👤 *Full Name:* {item.get('full_name', 'N/A')}
🏠 *Address:* {item.get('address', 'N/A')}
📧 *Email:* `{item.get('email', 'N/A')}`
🔑 *Password:* `{item.get('password', 'N/A')}`
"""
        if item.get('education'):
            message += f"🎓 *Education:* {item['education']}\n"
        message += f"\n💵 *Amount Paid:* ${item.get('price', 'N/A')}"
    elif category in ("coinbase", "cashapp", "paypal"):
        message += f"""
💰 *Balance:* {item.get('balance', 'N/A')}
📌 *Type:* {cat_name}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
        if category == "paypal" and item.get('type'):
            message += f"📋 *Account Type:* {item['type']}\n"
    elif category in ("cc", "non_vbv"):
        message += f"""
💳 *Card:* {item.get('brand', 'N/A')}
💰 *Balance:* {item.get('balance', 'N/A')}
💵 *Amount Paid:* ${item.get('price', 'N/A')}
"""
        if category == "non_vbv":
            message += "🔓 *Non-VBV:* ✅\n"
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