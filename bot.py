import settings
import requests

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardButton, InlineKeyboardMarkup, replymarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

empty = "⠀"
def category_command(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(text="Бакалея", callback_data="1")],
        [InlineKeyboardButton(text="Напитки", callback_data="1")],
        [InlineKeyboardButton(text="Молочные товары", callback_data="1")],
        [InlineKeyboardButton(text=" ", callback_data="empty")],
        [InlineKeyboardButton(text="Пошук", switch_inline_query_current_chat="")]
    ]
    update.message.reply_text(text="Категорії", reply_markup=InlineKeyboardMarkup(keyboard))

def inline(update: Update, context: CallbackContext):
    query = update.inline_query.query
    categories = requests.get(settings.SEARCH_CATEGORY + (query or ""), headers={"authorization": "Bearer " + settings.ACCESS_TOKEN}).json()

    result = [
        InlineQueryResultArticle(
            id=category["id"],
            title=category["title"],
            input_message_content=InputTextMessageContent(f"Ви вибрали {category['title']}"),
        )
        for category in categories["results"]
        if query.lower() in category["title"].lower()
    ]
    if len(result) > 50:
        result = result[:50]
    elif not result:
        result = [InlineQueryResultArticle(
            id=0,
            title="Результат відсутній",
            input_message_content=InputTextMessageContent("Пусто"),
        )]
    update.inline_query.answer(result)

def main() -> None:
    updater = Updater(settings.TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("c", category_command))
    dispatcher.add_handler(InlineQueryHandler(inline))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
