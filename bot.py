"""
Эхо-бот, который повторяет сообщения в Telegram.
Добавлена функция отправки картинки на слово "спасибо".
"""

import logging, os
from telegram import ForceReply, Update, InputFile
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from model import LLMService
import dotenv

# Загрузка переменных окружения
env = dotenv.dotenv_values(".env")

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

llm_service = LLMService()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение при команде /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот, который может отвечать на ваши сообщения.",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение при команде /help"""
    await update.message.reply_text(
        "Я умею:\n"
        "- Отвечать на ваши сообщения\n"
        "- Присылать приятную картинку, когда вы говорите 'спасибо'\n"
        "Просто напишите мне что-нибудь!"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает сообщения пользователя"""
    user_message = update.message.text
    
    # Проверяем на благодарность (регистронезависимо)
    if any(word in user_message.lower() for word in ["спасибо", "благодарю", "thanks"]):
        try:
            # Отправляем картинку из файла
            photo_path = os.path.join(os.path.dirname(__file__), "foto.jpeg")
            with open(photo_path, "rb") as photo:
                await update.message.reply_photo(
                    photo=InputFile(photo),
                    caption="Пожалуйста! 😊"
                )
            logger.info(f"User said thanks: {user_message}")
            return
        except FileNotFoundError:
            logger.error("Thanks image not found!")
            await update.message.reply_text("Спасибо вам! 😊 (картинка не найдена)")
            return
    
    # Обычный ответ ИИ
    llm_response = llm_service.chat(user_message)
    logger.info(f"User: {user_message}  LLM: {llm_response}")
    await update.message.reply_text(llm_response)

def main() -> None:
    """Запускает бота"""
    application = Application.builder().token(env["TELEGRAM_BOT_TOKEN"]).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()