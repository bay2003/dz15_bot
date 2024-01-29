from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
import logging

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Определяем этапы разговора
NAME, TEST = range(2)

# Список вопросов и правильных ответов
questions = [
    "*Что такое G-код в контексте ЧПУ станков?*\n\n"
    "(1) Язык программирования для графического дизайна\n"
    "(2) Стандартный язык программирования для управления движением станка\n"
    "(3) Программное обеспечение для моделирования ЧПУ станков\n"
    "(4) Тип сетевого протокола для ЧПУ машин",

    "*Какое утверждение лучше всего описывает процесс обработки на ЧПУ станке?*\n\n"
    "(1) Это автоматический процесс, не требующий вмешательства оператора\n"
    "(2) Это процесс, который полностью зависит от ручного управления оператором\n"
    "(3) Это процесс, где машина управляется посредством программ, но требует контроля и корректировки оператором\n"
    "(4) Это процесс, при котором оператор управляет машиной с помощью джойстика",

    "*Какие материалы чаще всего обрабатываются на ЧПУ станках?*\n\n"
    "(1) Только металлы, такие как сталь и алюминий\n"
    "(2) Только дерево\n"
    "(3) Разнообразные материалы, включая металлы, пластмассы и дерево\n"
    "(4) Только синтетические материалы, такие как пластмассы",

    "*Для чего используется функция 'G28' в G-коде?*\n\n"
    "(1) Для перемещения инструмента в заданное положение\n"
    "(2) Для возврата инструмента в начальное положение\n"
    "(3) Для изменения скорости резания\n"
    "(4) Для активации вращения шпинделя",

    "*Какова основная функция охлаждающей жидкости в процессе обработки на ЧПУ станке?*\n\n"
    "(1) Уменьшение трения между инструментом и заготовкой\n"
    "(2) Улучшение точности обработки\n"
    "(3) Предотвращение нагрева инструмента и заготовки\n"
    "(4) Увеличение скорости обработки",

    "*Если ЧПУ станок внезапно останавливается во время операции, какие первые шаги должен предпринять оператор?*\n\n"
    "(1) Перезагрузить станок и начать операцию заново\n"
    "(2) Проверить код на наличие ошибок и систему управления на предмет сбоев\n"
    "(3) Вызвать технического специалиста\n"
    "(4) Проверить электропитание и механические компоненты станка\n"
    "(5) Проверить инструмент на предмет износа или повреждения и убедиться, что нет застрявших обломков"
]

correct_answers = [2, 3, 3, 2, 3, 2]  # Правильные ответы

# Словарь для хранения ответов пользователей
user_data = {}

def start(update, context):
    update.message.reply_text('Привет! Как Вас зовут?')
    return NAME

# Получение имени пользователя и начало теста
def name(update, context):
    user_name = update.message.text
    user_data[update.message.chat_id] = {'name': user_name, 'answers': [], 'current_question': 0}
    update.message.reply_text(f"Привет, {user_name}! Давайте начнем тест.")
    return ask_question(update, context)

# Задать вопрос
def ask_question(update, context):
    chat_id = update.message.chat_id
    question_index = user_data[chat_id]['current_question']
    if question_index < len(questions):
        update.message.reply_text(questions[question_index], parse_mode='Markdown')
        return TEST
    else:
        return calculate_result(update, context)

# Получение ответа на вопрос и переход к следующему вопросу
def test(update, context):
    chat_id = update.message.chat_id
    answer = update.message.text
    try:
        user_data[chat_id]['answers'].append(int(answer))
        user_data[chat_id]['current_question'] += 1
        return ask_question(update, context)
    except ValueError:
        update.message.reply_text('Пожалуйста, введите номер ответа.')
        return TEST

# Подсчет результатов
def calculate_result(update, context):
    chat_id = update.message.chat_id
    score = sum(1 for i, answer in enumerate(user_data[chat_id]['answers']) if answer == correct_answers[i])
    update.message.reply_text(f"{user_data[chat_id]['name']}, вы завершили тест. Ваш результат: {score} из {len(questions)}")
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater("МОЙ ТОКЕН", use_context=True)

    # Получаем диспетчера для регистрации обработчиков
    dp = updater.dispatcher

    # Определяем обработчик разговоров с состояниями NAME и TEST
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            TEST: [MessageHandler(Filters.text, test)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)

    # Логирование ошибок
    dp.add_error_handler(error)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
# Здесь я использовал для работы https://t.me/Skills_of_the_Future_bot, токен можно использовать любой

