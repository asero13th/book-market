from telegram import Update, ReplyKeyboardRemove, CallbackQuery
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler,filters, ConversationHandler
from config import BOT_TOKEN
from handlers.start import start
from handlers.callback_handlers import handle_callback
from handlers.order_new_book import handle_new_order, order_title,  order_author,order_name,order_phone, cancel, NEW_ORDER_TITLE,NEW_ORDER_AUTHOR, NEW_ORDER_NAME, NEW_ORDER_PHONE
from handlers.buy_book import buy_this_book, buy_customer_address, buy_customer_name, buy_customer_phone,buy_process_book,buy_process_category, back,handle_buy_book, PROCESS_BUY_BOOK, PROCESS_BUY_CATEGORY, PROCESS_BUY_CUSTOMER_ADDRESS, PROCESS_BUY_CUSTOMER_NAME, PROCESS_BUY_CUSTOMER_PHONE, PROCESS_BUY_FINISH, PROCESS_BUY_THIS_BOOK
from handlers.rent_book import rent_customer_name, rent_customer_phone, rent_process_book, rent_process_category, rent_this_book, rent_customer_address, PROCESS_RENT_BOOK, PROCESS_RENT_CATEGORY, PROCESS_RENT_CUSTOMER_ADDRESS, PROCESS_RENT_CUSTOMER_NAME, PROCESS_RENT_CUSTOMER_PHONE, PROCESS_RENT_FINISH, PROCESS_RENT_THIS_BOOK
from handlers.sell_book import sell_author, sell_edition, sell_name,sell_overview,sell_phone,sell_price,sell_status,sell_title,SELL_AUTHOR,SELL_EDITION,SELL_NAME,SELL_OVERVIEW,SELL_PHONE,SELL_PRICE,SELL_STATUS,SELL_TITLE,handle_sell
from handlers.my_callback import MyCallback


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ------------> Order new book conversation handler <------------------------------
    order_new_book_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_new_order, pattern=MyCallback(name="order_book", id="4").pack())],
        states={
            NEW_ORDER_TITLE: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, order_title)],
            NEW_ORDER_AUTHOR: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, order_author)],
            NEW_ORDER_NAME: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, order_name)],
            NEW_ORDER_PHONE: [CommandHandler('cancel', cancel), MessageHandler(filters.CONTACT, order_phone)], 
        },
        fallbacks=[CommandHandler('cancel', cancel)],
       
    )

    # ------------> Buy book conversation handler <------------------------------
    buy_book_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_buy_book, pattern=MyCallback(name="buy_book", id="1").pack())],
        states={
            PROCESS_BUY_CATEGORY: [CommandHandler('back', back), CallbackQueryHandler(buy_process_category, pattern='^category_.*')],
            PROCESS_BUY_BOOK: [CommandHandler('back', back),  CallbackQueryHandler(buy_process_book, pattern='^book_.*')],
            PROCESS_BUY_THIS_BOOK: [CommandHandler('back', back),CallbackQueryHandler(buy_this_book, pattern='^buy_this_book.*')],
            PROCESS_BUY_CUSTOMER_NAME: [CommandHandler('back', back), MessageHandler(filters.ALL, buy_customer_name)],
            PROCESS_BUY_CUSTOMER_PHONE: [CommandHandler('back', back), MessageHandler(filters.ALL, buy_customer_phone)],
            PROCESS_BUY_CUSTOMER_ADDRESS: [CommandHandler('back', back), MessageHandler(filters.ALL, buy_customer_address)],
            PROCESS_BUY_FINISH: [CallbackQueryHandler(back, pattern='^back$')]
        },
         fallbacks=[CallbackQueryHandler(back, pattern='^category.*')]
    )

    rent_book_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_buy_book, pattern=MyCallback(name="rent_book", id="2").pack())],
        states={
            PROCESS_RENT_CATEGORY: [CommandHandler('back', back), CallbackQueryHandler(rent_process_category, pattern='^category_.*')],
            PROCESS_RENT_BOOK: [CommandHandler('back', back),  CallbackQueryHandler(rent_process_book, pattern='^book_.*')],
            PROCESS_RENT_THIS_BOOK: [CommandHandler('back', back),CallbackQueryHandler(rent_this_book, pattern='^rent_this_book.*')],
            PROCESS_RENT_CUSTOMER_NAME: [CommandHandler('back', back), MessageHandler(filters.ALL, rent_customer_name)],
            PROCESS_RENT_CUSTOMER_PHONE: [CommandHandler('back', back), MessageHandler(filters.ALL, rent_customer_phone)],
            PROCESS_RENT_CUSTOMER_ADDRESS: [CommandHandler('back', back), MessageHandler(filters.ALL, rent_customer_address)],
            PROCESS_RENT_FINISH: [CallbackQueryHandler(back, pattern='^back$')]
        },
         fallbacks=[CallbackQueryHandler(back, pattern='^category.*')]
    )

    sell_book_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_sell, pattern=MyCallback(name="sell_book", id="3").pack())],
        states={
            SELL_TITLE: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, sell_title)],
            SELL_AUTHOR: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, sell_author)],
            SELL_EDITION: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, sell_edition)],
            SELL_PRICE: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, sell_price)],
            SELL_STATUS: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, sell_status)],  
            SELL_OVERVIEW: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, sell_overview)], 
            SELL_NAME: [CommandHandler('cancel', cancel),MessageHandler(filters.TEXT, sell_name)], 
            SELL_PHONE: [CommandHandler('cancel', cancel), MessageHandler(filters.CONTACT, sell_phone)], 
        },
        fallbacks=[CommandHandler('cancel', cancel) ],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(order_new_book_conv_handler)
    app.add_handler(buy_book_conv_handler)
    app.add_handler(rent_book_conv_handler)
    app.add_handler(sell_book_conv_handler)

    app.run_polling()


if __name__ == "__main__" :
    main()