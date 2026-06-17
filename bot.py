import logging
import asyncio
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

from config import *
from database import *

# ─── CHANNEL CONFIGURATION ───
CHANNEL_USERNAME = "Twoeasymarket1"   # without @
CHANNEL_URL = "https://t.me/Twoeasymarket1"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

init_db()

# ==================== TRANSLATIONS ====================
TEXTS = {
    'en': {
        'welcome': "✨ *Welcome to official 2easy marketplace* ✨\n\n🏦 \n\n📌 *Shop Categories:*\n• Bank Logs\n• Coinbase\n• CashApp\n• PayPal\n• Fullz\n• Credit Cards\n• Non-VBV\n• Dumps\n• Gift Cards\n\n",
        'shop': "🏪 SHOP",
        'support': "🆘 SUPPORT",
        'account_balance': "💰 ACCOUNT BALANCE",
        'languages': "🌐 LANGUAGES",
        'back': "🔙 BACK",
        'confirm': "✅ Confirm",
        'cancel': "❌ Cancel",
        'upload_proof': "📸 UPLOAD PROOF",
        'contact_support': "📞 CONTACT SUPPORT",
        'lang_set': "✅ Language set to *{lang}*.",
        'error_address': "❌ {method} payments are not configured yet. Contact @{support}",
        'no_stock': "❌ No active items in this category.",
        'payment_for': "💰 *Payment*",
        'select_method': "👇 Select payment method:",
        'complete_payment': "💳 *COMPLETE YOUR PAYMENT*\n\n📌 *Item:* {plan}\n💲 *Amount:* `${price}`\n🔹 *Method:* {symbol} {method}\n───────────────────────────────\n📤 *Send exactly* `${price}` *in* `{method}` *to:*\n`{address}`\n───────────────────────────────\n📸 *After sending:*\n1. Take a screenshot\n2. Click *'Upload Proof'*\n3. Send the image here\n⏱️ Verification within 15–30 min.",
        'send_proof': "📸 *SEND YOUR PAYMENT PROOF*\n\nPlease send a clear screenshot of your `{method}` payment for the *{plan}* (${price}).\n\n🖼️ *Instructions:*\n• Take a screenshot showing the transaction\n• Send it as a *PHOTO* in this chat",
        'proof_received': "✅ *PAYMENT PROOF RECEIVED!*\n\nThank you for your payment for the item.\n\n🛂 We will verify and deliver your order.\n⏱️ Estimated time: 15–30 minutes.\n\n📞 For urgent questions: @{support}",
        'no_accounts': "📭 *No purchased items found.*",
        'support_text': "🆘 *SUPPORT CENTER*\n\n📱 Telegram: @{support}\n⏰ Response time: 15–30 min (24/7)",
        'plans_title': "🏪 *SHOP – Choose Category*",
        'country_select': "🌍 *Select Country for Bank Logs*",
    },
    'es': {}, 'fr': {}, 'de': {}, 'zh': {}, 'ar': {}, 'ru': {}
}

async def get_text(update: Update, key: str, **kwargs):
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    text = TEXTS.get(lang, TEXTS['en']).get(key, TEXTS['en'][key])
    return text.format(**kwargs) if kwargs else text

# ==================== CHANNEL VERIFICATION ====================
async def is_user_in_channel(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_USERNAME}", user_id=user_id)
        status = member.status
        logger.info(f"User {user_id} channel status: {status}")
        return status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.warning(f"Channel check failed for user {user_id}: {e}")
        return False

