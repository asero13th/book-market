import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler
from handlers.my_callback import MyCallback

def post_books(data):
    response = requests.post('https://bookstore-theta-two.vercel.app/api/customerbook', json=data)
    if response.status_code == 200:
        return("sell successfully sent")
    else:
        return("Failed to send sell")
    
# Define states
SELL_TITLE, SELL_AUTHOR, SELL_NAME, SELL_PHONE, SELL_EDITION, SELL_PRICE,SELL_STATUS,SELL_OVERVIEW,SELL_PHONE , FINISH = range(10)
async def handle_sell(update: Update, context: CallbackContext, id = "4") -> int:
    """Start the sell process and ask for the book title."""
    query = update.callback_query

    print("---------------->something here <-----------------------------")

    await query.answer()
    await query.message.delete()
    
    await query.message.reply_text(
        "Enter the title of the book",
        reply_markup=ReplyKeyboardRemove()
    )

    return SELL_TITLE

async def sell_title(update: Update, context: CallbackContext) -> int:
    """Store the book title and ask for the author."""
    print("arrived here")
    context.user_data['sell_title'] = update.message.text

    await update.message.reply_text(
        "Enter the author of the book",
        reply_markup=ReplyKeyboardRemove()
    )
    return SELL_AUTHOR

async def sell_author(update: Update, context: CallbackContext) -> int:
    """Store the author and ask for the user's name."""

    context.user_data['sell_author'] = update.message.text
    await update.message.reply_text("when is the edition of the book", reply_markup=ReplyKeyboardRemove())
    return SELL_EDITION

async def sell_edition(update: Update, context: CallbackContext) -> int:
    """Store the user's edition and ask for the price."""
    context.user_data['sell_edition'] = update.message.text
    await update.message.reply_text("Enter the price of the book", reply_markup=ReplyKeyboardRemove())
    return SELL_PRICE

async def sell_price(update: Update, context: CallbackContext) -> int:
    """Store the user's price and ask for the status"""
    context.user_data['sell_price'] = update.message.text
    await update.message.reply_text("Enter the status of the book new/used \n if used speciy how long it's used", reply_markup=ReplyKeyboardRemove())
    return SELL_STATUS

async def sell_status(update: Update, context: CallbackContext) -> int:
    """Store the user's status and ask for the overview"""
    context.user_data['sell_status'] = update.message.text
    await update.message.reply_text("write overivew", reply_markup=ReplyKeyboardRemove())
    return SELL_OVERVIEW

async def sell_overview(update: Update, context: CallbackContext) -> int:
    """Store the user's overview and ask for name"""
    context.user_data['sell_overview'] = update.message.text
    await update.message.reply_text("Enter your full name", reply_markup=ReplyKeyboardRemove())
    return SELL_NAME

async def sell_name(update: Update, context: CallbackContext) -> int:
    """Store the user's overview and ask for the name."""
    context.user_data['sell_name'] = update.message.text
    await update.message.reply_text("phone", reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Share your phone", request_contact=True)
                ]
            ], resize_keyboard=True
        ))
    return SELL_PHONE

async def sell_phone(update: Update, context: CallbackContext) -> int:
    """Store the phone number and finish the sell process."""
    context.user_data['sell_phone'] = update.message.contact.phone_number
    
    #TODO: connection with backkend
    # connect it to the back end here --------> connection with backend <----------------
    
    sell_data = {
        'Title': context.user_data['sell_title'],
        'Author': context.user_data['sell_author'],
        'UserName': context.user_data['sell_name'] + ' - ' +  update.message.from_user.username,
        'PhoneNumber': context.user_data['sell_phone'],
        'Overview': context.user_data['sell_overview'],
        'Edition' : context.user_data['sell_edition'],
        'Status' : context.user_data['sell_status'],
        'Price': context.user_data['sell_price'],
        'Type' : 'Sell'
    }

    print("Hello there")
    reponse = post_books(sell_data)
    print(f"--------------->{reponse}<--------------")
    await update.message.reply_text(reponse, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the conversation."""
    await update.message.reply_text('sell cancelled.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
