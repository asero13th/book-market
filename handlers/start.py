from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from handlers.callback_handlers import MyCallback


async def start(update: Update, context: CallbackContext) -> None:
 
    menu = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Buy Book", callback_data=MyCallback(name="buy_book", id="1").pack()),
                InlineKeyboardButton(text="Rent Book", callback_data=MyCallback(name="rent_book", id="2").pack()),
            ],
            [
                InlineKeyboardButton(text="Sell Book", callback_data=MyCallback(name="sell_book", id="3").pack()),
                InlineKeyboardButton(text="Order new", callback_data=MyCallback(name="order_book", id="4").pack()),
            ]
        ]
    )
 
    
    await update.message.reply_text("Welcome to ብርሀን መፅሐፍ ማከፋፈያ", reply_markup=menu)

