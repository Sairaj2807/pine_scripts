import MetaTrader5 as mt5
from telegram import Bot
import asyncio
from datetime import datetime
import pytz


# Telegram Bot Setup
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

# Fetch all orders
def fetch_orders():
    """Fetch historical and open orders from MT5."""
    # Set timezone to match MT5 server time
    timezone = pytz.timezone("Etc/UTC")  # Replace with the broker's timezone if known
    start_date = timezone.localize(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0))
    end_date = timezone.localize(datetime.now())

    # Fetch historical orders
    orders_history = mt5.history_orders_get(start_date, end_date)
    if orders_history is None:
        print(f"Error fetching order history: {mt5.last_error()}")
        orders_history = []

    # Fetch open orders
    open_orders = mt5.orders_get()
    if open_orders is None:
        print(f"Error fetching open orders: {mt5.last_error()}")
        open_orders = []

    return list(orders_history), list(open_orders)

# Format order information
def format_order_info(orders, title):
    """Format order details for Telegram message."""
    message = f"*{title}*\n"
    if not orders:
        message += "_No orders found._\n"
    else:
        for order in orders:
            message += (
                f"Order ID: {order.ticket}\n"
                f"Symbol: {order.symbol}\n"
                f"Type: {order.type}\n"
                f"Volume: {getattr(order, 'volume_initial', 'N/A')}\n"
                f"Price: {getattr(order, 'price_open', 'N/A')}\n"
                f"Status: {order.state}\n\n"
            )
    return message

# Main function to execute at the end of the day
async def main():
    """Fetch orders and send to Telegram."""
    bot = Bot(token=TELEGRAM_TOKEN)

    # Fetch orders
    orders_history, open_orders = fetch_orders()

    # Format order messages
    open_orders_message = format_order_info(open_orders, "Open Orders")
    history_orders_message = format_order_info(orders_history, "Order History")

    # Combine messages
    final_message = f"{open_orders_message}\n{history_orders_message}"

    # Send message to Telegram
    await send_message_to_telegram(bot, final_message)

# Cleanup MT5
def cleanup_mt5():
    """Shutdown MT5 connection."""
    mt5.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        cleanup_mt5()



