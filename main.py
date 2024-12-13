from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import executor
import asyncio
import random
import logging

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Списки для идей
GIFT_IDEAS = [
    "Подарочный сертификат в любимый магазин. Совет: выбирайте сертификаты универсальных магазинов, чтобы получатель мог выбрать то, что ему действительно нужно. https://www.sportmaster.ru/catalog/podarochnye_karty_/?utm_referrer=https%3A%2F%2Fwww.google.com%2F",
    "Теплый плед с новогодним рисунком. Пример такого пледа: https://www.wildberries.ru/catalog/163712042/detail.aspx?targetUrl=SN",
    "Набор ароматических свечей. Пример набора: https://www.wildberries.ru/catalog/272184043/detail.aspx?targetUrl=SN",
    "Книга любимого автора. Пример книги: https://www.wildberries.ru/catalog/123556275/detail.aspx?targetUrl=SN",
    "Подарочная корзина с фруктами и сладостями. Пример корзины: https://www.wildberries.ru/catalog/188408946/detail.aspx?targetUrl=SN",
    "Настольная игра для вечеров с семьей. Пример игры: https://www.wildberries.ru/catalog/257359538/detail.aspx?targetUrl=SN",
    "Персонализированный ежедневник или блокнот. Пример ежедневника: https://www.wildberries.ru/catalog/6917131/detail.aspx?targetUrl=SN"
]

RECIPES = [
    "Рецепт оливье: \nИнгредиенты:\n- Картофель: 4 шт.\n- Морковь: 1 шт.\n- Яйца: 4 шт.\n- Зеленый горошек: 200 г\n- Вареная колбаса: 300 г\n- Майонез: по вкусу.\nИнструкция: \n1. Отварите картофель, морковь и яйца. Остудите и очистите.\n2. Нарежьте все ингредиенты кубиками.\n3. Добавьте зеленый горошек и заправьте майонезом.\n4. Тщательно перемешайте и подавайте охлажденным. Вот подробный рецепт из интернета: https://www.gastronom.ru/recipe/10803/salat-olive-klassicheskij-sovetskij",
    "Рецепт глинтвейна: \nИнгредиенты:\n- Красное вино: 1,5 л\n- Корица: 1 палочка\n- Гвоздика: 3 шт.\n- Апельсин или лимон: 1 шт.\n- Мед по вкусу: 2 ст. л.\nИнструкция: \n1. В кастрюлю налейте вино, добавьте корицу и гвоздику.\n2. Нарежьте апельсин кружочками и положите в кастрюлю.\n3. Нагрейте смесь, не доводя до кипения.\n4. Добавьте мед и перемешайте. Вот подробный рецепт из интернета: https://www.russianfood.com/recipes/recipe.php?rid=68671",
    "Рецепт запеченного гуся: \nИнгредиенты:\n- Гусь: 1 шт.\n- Яблоки: 5 шт.\n- Мед: 3 ст. л.\n- Горчица: 2 ст. л.\n- Специи: по вкусу.\nИнструкция: \n1. Очистите гуся, натрите специями.\n2. Нарежьте яблоки крупными кусками и нафаршируйте ими гуся.\n3. Смешайте мед и горчицу, смажьте гуся сверху.\n4. Запекайте в духовке при 180°C около 2-3 часов. Вот примерный рецепт из интернета: https://www.gastronom.ru/text/gus-zapechennyj-v-duhovke-1003555",
    "Рецепт тирамису: \nИнгредиенты:\n- Печенье савоярди: 200 г\n- Маскарпоне: 500 г\n- Яйца: 4 шт.\n- Кофе эспрессо: 300 мл\n- Какао: для посыпки.\nИнструкция: \n1. Заварите крепкий кофе и дайте ему остыть.\n2. Разделите белки и желтки. Взбейте желтки с сахаром, затем добавьте маскарпоне.\n3. Взбейте белки до устойчивых пиков и аккуратно вмешайте в крем.\n4. Окуните савоярди в кофе и уложите слой в форму. Вот подробный рецепт из интернета: https://www.edimdoma.ru/retsepty/45966-tiramisu-klassicheskiy"
]

TRADITIONS = [
    "В России принято загадывать желание под бой курантов. Напишите его на бумажке, сожгите и бросьте пепел в бокал с шампанским. Вот более подробно про данную традицию: https://ria.ru/20181231/1548546830.html",
    "В Италии в Новый год выбрасывают старые вещи из окон. Это символизирует прощание с прошлым и начало нового этапа жизни. Вот более подробно про данную традицию: https://trk7.ru/news/90721.html",
    "В Японии звонят в колокола 108 раз, чтобы избавиться от грехов. Это число соответствует человеческим порокам, которые нужно оставить в уходящем году.  Вот более подробно про данную традицию: https://japan-ego.livejournal.com/22794.html",
    "В Шотландии популярна традиция 'Первый гость': первый человек, переступивший порог в новом году, приносит удачу. Вот более подробно про данную традицию: https://dzen.ru/a/X81YQHAthFoTIwuk"
]

# Инициализация бота
BOT_TOKEN = "7826090291:AAESXxALZ_lFV1jE6YBWY3VRaI4r2c4F8pI"  # Замените на ваш токен
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Состояния пользователей
USER_STATE = {}