# ==================== MAIN MENU ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    logger.info(f"User {user_id} sent /start")

    if not await is_user_in_channel(context.bot, user_id):
        keyboard = [
            [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_channel")]
        ]
        await update.message.reply_text(
            "🚫 *Access Restricted*\n\n"
            "You must join our official channel before using this bot.\n\n"
            "👇 Click the button below to join, then click 'I've Joined' to continue.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    create_user(user.id, user.username, user.first_name)
    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message=None):
    user_id = update.effective_user.id if hasattr(update, 'effective_user') else update.callback_query.from_user.id
    texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
    keyboard = [
        [InlineKeyboardButton(texts['shop'], callback_data="shop")],
        [InlineKeyboardButton(texts['support'], callback_data="support")],
        [InlineKeyboardButton(texts['account_balance'], callback_data="account_balance")],
        [InlineKeyboardButton(texts['languages'], callback_data="languages")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if message:
        await message.reply_text(texts['welcome'], reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(texts['welcome'], reply_markup=reply_markup, parse_mode="Markdown")

# ==================== SHOP ====================
async def show_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
    keyboard = []
    for key, cat in SHOP_CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(cat['emoji'] + " " + cat['name'], callback_data=f"shop_{key}")])
    keyboard.append([InlineKeyboardButton(texts['back'], callback_data="back_to_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(texts['plans_title'], reply_markup=reply_markup, parse_mode="Markdown")

async def show_country_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🇺🇸 USA", callback_data="shop_bank_logs_USA")],
        [InlineKeyboardButton("🇬🇧 UK", callback_data="shop_bank_logs_UK")],
        [InlineKeyboardButton("🇨🇦 Canada", callback_data="shop_bank_logs_Canada")],
        [InlineKeyboardButton("🇦🇺 Australia", callback_data="shop_bank_logs_Australia")],
        [InlineKeyboardButton("🔙 Back", callback_data="shop")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("🌍 *Select Country for Bank Logs*", reply_markup=reply_markup, parse_mode="Markdown")

async def show_category_items(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, country: str = None, page: int = 0):
    query = update.callback_query
    await query.answer()
    logger.info(f"Showing items for category: {category}, country: {country}, page: {page}")

    ITEMS_PER_PAGE = 10

    if category == "bank_logs" and country:
        items = get_active_items_by_country(category, country)
        cat_name = f"{SHOP_CATEGORIES.get(category, {}).get('name', category)} - {country}"
    else:
        items = get_active_items(category)
        cat_name = SHOP_CATEGORIES.get(category, {}).get('name', category)

    if not items:
        await query.message.reply_text(f"❌ No active items in {cat_name}.")
        return

    total_items = len(items)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    start_idx = page * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, total_items)
    page_items = items[start_idx:end_idx]

    keyboard = []
    for row in page_items:
        item_id, item_data_json, price, status = row
        item_data = json.loads(item_data_json)

        if category == "bank_logs":
            display = f"🏦 {item_data.get('bank', 'Account')} | Balance: {item_data.get('balance', '$0')} | ${price}"
        elif category == "coinbase":
            display = f"💰 Coinbase | Balance: {item_data.get('balance', '$0')} | ${price}"
        elif category == "cashapp":
            display = f"💵 CashApp | Balance: {item_data.get('balance', '$0')} | ${price}"
        elif category == "paypal":
            display = f"💳 PayPal | Balance: {item_data.get('balance', '$0')} | ${price}"
        elif category == "fullz":
            full_name = item_data.get('full_name', 'Unknown')
            dob = item_data.get('dob', 'N/A')
            ssn_last4 = item_data.get('ssn', '')[-4:] if item_data.get('ssn') else '****'
            display = f"📋 {full_name} | DOB: {dob} | SSN: ***-***-{ssn_last4} | ${price}"
        elif category == "cc":
            display = f"💳 {item_data.get('brand', 'Card')} | Balance: {item_data.get('balance', '$0')} | ${price}"
        elif category == "non_vbv":
            display = f"🔓 Non-VBV {item_data.get('brand', 'Card')} | Balance: {item_data.get('balance', '$0')} | ${price}"
        elif category == "dumps":
            display = f"💾 {item_data.get('brand', '')} {item_data.get('type', '')} | ${price}"
        elif category == "shopwithscrip":
            display = f"🛍️ {item_data.get('platform', 'Gift Card')} | Balance: {item_data.get('balance', '$0')} | ${price}"
        else:
            display = f"Item #{item_id} | ${price}"
        keyboard.append([InlineKeyboardButton(display, callback_data=f"buy_item_{item_id}")])

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Previous", callback_data=f"page:{category}:{country if country else 'none'}:{page-1}"))
    nav_buttons.append(InlineKeyboardButton(f"📄 {page+1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data=f"page:{category}:{country if country else 'none'}:{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)

    back_callback = "shop_bank_logs" if category == "bank_logs" and country else "shop"
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=back_callback)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        f"🛍️ *{cat_name}*\n\nShowing {start_idx+1}-{end_idx} of {total_items} items:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ==================== BUY FLOW ====================
async def confirm_item(update: Update, context: ContextTypes.DEFAULT_TYPE, item_id: int):
    query = update.callback_query
    item = get_item_by_id(item_id)
    if not item or item['status'] != 'active':
        await query.message.reply_text("❌ Item unavailable.")
        return
    category = item['category']
    item_data = item['item_data']
    price = item['price']
    cat_name = SHOP_CATEGORIES.get(category, {}).get("name", category)

    if category == "bank_logs":
        features = "✅ Online Access • ✅ Account/Routing Number • ✅ Name & Address • ✅ Email Access • ✅ Debit Card Details • ✅ Cookies"
        details = (
            f"🏦 *Bank:* {item_data.get('bank', 'N/A')}\n"
            f"🌍 *Country:* {item_data.get('country', 'N/A')}\n"
            f"💰 *Balance:* {item_data.get('balance', 'N/A')}\n"
            f"📋 *Features:* {features}"
        )
    elif category == "fullz":
        ssn_last4 = item_data.get('ssn', '')[-4:] if item_data.get('ssn') else '****'
        details = f"📋 *Full Name:* {item_data.get('full_name', 'N/A')}\n🎂 *DOB:* {item_data.get('dob', 'N/A')}\n🔐 *SSN (last 4):* ***-***-{ssn_last4}"
        if item_data.get('education'):
            details += f"\n🎓 *Education:* {item_data['education']}"
    else:
        details = f"💰 *Balance:* {item_data.get('balance', 'N/A')}"
        if category in ("cc", "non_vbv"):
            details += f"\n💳 *Brand:* {item_data.get('brand', 'N/A')}"
        elif category == "dumps":
            details += f"\n💾 *Type:* {item_data.get('type', 'N/A')}"

    context.user_data['selected_item'] = {'item_id': item_id, 'price': price, 'category': category, 'item_data': item_data}
    keyboard = [
        [InlineKeyboardButton("💳 Buy Now", callback_data=f"confirm_item_{item_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"shop_{category}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"📌 *Item Details*\n\n{details}\n\n💰 *Price:* ${price}\n\nProceed?", reply_markup=reply_markup, parse_mode="Markdown")

async def buy_now(update: Update, context: ContextTypes.DEFAULT_TYPE, item_id: int):
    query = update.callback_query
    selected = context.user_data.get('selected_item', {})
    if not selected or selected.get('item_id') != item_id:
        item = get_item_by_id(item_id)
        if not item or item['status'] != 'active':
            await query.message.reply_text("❌ Item unavailable.")
            return
        selected = {'item_id': item_id, 'price': item['price'], 'category': item['category'], 'item_data': item['item_data']}
        context.user_data['selected_item'] = selected
    price = selected['price']
    keyboard = [
        [InlineKeyboardButton("₿ BTC", callback_data="pay_btc_item"), InlineKeyboardButton("💲 USDT", callback_data="pay_usdt_item")],
        [InlineKeyboardButton("Ł LTC", callback_data="pay_ltc_item"), InlineKeyboardButton("Ð DOGE", callback_data="pay_doge_item")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"shop_{selected['category']}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"💰 *Payment*\n\n💵 Amount: `${price}`\n\nSelect payment method:", reply_markup=reply_markup, parse_mode="Markdown")

async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE, method: str):
    query = update.callback_query
    selected = context.user_data.get('selected_item', {})
    if not selected:
        await query.message.reply_text("❌ No item selected.")
        return
    price = selected['price']
    category = selected['category']
    cat_name = SHOP_CATEGORIES.get(category, {}).get("name", category)
    method_info = PAYMENT_METHODS.get(method, {"name": method.upper(), "symbol": ""})
    address = WALLET_ADDRESSES.get(method, "NOT_CONFIGURED")
    if address == "NOT_CONFIGURED":
        texts = TEXTS.get(get_user_language(query.from_user.id), TEXTS['en'])
        await query.message.reply_text(texts['error_address'].format(method=method.upper(), support=SUPPORT_USERNAME))
        return
    context.user_data['pending_payment'] = {
        'item_id': selected['item_id'],
        'price': price,
        'method': method,
        'category': category,
        'item_data': selected.get('item_data', {})
    }
    text = f"""
💳 *COMPLETE YOUR PAYMENT*

📌 *Item:* {cat_name}
💲 *Amount:* `${price}`
🔹 *Method:* {method_info['symbol']} {method_info['name']}
───────────────────────────────
📤 *Send exactly* `${price}` *in* `{method}` *to:*
`{address}`
───────────────────────────────
📸 *After sending:*
1. Take a screenshot
2. Click *'Upload Proof'*
3. Send the image here
⏱️ Verification within 15–30 min.
"""
    keyboard = [
        [InlineKeyboardButton("📸 UPLOAD PROOF", callback_data="upload_proof_item")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"shop_{category}")],
        [InlineKeyboardButton("📞 CONTACT SUPPORT", url=f"https://t.me/{SUPPORT_USERNAME}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def upload_proof_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    pending = context.user_data.get('pending_payment', {})
    if not pending:
        await query.message.reply_text("❌ No pending payment.")
        return
    price = pending['price']
    method = pending['method']
    cat_name = SHOP_CATEGORIES.get(pending['category'], {}).get("name", "Item")
    text = f"""
📸 *SEND YOUR PAYMENT PROOF*

Please send a clear screenshot of your `{method}` payment for the *{cat_name}* (${price}).

🖼️ *Instructions:*
• Take a screenshot showing the transaction
• Send it as a *PHOTO* in this chat
"""
    keyboard = [[InlineKeyboardButton("❌ Cancel", callback_data="shop")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    photo = update.message.photo[-1]
    pending = context.user_data.get('pending_payment', {})
    if not pending:
        await update.message.reply_text("❌ No pending payment. Please start from the shop.")
        return
    item_id = pending['item_id']
    price = pending['price']
    category = pending['category']
    method = pending['method']
    add_payment_record(user.id, f"item_{item_id}", price, method, f"photo_{datetime.now().timestamp()}")
    caption = f"📸 *NEW PAYMENT PROOF*\n\n👤 {user.first_name} (@{user.username or 'N/A'})\n🆔 {user.id}\n📦 Item #{item_id}\n💰 ${price}\n💳 {method.upper()}\n\n👉 /verify {item_id} {user.id}"
    await context.bot.send_photo(chat_id=OWNER_ID, photo=photo.file_id, caption=caption, parse_mode="Markdown")
    if SUPPORT_USERNAME:
        try:
            await context.bot.send_photo(chat_id=f"@{SUPPORT_USERNAME}", photo=photo.file_id, caption=f"Proof from @{user.username or user.first_name}")
        except:
            pass
    await update.message.reply_text(f"✅ *PAYMENT PROOF RECEIVED!*\n\nThank you! We will verify and deliver your order within 15-30 minutes.\n\n📞 For urgent: @{SUPPORT_USERNAME}", parse_mode="Markdown")
    context.user_data['pending_payment'] = {}

# ==================== SUPPORT, BALANCE, LANGUAGES ====================
async def show_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
    text = "💰 *Account Balance*\n\nYou have not purchased any items yet.\n"
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    texts = TEXTS.get(get_user_language(query.from_user.id), TEXTS['en'])
    text = texts['support_text'].format(support=SUPPORT_USERNAME)
    keyboard = [
        [InlineKeyboardButton("📞 CONTACT SUPPORT", url=f"https://t.me/{SUPPORT_USERNAME}")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_languages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")],
        [InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr")],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("🇨🇳 中文", callback_data="lang_zh")],
        [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("🌐 *Select your language*", reply_markup=reply_markup, parse_mode="Markdown")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE, data):
    query = update.callback_query
    lang_code = data.split("_")[1]
    set_user_language(query.from_user.id, lang_code)
    lang_names = {'en':'English','es':'Español','fr':'Français','de':'Deutsch','zh':'中文','ar':'العربية','ru':'Русский'}
    await query.message.reply_text(f"✅ Language set to *{lang_names.get(lang_code, lang_code)}*.", parse_mode="Markdown")
    await asyncio.sleep(1)
    await show_main_menu_from_query(update, context)

async def show_main_menu_from_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
    keyboard = [
        [InlineKeyboardButton(texts['shop'], callback_data="shop")],
        [InlineKeyboardButton(texts['support'], callback_data="support")],
        [InlineKeyboardButton(texts['account_balance'], callback_data="account_balance")],
        [InlineKeyboardButton(texts['languages'], callback_data="languages")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(texts['welcome'], reply_markup=reply_markup, parse_mode="Markdown")

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if not await is_user_in_channel(context.bot, user_id):
        keyboard = [
            [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_URL)],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_channel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "🚫 *Access Restricted*\n\n"
            "You must join our official channel to use this bot.\n\n"
            "👇 Click the button below to join, then click 'I've Joined'.",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
    keyboard = [
        [InlineKeyboardButton(texts['shop'], callback_data="shop")],
        [InlineKeyboardButton(texts['support'], callback_data="support")],
        [InlineKeyboardButton(texts['account_balance'], callback_data="account_balance")],
        [InlineKeyboardButton(texts['languages'], callback_data="languages")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(texts['welcome'], reply_markup=reply_markup, parse_mode="Markdown")

# ==================== ADMIN COMMANDS ====================
async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: `/verify <item_id> <user_id>`", parse_mode="Markdown")
        return
    try:
        item_id = int(args[0])
        user_id = int(args[1])
        item = get_item_by_id(item_id)
        if not item or item['status'] != 'active':
            await update.message.reply_text("❌ Item not available.")
            return
        mark_item_sold(item_id)
        from config import format_item_message
        user_text = format_item_message(item['category'], item['item_data'])
        await context.bot.send_message(chat_id=user_id, text=user_text, parse_mode="Markdown")
        await update.message.reply_text(f"✅ Item #{item_id} delivered to user {user_id}.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def pending_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("Use /verify <item_id> <user_id> to deliver items.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Unauthorized.")
        return
    await update.message.reply_text("📊 Bot running. Use /pending to check pending payments.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please use the buttons. Send /start to see the menu.")

# ==================== CHECK COMMAND ====================
async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    if await is_user_in_channel(context.bot, user_id):
        await update.message.reply_text("✅ You are a member of the channel.")
    else:
        await update.message.reply_text("❌ You are NOT a member of the channel. Please join @Twoeasymarket1 first.")

# ==================== CALLBACK DISPATCHER ====================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    logger.info(f"Button clicked: {data}")

    if data == "shop":
        await show_shop(update, context)
    elif data == "support":
        await show_support(update, context)
    elif data == "account_balance":
        await show_balance(update, context)
    elif data == "languages":
        await show_languages(update, context)
    elif data == "back_to_menu":
        await back_to_menu(update, context)
    elif data == "check_channel":
        user_id = query.from_user.id
        if await is_user_in_channel(context.bot, user_id):
            create_user(user_id, query.from_user.username, query.from_user.first_name)
            texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
            keyboard = [
                [InlineKeyboardButton(texts['shop'], callback_data="shop")],
                [InlineKeyboardButton(texts['support'], callback_data="support")],
                [InlineKeyboardButton(texts['account_balance'], callback_data="account_balance")],
                [InlineKeyboardButton(texts['languages'], callback_data="languages")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(texts['welcome'], reply_markup=reply_markup, parse_mode="Markdown")
        else:
            await query.answer("You haven't joined the channel yet. Please join first!", show_alert=True)
    elif data.startswith("shop_bank_logs_"):
        country = data.replace("shop_bank_logs_", "")
        await show_category_items(update, context, "bank_logs", country=country, page=0)
    elif data.startswith("shop_"):
        category = data.replace("shop_", "")
        if category == "bank_logs":
            await show_country_selection(update, context)
        else:
            await show_category_items(update, context, category, page=0)
    elif data.startswith("page:"):
        parts = data.split(":")
        if len(parts) == 4:
            category = parts[1]
            country = parts[2] if parts[2] != "none" else None
            try:
                page = int(parts[3])
            except ValueError:
                await query.message.reply_text("❌ Invalid page. Please try again.")
                return
            await show_category_items(update, context, category, country, page)
    elif data == "noop":
        pass
    elif data.startswith("buy_item_"):
        item_id = int(data.replace("buy_item_", ""))
        await confirm_item(update, context, item_id)
    elif data.startswith("confirm_item_"):
        item_id = int(data.replace("confirm_item_", ""))
        await buy_now(update, context, item_id)
    elif data.startswith("pay_") and data.endswith("_item"):
        method = data.split("_")[1]
        await process_payment(update, context, method)
    elif data.startswith("upload_proof_item"):
        await upload_proof_prompt(update, context)
    elif data.startswith("lang_"):
        await set_language(update, context, data)
    else:
        logger.warning(f"Unknown callback: {data}")
        await query.message.reply_text("❌ Unknown action. Please try again.")

# ==================== MAIN ====================
def main():
    print("Starting bot...")
    populate_inventory()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check_command))
    application.add_handler(CommandHandler("verify", verify_command))
    application.add_handler(CommandHandler("pending", pending_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_payment_proof))
    print("Bot is running.")
    application.run_polling()

if __name__ == "__main__":
    main()