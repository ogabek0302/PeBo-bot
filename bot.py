import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from scraper import get_product_prices
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)



def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Salom!✋ \n Men PeBo🤖, narx solishtiruvchi botman. Iltimos, narxini solishtirmoqchi bo'lgan mahsulot nomini yuboring.")


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Iltimos, menga narxlarni taqqoslamoqchi bo'lgan mahsulot nomini yuboring.")


def echo(update, context):
    user_id = update.effective_chat.id
    user_message = update.message.text
    prices = get_product_prices(user_message)

    message = f'Prices for {user_message}:\n\n'
    for site, price in prices.items():
        message += f'{site}: {price}\n'

    context.bot.send_message(chat_id=user_id, text=message)

    app.extra['user_info'][user_id] = {'user_message': user_message, 'prices': prices}


# def error(update, context):
#     logger.warning(f'Update {update} caused error {context.error}')


def main():
    app = FastAPI()
    app.extra['user_info'] = {}

    templates = Jinja2Templates(directory='templates')

    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request, "user_info": app.extra['user_info']})
            
    updater = Updater(token='6079475096:AAFxUxmmWEHpDy07n-YYj2PiaAL81eoiMes', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    message_handler = MessageHandler(filters.text & ~filters.command, echo)
    # error_handler = MessageHandler(filters.all, error)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(message_handler)
    # dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



if __name__ == '__main__':
    main()
