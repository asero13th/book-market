from telegram import Update
from telegram.ext import CallbackContext
from handlers.buy_book import handle_buy_book
from handlers.rent_book import handle_rent_book
from handlers.sell_book import handle_sell
from handlers.order_new_book import handle_new_order, order_title
from handlers.my_callback import MyCallback


async def handle_callback(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
   
    callback = MyCallback.unpack(callback_data)
   
    if callback.name == 'buy_book':
        handle_buy_book(query, context, callback.id)
    elif callback.name == 'rent_book':
        handle_rent_book(query, context, callback.id)
    elif callback.name == 'sell_book':
        handle_sell(query, context, callback.id)
    elif callback.name == 'order_book':
        await handle_new_order(query, context, callback.id)
    else:
       await query.edit_message_text(text="Unknown callback!")
