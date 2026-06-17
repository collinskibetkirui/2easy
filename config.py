import os
from dotenv import load_dotenv
import random
import string
from datetime import datetime, timedelta

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8849937805:AAHSrSZMdBy8T_av-7IH49ULpNAAZfPqiLo")
VIP_CHANNEL_ID = int(os.getenv("VIP_CHANNEL_ID", "-1001234567890"))
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "Twoeasysupport")

# ─── SHOP CATEGORIES WITH UNICODE ESCAPES ───
SHOP_CATEGORIES = {
    "bank_logs": {"name": "\U0001F3E6 Bank Logs ", "emoji": "\U0001F3E6"},
    "coinbase": {"name": "\U0001F4B0 Coinbase ", "emoji": "\U0001F4B0"},
    "cashapp": {"name": "\U0001F4B5 CashApp ", "emoji": "\U0001F4B5"},
    "paypal": {"name": "\U0001F4B3 PayPal ", "emoji": "\U0001F4B3"},
    "fullz": {"name": "\U0001F4CB Fullz ", "emoji": "\U0001F4CB"},
    "cc": {"name": "\U0001F4B3 Credit Cards ", "emoji": "\U0001F4B3"},
    "non_vbv": {"name": "\U0001F513 Non-VBV Cards ", "emoji": "\U0001F513"},
    "dumps": {"name": "\U0001F4BE Dumps ", "emoji": "\U0001F4BE"},
    "shopwithscrip": {"name": "\U0001F6CD Gift Cards ", "emoji": "\U0001F6CD"},
}

PAYMENT_METHODS = {
    "btc": {"name": "Bitcoin (BTC)", "symbol": "\u20BF"},
    "usdt": {"name": "USDT (TRC20)", "symbol": "\U0001F4B2"},
    "ltc": {"name": "LiteCoin (LTC)", "symbol": "\u0141"},
    "doge": {"name": "Dogecoin (DOGE)", "symbol": "\u00D0"},
}

WALLET_ADDRESSES = {
    "btc": "3KXxcezpun9AJbNSg88PmD1HTH5s7inRXx",
    "usdt": "TWpr3drUQPBCLpHsbmHHsFwPwqM4X1PZEY",
    "ltc": "MPyWXR8WGNZS9gx4D1WFqoUtF4KSGczJMv",
    "doge": "DDxz1EUymydsBs2VC5ipNVNUSFkAS8DpEE",
}

