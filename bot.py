import logging
import asyncio
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

from config import *
from database import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

init_db()

# ==================== TRANSLATIONS (simplified – add more languages if needed) ====================
TEXTS = {
    'en': {
        'welcome': "✨ *WELCOME TO DEMO BANK ACCOUNTS* ✨\n\n🏦 Buy realistic demo bank accounts and digital assets.\n\n📌 *Shop Categories:*\n• Bank Logs\n• Coinbase\n• CashApp\n• PayPal\n• Fullz\n• Credit Cards\n• Non-VBV\n• Dumps\n• Gift Cards\n\nAll items are for educational purposes only.",
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

# ==================== MAIN MENU ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    create_user(user.id, user.username, user.first_name)
    texts = TEXTS.get(get_user_language(user.id), TEXTS['en'])
    keyboard = [
        [InlineKeyboardButton(texts['shop'], callback_data="shop")],
        [InlineKeyboardButton(texts['support'], callback_data="support")],
        [InlineKeyboardButton(texts['account_balance'], callback_data="account_balance")],
        [InlineKeyboardButton(texts['languages'], callback_data="languages")]
    ]
    await update.message.reply_text(texts['welcome'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
    keyboard = [
        [InlineKeyboardButton(texts['shop'], callback_data="shop")],
        [InlineKeyboardButton(texts['support'], callback_data="support")],
        [InlineKeyboardButton(texts['account_balance'], callback_data="account_balance")],
        [InlineKeyboardButton(texts['languages'], callback_data="languages")]
    ]
    await query.edit_message_text(texts['welcome'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ==================== SHOP ====================
async def show_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    texts = TEXTS.get(get_user_language(user_id), TEXTS['en'])
    keyboard = []
    for key, cat in SHOP_CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(cat['emoji'] + " " + cat['name'], callback_data=f"shop_{key}")])
    keyboard.append([InlineKeyboardButton(texts['back'], callback_data="back_to_menu")])
    await query.edit_message_text(texts['plans_title'], reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_country_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button click
    keyboard = [
        [InlineKeyboardButton("🇺🇸 USA", callback_data="shop_bank_logs_USA")],
        [InlineKeyboardButton("🇬🇧 UK", callback_data="shop_bank_logs_UK")],
        [InlineKeyboardButton("🇨🇦 Canada", callback_data="shop_bank_logs_Canada")],
        [InlineKeyboardButton("🇦🇺 Australia", callback_data="shop_bank_logs_Australia")],
        [InlineKeyboardButton("🔙 Back", callback_data="shop")]
    ]
    await query.edit_message_text("🌍 *Select Country for Bank Logs*", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_category_items(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, country: str = None):
    query = update.callback_query
    await query.answer()
    logger.info(f"Showing items for category: {category}, country: {country}")

    if category == "bank_logs" and country:
        items = get_active_items_by_country(category, country)
        cat_name = f"{SHOP_CATEGORIES.get(category, {}).get('name', category)} - {country}"
        logger.info(f"Found {len(items)} items for {country}")
    else:
        items = get_active_items(category)
        cat_name = SHOP_CATEGORIES.get(category, {}).get('name', category)
        logger.info(f"Found {len(items)} items for {category}")

    if not items:
        await query.edit_message_text(f"❌ No active items in {cat_name}.", reply_markup=None)
        return

    keyboard = []
    for row in items:
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

    # Back button – go back to country selection if bank logs, else main shop
    if category == "bank_logs" and country:
        back_callback = "shop_bank_logs"  # This triggers the country selection again
    else:
        back_callback = "shop"
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data=back_callback)])
    await query.edit_message_text(f"🛍️ *{cat_name}*\n\nSelect an item to buy:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ==================== BUY FLOW (shortened for brevity) ====================
# ... (all the buy_now, process_payment, upload_proof, etc. – same as before)
# You can copy them from the previous full bot.py – they are unchanged.

# ==================== SUPPORT, BALANCE, LANGUAGES ====================
# ... (same as before)

# ==================== ADMIN COMMANDS ====================
# ... (same as before)

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
    elif data.startswith("shop_bank_logs_"):
        # Handle country selection for bank logs
        country = data.replace("shop_bank_logs_", "")
        logger.info(f"User selected country: {country} for bank logs")
        await show_category_items(update, context, "bank_logs", country=country)
    elif data.startswith("shop_"):
        category = data.replace("shop_", "")
        if category == "bank_logs":
            await show_country_selection(update, context)
        else:
            await show_category_items(update, context, category)
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
        await query.edit_message_text("❌ Unknown action. Please try again.")

# ==================== MAIN ====================
def main():
    print("Starting bot...")
    populate_inventory()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
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