def create_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Идеи подарков", callback_data="gifts")],
            [InlineKeyboardButton("Рецепты", callback_data="recipes")],
            [InlineKeyboardButton("Традиции", callback_data="traditions")],
        ]
    )
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Инициализация состояния пользователя, если его нет
    user_id = message.from_user.id
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {'category': None, 'seen_categories': [], 'seen_items': {'gifts': [], 'recipes': [], 'traditions': []}}

    # Ответ и отображение кнопок
    await message.answer(
        "Привет! Я готов помочь выбрать идею для новогоднего ужина или подарка! Что тебя интересует?",
        reply_markup=create_main_keyboard()
    )

@dp.message_handler()
async def handle_messages(message: types.Message):
    user_text = message.text.strip().lower()

    # Инициализация состояния пользователя, если его нет
    user_id = message.from_user.id
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {'category': None, 'seen_categories': [], 'seen_items': {'gifts': [], 'recipes': [], 'traditions': []}}

    # Ответ на фразы типа "Как дела?", "Что нового?"
    if any(phrase in user_text for phrase in ["как дела", "что нового", "привет", "здравствуй"]):
        await message.reply("Привет! Я готов помочь выбрать идею для новогоднего ужина или подарка! Что тебя интересует?", reply_markup=create_main_keyboard())
        return

    response = "Простите, я не понял ваш запрос. Попробуйте выбрать один из вариантов выше или уточнить вопрос."

    # Проверка на отказ от предложенной идеи
    if any(phrase in user_text for phrase in ["не нравится", "не хочу", "убери", "не хочется"]):
        category = USER_STATE[user_id].get('category')

        if category == 'gifts':
            available_gifts = [gift for gift in GIFT_IDEAS if gift not in USER_STATE[user_id]['seen_items']['gifts']]
            if available_gifts:
                response = random.choice(available_gifts)
                USER_STATE[user_id]['seen_items']['gifts'].append(response)
            else:
                response = "У вас уже были все идеи для подарков. Пожалуйста, выберите новую категорию."
        elif category == 'recipes':
            available_recipes = [recipe for recipe in RECIPES if recipe not in USER_STATE[user_id]['seen_items']['recipes']]
            if available_recipes:
                response = random.choice(available_recipes)
                USER_STATE[user_id]['seen_items']['recipes'].append(response)
            else:
                response = "У вас уже были все рецепты. Пожалуйста, выберите новую категорию."
        elif category == 'traditions':
            available_traditions = [tradition for tradition in TRADITIONS if tradition not in USER_STATE[user_id]['seen_items']['traditions']]
            if available_traditions:
                response = random.choice(available_traditions)
                USER_STATE[user_id]['seen_items']['traditions'].append(response)
            else:
                response = "У вас уже были все традиции. Пожалуйста, выберите новую категорию."
        else:
            response = "Пожалуйста, выберите категорию, чтобы я мог предложить что-то другое."

    await message.reply(response)

@dp.callback_query_handler(lambda c: c.data == 'gifts')
async def handle_gift_selection(query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {'category': None, 'seen_categories': [], 'seen_items': {'gifts': [], 'recipes': [], 'traditions': []}}

    USER_STATE[user_id]['category'] = 'gifts'
    USER_STATE[user_id]['seen_categories'].append('gifts')

    # Отправляем новый подарок
    available_gifts = [gift for gift in GIFT_IDEAS if gift not in USER_STATE[user_id]['seen_items']['gifts']]
    if available_gifts:
        response = random.choice(available_gifts)
        USER_STATE[user_id]['seen_items']['gifts'].append(response)
    else:
        response = "У вас уже были все идеи для подарков. Пожалуйста, выберите новую категорию."

    await query.message.edit_text(f"Вот идея подарка: {response}")
    await query.message.answer("Пожалуйста, выберите следующую категорию:", reply_markup=create_main_keyboard())
    await query.answer()

@dp.callback_query_handler(lambda c: c.data == 'recipes')
async def handle_recipe_selection(query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {'category': None, 'seen_categories': [], 'seen_items': {'gifts': [], 'recipes': [], 'traditions': []}}

    USER_STATE[user_id]['category'] = 'recipes'
    USER_STATE[user_id]['seen_categories'].append('recipes')

    # Отправляем новый рецепт
    available_recipes = [recipe for recipe in RECIPES if recipe not in USER_STATE[user_id]['seen_items']['recipes']]
    if available_recipes:
        response = random.choice(available_recipes)
        USER_STATE[user_id]['seen_items']['recipes'].append(response)
    else:
        response = "У вас уже были все рецепты. Пожалуйста, выберите новую категорию."

    await query.message.edit_text(f"Вот рецепт: {response}")
    await query.message.answer("Пожалуйста, выберите следующую категорию:", reply_markup=create_main_keyboard())
    await query.answer()

@dp.callback_query_handler(lambda c: c.data == 'traditions')
async def handle_tradition_selection(query: CallbackQuery):
    user_id = query.from_user.id
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {'category': None, 'seen_categories': [], 'seen_items': {'gifts': [], 'recipes': [], 'traditions': []}}

    USER_STATE[user_id]['category'] = 'traditions'
    USER_STATE[user_id]['seen_categories'].append('traditions')

    # Отправляем новую традицию
    available_traditions = [tradition for tradition in TRADITIONS if tradition not in USER_STATE[user_id]['seen_items']['traditions']]
    if available_traditions:
        response = random.choice(available_traditions)
        USER_STATE[user_id]['seen_items']['traditions'].append(response)
    else:
        response = "У вас уже были все традиции. Пожалуйста, выберите новую категорию."

    await query.message.edit_text(f"Вот традиция: {response}")
    await query.message.answer("Пожалуйста, выберите следующую категорию:", reply_markup=create_main_keyboard())
    await query.answer()

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
