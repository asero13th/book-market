import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler
from handlers.my_callback import MyCallback

def post_books(data):
    response = requests.post('https://bookstore-theta-two.vercel.app/api/ordernew', json=data)
    if response.status_code == 200:
        return("Order successfully sent")
    else:
        return("Failed to send order")
    
# Define states
NEW_ORDER_TITLE, NEW_ORDER_AUTHOR, NEW_ORDER_NAME, NEW_ORDER_PHONE, FINISH = range(5)
async def handle_new_order(update: Update, context: CallbackContext, id = "4") -> int:
    """Start the order process and ask for the book title."""
    query = update.callback_query

    print("---------------->something here <-----------------------------")

    await query.answer()
    await query.message.delete()
    
    await query.message.reply_text(
        "Enter the title of the book",
        reply_markup=ReplyKeyboardRemove()
    )

    return NEW_ORDER_TITLE

async def order_title(update: Update, context: CallbackContext) -> int:
    """Store the book title and ask for the author."""
    print("arrived here")
    context.user_data['new_order_title'] = update.message.text

    await update.message.reply_text(
        "Enter the author of the book",
        reply_markup=ReplyKeyboardRemove()
    )
    return NEW_ORDER_AUTHOR

async def order_author(update: Update, context: CallbackContext) -> int:
    """Store the author and ask for the user's name."""
    context.user_data['new_order_author'] = update.message.text
    await update.message.reply_text("Enter your fullname please", reply_markup=ReplyKeyboardRemove())
    return NEW_ORDER_NAME

async def order_name(update: Update, context: CallbackContext) -> int:
    """Store the user's name and ask for the phone number."""
    context.user_data['new_order_name'] = update.message.text
    await update.message.reply_text(
        "Share your number please",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Share your phone", request_contact=True)
                ]
            ], resize_keyboard=True
        )
    )
    return NEW_ORDER_PHONE

async def order_phone(update: Update, context: CallbackContext) -> int:
    """Store the phone number and finish the order process."""
    context.user_data['new_order_phone'] = update.message.contact.phone_number
    

    #TODO: connection with backkend
    # connect it to the back end here --------> connection with backend <----------------
    
    new_order = {
        'Title': context.user_data['new_order_title'],
        'Author': context.user_data['new_order_author'],
        'UserName': update.message.from_user.username,
        'PhoneNumber': context.user_data['new_order_phone'],
    }

    print("Hello there")
    reponse = post_books(new_order)
    print(f"--------------->{reponse}<--------------")
    await update.message.reply_text(reponse, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the conversation."""
    await update.message.reply_text('Order cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