# ─── BANK LISTS PER COUNTRY ───
BANK_LISTS = {
    "USA": [
        "Chase", "Bank of America", "Wells Fargo", "Citigroup", "U.S. Bancorp",
        "Capital One Financial", "PNC Financial Services", "Goldman Sachs", "Truist",
        "TD Bank", "Morgan Stanley Bank NA", "BMO", "Morgan Stanley Private Bank",
        "First Citizens Bank", "Citizens Bank"
    ],
    "UK": [
        "HSBC UK", "Barclays", "Lloyds Bank", "NatWest", "Santander UK",
        "Monzo", "Revolut"
    ],
    "Canada": [
        "TD Canada Trust", "RBC Royal Bank", "Scotiabank", "BMO Bank of Montreal",
        "CIBC", "Tangerine"
    ],
    "Australia": [
        "Commonwealth Bank", "Westpac", "ANZ Bank", "NAB", "Macquarie Bank",
        "Bendigo Bank"
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

def price_from_balance(balance):
    """Calculate 5.5% of balance, round to nearest $5, min $5, max $1000."""
    price = round(balance * 0.055 / 5) * 5
    return max(5, min(1000, price))

def balance_for_price(price):
    """Return a balance that yields exactly the given price (5.5% rule)."""
    return int(price / 0.055)

# ---- Generate bank logs with featured items for USA ----
def generate_bank_logs(count_per_country=120):
    items = []
    balance_ranges = {
        "USA": (1200, 16000),
        "UK": (100, 2900),
        "Canada": (100, 2900),
        "Australia": (100, 2900)
    }
    featured_prices = [50, 75, 100]  # for USA only

    for country, banks in BANK_LISTS.items():
        per_bank = count_per_country // len(banks)
        remainder = count_per_country % len(banks)
        for i, bank in enumerate(banks):
            count = per_bank + (1 if i < remainder else 0)
            min_bal, max_bal = balance_ranges[country]

            if country == "USA":
                for price in featured_prices:
                    balance = balance_for_price(price)
                    item = {
                        "bank": bank,
                        "country": country,
                        "balance": f"${balance:,.2f}",
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
                    }
                    items.append(item)
                    count -= 1

            for _ in range(count):
                balance = random.randint(min_bal, max_bal)
                price = price_from_balance(balance)
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

# ---- Other categories (unchanged, 100 each) ----
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

        base_price = 5
        extra = 0
        if address: extra += 1
        if email: extra += 1
        if password: extra += 1
        if education: extra += 2
        price = min(60, base_price + extra * 5)
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

def generate_accounts(category, count=100):
    items = []
    for _ in range(count):
        balance = random.randint(100, 2900)
        price = price_from_balance(balance)
        item = {"balance": f"${balance:,.2f}", "price": int(price)}
        if category == "paypal":
            item["type"] = random.choice(["Business", "Verified Personal", "Premier"])
        items.append(item)
    return items

def generate_cards(category, count=100):
    items = []
    brands = ["Visa", "Mastercard", "Amex", "Discover"]
    for _ in range(count):
        balance = random.randint(100, 2900)
        price = price_from_balance(balance)
        item = {"brand": random.choice(brands), "balance": f"${balance:,.2f}", "price": int(price)}
        if category == "non_vbv":
            item["non_vbv"] = True
        items.append(item)
    return items

def generate_dumps(count=100):
    types = ["Classic", "Gold", "Platinum", "World", "Elite"]
    prices = {"Classic": 15, "Gold": 30, "Platinum": 45, "World": 60, "Elite": 75}
    brands = ["Visa", "Mastercard", "Amex"]
    items = []
    for _ in range(count):
        dtype = random.choice(types)
        balance = random.randint(100, 2900)
        item = {
            "brand": random.choice(brands),
            "type": dtype,
            "price": prices[dtype],
            "balance": f"${balance:,.2f}"
        }
        items.append(item)
    return items

def generate_giftcards(count=100):
    platforms = ["Amazon", "Walmart", "Target", "Best Buy", "Starbucks", "Uber", "DoorDash", "Netflix", "Spotify", "Google Play", "Apple Store", "Sephora", "Nike", "Adidas", "Steam", "PlayStation", "Xbox", "eBay", "Etsy", "Wayfair", "Chewy", "Lowes", "Home Depot", "Macy's", "Kohl's"]
    items = []
    for _ in range(count):
        balance = random.randint(5, 500)
        discount = random.uniform(0.05, 0.20)
        price = round(balance * (1 - discount) / 5) * 5
        price = max(3, min(475, price))
        items.append({
            "platform": random.choice(platforms),
            "balance": f"${balance:,.2f}",
            "price": int(price)
        })
    return items

DEMO_ITEMS = {
    "bank_logs": generate_bank_logs(120),
    "coinbase": generate_accounts("coinbase", 100),
    "cashapp": generate_accounts("cashapp", 100),
    "paypal": generate_accounts("paypal", 100),
    "fullz": generate_fullz(100),
    "cc": generate_cards("cc", 100),
    "non_vbv": generate_cards("non_vbv", 100),
    "dumps": generate_dumps(100),
    "shopwithscrip": generate_giftcards(100),
}

def format_item_message(category, item):
    cat_name = SHOP_CATEGORIES.get(category, {}).get("name", category)
    message = f"""
\U0001F389 *DEMO {cat_name.upper()} DELIVERED!*

\U0001F4CC *Type:* {cat_name}
\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD
"""
    if category == "bank_logs":
        features = "\u2705 Online Access \u2022 \u2705 Account/Routing Number \u2022 \u2705 Name & Address \u2022 \u2705 Email Access \u2022 \u2705 Debit Card Details \u2022 \u2705 Cookies details"
        message += f"""
\U0001F3E6 *Bank:* {item.get('bank', 'N/A')}
\U0001F30D *Country:* {item.get('country', 'N/A')}
\U0001F4B0 *Balance:* {item.get('balance', 'N/A')}
\U0001F4B5 *Amount Paid:* ${item.get('price', 'N/A')}
\U0001F4CB *Features:* {features}

\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD
\U0001F4E7 *Email Access:*
   • Email: `{item.get('email', 'N/A')}`
   • Password: `{item.get('password', 'N/A')}`

\U0001F3E6 *Account Details:*
   • Routing Number: `{item.get('routing_number', 'N/A')}`
   • Account Number: `{item.get('account_number', 'N/A')}`
   • Full Name: {item.get('full_name', 'N/A')}
   • Address: {item.get('address', 'N/A')}

\U0001F36A *Cookies:*
`{item.get('cookies', 'N/A')}`

\U0001F4B3 *Debit Card:*
   • Brand: {item.get('card_brand', 'N/A')}
   • Number: `{item.get('card_number', 'N/A')}`
   • Expiry: {item.get('card_expiry', 'N/A')}
   • CVV: `{item.get('card_cvv', 'N/A')}`
"""
    elif category == "fullz":
        message += f"""
\U0001F4CB *Fullz Profile*

\U0001F510 *SSN:* `{item.get('ssn', 'N/A')}`
\U0001F382 *DOB:* {item.get('dob', 'N/A')}
\U0001F464 *Full Name:* {item.get('full_name', 'N/A')}
\U0001F3E0 *Address:* {item.get('address', 'N/A')}
\U0001F4E7 *Email:* `{item.get('email', 'N/A')}`
\U0001F511 *Password:* `{item.get('password', 'N/A')}`
"""
        if item.get('education'):
            message += f"\U0001F393 *Education:* {item['education']}\n"
        message += f"\n\U0001F4B5 *Amount Paid:* ${item.get('price', 'N/A')}"
    elif category in ("coinbase", "cashapp", "paypal"):
        message += f"""
\U0001F4B0 *Balance:* {item.get('balance', 'N/A')}
\U0001F4CC *Type:* {cat_name}
\U0001F4B5 *Amount Paid:* ${item.get('price', 'N/A')}
"""
        if category == "paypal" and item.get('type'):
            message += f"\U0001F4CB *Account Type:* {item['type']}\n"
    elif category in ("cc", "non_vbv"):
        message += f"""
\U0001F4B3 *Card:* {item.get('brand', 'N/A')}
\U0001F4B0 *Balance:* {item.get('balance', 'N/A')}
\U0001F4B5 *Amount Paid:* ${item.get('price', 'N/A')}
"""
        if category == "non_vbv":
            message += "\U0001F513 *Non-VBV:* \u2705\n"
    elif category == "dumps":
        message += f"""
\U0001F4BE *Dumps:* {item.get('brand', 'N/A')} - {item.get('type', 'N/A')}
\U0001F4B0 *Balance:* {item.get('balance', 'N/A')}
\U0001F4B5 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    elif category == "shopwithscrip":
        message += f"""
\U0001F6CD *Platform:* {item.get('platform', 'N/A')}
\U0001F4B0 *Balance:* {item.get('balance', 'N/A')}
\U0001F4B5 *Amount Paid:* ${item.get('price', 'N/A')}
"""
    message += f"""
\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD\U0001F4CD

📞 Support: @{SUPPORT_USERNAME}
"""
    return message