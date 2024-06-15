import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler, ConversationHandler, CallbackContext
from datetime import datetime

PROCESS_RENT_BOOK, PROCESS_RENT_CATEGORY, PROCESS_RENT_THIS_BOOK, PROCESS_RENT_CUSTOMER_NAME, PROCESS_RENT_CUSTOMER_PHONE, PROCESS_RENT_CUSTOMER_ADDRESS, PROCESS_RENT_FINISH = range(7)
def fetch_books():
    url = f"https://bookstore-theta-two.vercel.app/api/addbook"
    response =  requests.get(url)

    
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
   
    return None
def post_books(data):
    response = requests.post('https://bookstore-theta-two.vercel.app/api/orders', json=data)
    if response.status_code == 200:
        return("Order successfully sent")
    else:
        return("Failed to send order")

# ------------------> Books global variabl <------------------------
# ------------------> Books global variabl <------------------------

books = fetch_books()
ordered_book_id = ''
# ------------------> Books global variabl <------------------------
# ------------------> Books global variabl <------------------------

def get_book_by_id(books, book_id):
    for book in books:
        if book['_id'] == book_id:
            return book
    return None

async def handle_rent_book(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    await query.message.delete()

    keyboard = [
        [
            InlineKeyboardButton("Fiction", callback_data='category_Fiction'),
            InlineKeyboardButton("Educational", callback_data='category_Educational')
        ],
        [
            InlineKeyboardButton("Spiritual", callback_data='category_Spiritual'),
            InlineKeyboardButton("Philosophy", callback_data='category_Philosophy')
        ],
        [
            InlineKeyboardButton("Selfhelp", callback_data='category_Business'),
            InlineKeyboardButton("Business", callback_data='category_Others')
        ],
        [
            InlineKeyboardButton("View all books", callback_data='category_all_book')
        ],
        [
            InlineKeyboardButton("Back", callback_data='back')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text('Select the category of the book you want to RENT:', reply_markup=reply_markup)
    return PROCESS_RENT_CATEGORY

async def rent_process_category(update: Update, context: CallbackContext) -> int:
    print("<-------- arrived here <--------------")
    query = update.callback_query
    await query.answer()
    await query.message.delete()

    genre = query.data.split('_')[1]
    print(genre)
    # Fetch books from api
    if genre != "all":
        filtered_books = [book for book in books if book['Genere'] == genre and book["Type"] == "rent"]
    else:
        filtered_books = [book for book in books if book["Type"] == "Rent"]

    keyboard = []
    for i in range(0, len(filtered_books), 2):
        row = []
        row.append(InlineKeyboardButton(filtered_books[i]['Title'], callback_data=f'book_{filtered_books[i]["_id"]}'))
        if i+1 < len(filtered_books):
            row.append(InlineKeyboardButton(filtered_books[i+1]['Title'], callback_data=f'book_{filtered_books[i+1]["_id"]}'))
        keyboard.append(row)
    keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
    menu = InlineKeyboardMarkup(keyboard)
    
    if not filtered_books:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No such book with the genre.", reply_markup=menu)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Select the book you want to RENT:", reply_markup=menu)

    return PROCESS_RENT_BOOK

async def rent_process_book(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    book_id = query.data.split('_')[1]

    
    filtered_books = [book for book in books if book['_id'] == book_id]
    book = filtered_books[0]
    text = f'Title: {book["Title"]}\nAuthor: {book["Author"]}\nEdition: {book["Edition"]}\nPrice: {book["Price"]}\nStatus: {book["Status"]}\nOverview: {book["Overview"]}\nGenre: {book["Genere"]}\nContact: @SilentERr\nCall: +251953933492'
    keyboard = [
        [InlineKeyboardButton("rent this book", callback_data=f'rent_this_book_{book_id}')],
        [InlineKeyboardButton("Back", callback_data='back')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=text, reply_markup=reply_markup)
    return PROCESS_RENT_THIS_BOOK

async def rent_this_book(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    book_id = query.data.split('_')[3]
    print(f'--------->{book_id}<------------')
    context.user_data['book_id'] = book_id
   

    # Fetch book title from Firestore
    
    book = get_book_by_id(books, book_id)
    context.user_data['book_title'] = book["Title"]
    await query.edit_message_text(text="Enter your full name please:")
    return PROCESS_RENT_CUSTOMER_NAME

async def rent_customer_name(update: Update, context: CallbackContext) -> int:
    context.user_data['renter_name'] = update.message.text
    keyboard = [[KeyboardButton("Share your phone", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Enter your phone number:", reply_markup=reply_markup)
    return PROCESS_RENT_CUSTOMER_PHONE

async def rent_customer_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['renter_phone'] = update.message.contact.phone_number
    await update.message.reply_text("Enter your block and room number:", reply_markup=ReplyKeyboardRemove())
    return PROCESS_RENT_CUSTOMER_ADDRESS

async def rent_customer_address(update: Update, context: CallbackContext) -> int:

    context.user_data['renter_address'] = update.message.text
    filtered_books = [book for book in books if book['_id'] == context.user_data['book_id']]
    book = filtered_books[0]
    price = book['Price']

    new_order = {
        'Title': context.user_data['book_title'],
        'Price': price,
        'UserName': update.message.from_user.username,
        'PhoneNumber': context.user_data['renter_phone'],
        'Location': context.user_data['renter_address'],
        'Type': 'Rent',
        'Date': datetime.now().strftime('%Y-%m-%d')
    }

    reponse = post_books(new_order)
    await update.message.reply_text(reponse, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def back(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    # Get the list of states from the context
    states = context.user_data.get('states', [])

    if not states:
        # If there are no previous states, end the conversation
        await query.edit_message_text(text="No previous state, ending the conversation...")
        return ConversationHandler.END

    # Remove the last state from the list
    last_state = states.pop()
    context.user_data['states'] = states

    await query.edit_message_text(text="Going back to the previous state...")
    return last_state