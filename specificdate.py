import MetaTrader5 as mt5
from telegram import Bot
import asyncio
from datetime import datetime
import pytz

TELEGRAM_TOKEN = '7727934479:AAFRPDbB9tYS4tNoHF_mdMWoTbVKXbsOjzw'
CHAT_ID = '7267982013'

async def send_message_to_telegram(bot, message):
    """Send a message to Telegram asynchronously."""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")

# Initialize MT5
if not mt5.initialize():
    print(f"MT5 Initialization failed: {mt5.last_error()}")
    quit()
else:
    print("MT5 Initialized successfully.")

# Fetch orders for a specific date
def fetch_orders_for_date(date_str):
    """Fetch historical orders for a specific date."""
    # Indian Standard Time (IST)
    timezone = pytz.timezone("Asia/Kolkata")
    
    # Parse the input date
    specific_date = datetime.strptime(date_str, "%Y-%m-%d")
    start_date = timezone.localize(specific_date.replace(hour=0, minute=0, second=0, microsecond=0))
    end_date = timezone.localize(specific_date.replace(hour=23, minute=59, second=59, microsecond=999999))

    # Fetch historical orders
    orders_history = mt5.history_orders_get(start_date, end_date)
    if orders_history is None:
        print(f"Error fetching order history: {mt5.last_error()}")
        orders_history = []

    return list(orders_history)

# Format order information
def format_order_info(orders, title, date_str):
    """Format order details for Telegram message."""
    message = f"*{title} for {date_str}*\n"
    if not orders:
        message += "_No orders found._\n"
    else:
        for order in orders:
            order_time = datetime.fromtimestamp(order.time_setup, tz=pytz.timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
            message += (
                f"Order ID: {order.ticket}\n"
                f"Symbol: {order.symbol}\n"
                f"Type: {order.type}\n"
                f"Volume: {getattr(order, 'volume_initial', 'N/A')}\n"
                f"Price: {getattr(order, 'price_open', 'N/A')}\n"
                f"Status: {order.state}\n"
                f"Date/Time (IST): {order_time}\n\n"
            )
    return message

# Main function to execute with a specific date
async def main():
    """Fetch orders for a specific date and send to Telegram."""
    bot = Bot(token=TELEGRAM_TOKEN)

    # Specify the date (YYYY-MM-DD format)
    specific_date = "2024-12-31"  

    # Fetch orders for the specific date
    orders_history = fetch_orders_for_date(specific_date)

    # Format the message
    history_orders_message = format_order_info(orders_history, "Order History", specific_date)

    # Send message to Telegram
    await send_message_to_telegram(bot, history_orders_message)

# Cleanup MT5
def cleanup_mt5():
    """Shutdown MT5 connection."""
    mt5.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        cleanup_mt5()
