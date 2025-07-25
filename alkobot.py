import telebot
from telebot import types
import json
import os
from datetime import datetime, timedelta
import random

# Токен вашего бота
BOT_TOKEN = "8084212728:AAGRNLAImnU4189WGA5E3-IO1Itq8WtGnD4"

bot = telebot.TeleBot(BOT_TOKEN)

# Файл для хранения данных пользователей
DATA_FILE = "users_data.json"

# Мотивационные цитаты
MOTIVATIONAL_QUOTES = [
    "Трезвость - это не отказ от жизни, это выбор настоящей жизни.",
    "Каждый трезвый день - это победа над собой.",
    "Ты сильнее, чем думаешь, и у тебя больше возможностей, чем кажется.",
    "Алкоголь не решает проблемы, он их создает.",
    "Трезвость открывает двери к настоящему счастью.",
    "Твоя жизнь слишком ценна, чтобы тратить ее на алкоголь.",
    "Каждый новый день трезвости - это шанс стать лучше.",
    "Сила воли растет с каждым днем трезвости.",
    "Ты не одинок в своей борьбе. Многие прошли этот путь.",
    "Трезвость - это свобода, а не ограничение.",
    "Твое тело и разум благодарят тебя за каждый трезвый день.",
    "Алкоголь крадет завтра ради сегодняшнего забвения.",
    "Трезвость дает ясность мысли и силу духа.",
    "Каждый день без алкоголя - это инвестиция в свое будущее.",
    "Ты можешь все, что угодно, но не можешь все сразу. Начни с трезвости.",
    "Трезвость - это не наказание, это награда.",
    "Твоя семья нуждается в трезвом тебе.",
    "Алкоголь - это иллюзия решения проблем.",
    "Трезвость делает тебя героем своей собственной истории.",
    "Каждый трезвый момент - это момент настоящей жизни.",
    "Ты заслуживаешь трезвой, полноценной жизни.",
    "Трезвость - это мужество быть собой.",
    "Алкоголь не даст тебе того, что ты ищешь.",
    "Трезвый разум - твое самое мощное оружие.",
    "Каждый день трезвости - это день, который ты не потеряешь.",
    "Трезвость открывает возможности, которых ты не видел раньше.",
    "Ты контролируешь свою жизнь, а не алкоголь.",
    "Трезвость - это путь к самоуважению.",
    "Каждый трезвый день делает тебя сильнее.",
    "Алкоголь - это вчерашний день, трезвость - это будущее.",
    "Трезвость позволяет тебе быть настоящим.",
    "Ты можешь быть гордым собой каждый трезвый день.",
    "Трезвость - это выбор сильных людей.",
    "Алкоголь не решит твои проблемы, но создаст новые.",
    "Трезвость дает тебе время для того, что действительно важно.",
    "Каждый трезвый день - это подарок себе.",
    "Ты достоин трезвой, счастливой жизни.",
    "Трезвость - это свобода от зависимости.",
    "Алкоголь - это ложный друг, трезвость - настоящий.",
    "Трезвость помогает тебе видеть красоту жизни.",
    "Каждый день без алкоголя - это день для роста.",
    "Трезвость - это уважение к себе и окружающим.",
    "Ты можешь преодолеть любые трудности трезвым.",
    "Трезвость - это ключ к настоящему успеху.",
    "Алкоголь крадет твои мечты, трезвость их возвращает."
]

# Стоп-предложения при желании выпить
STOP_SUGGESTIONS = [
    "Сделай 10 глубоких вдохов и выдохов. Это поможет успокоиться.",
    "Выпей стакан воды или чая. Часто жажда маскируется под другие потребности.",
    "Позвони другу или близкому человеку. Поделись своими чувствами.",
    "Выйди на прогулку. Свежий воздух поможет очистить мысли.",
    "Займись спортом: отжимания, приседания или растяжка.",
    "Послушай любимую музыку или подкаст.",
    "Прими душ или ванну. Вода помогает расслабиться.",
    "Вспомни, почему ты решил стать трезвым. Запиши эти причины.",
    "Займись хобби: рисование, чтение, игра на инструменте.",
    "Приготовь что-нибудь вкусное и полезное.",
    "Сделай уборку или займись домашними делами.",
    "Посмотри мотивационное видео или фильм.",
    "Помедитируй или займись йогой.",
    "Напиши в дневнике о своих чувствах.",
    "Вспомни, как хорошо ты себя чувствуешь трезвым утром.",
    "Подумай о своих целях и планах на будущее.",
    "Займись творчеством: рисуй, пиши, создавай.",
    "Поиграй в видеоигры или настольные игры.",
    "Посети спортзал или займись домашними тренировками.",
    "Приготовь себе вкусный безалкогольный коктейль.",
    "Почитай книгу или статью на интересную тему.",
    "Займись садоводством или уходом за растениями.",
    "Посмотри комедийное шоу или смешные видео.",
    "Сделай себе массаж или расслабляющие упражнения.",
    "Позвони в службу поддержки или на горячую линию.",
    "Вспомни о своих достижениях в трезвости.",
    "Займись планированием: составь список дел или целей.",
    "Поговори с зеркалом: скажи себе, что ты сильный.",
    "Займись волонтерством или помоги кому-то.",
    "Посети парк, музей или другое интересное место.",
    "Сделай дыхательную гимнастику или релаксацию.",
    "Вспомни о людях, которые в тебя верят.",
    "Займись изучением чего-то нового.",
    "Приготовь себе любимый безалкогольный напиток.",
    "Сделай фотографии или займись фотографией.",
    "Послушай аудиокнигу или подкаст.",
    "Займись рукоделием: вязание, шитье, лепка.",
    "Поиграй с домашними животными.",
    "Сделай генеральную уборку своего пространства.",
    "Посмотри документальный фильм или обучающее видео.",
    "Займись планированием путешествия или выходного дня.",
    "Напиши письмо или сообщение близкому человеку.",
    "Сделай растяжку или упражнения для расслабления.",
    "Вспомни о своих успехах и достижениях.",
    "Займись приготовлением здоровой пищи.",
    "Посети онлайн-группу поддержки или форум.",
    "Сделай что-то приятное для себя (но не связанное с алкоголем).",
    "Займись организацией своего времени и планов.",
    "Поговори с профессиональным консультантом.",
    "Вспомни, что это желание временно и пройдет.",
    "Займись любимым делом, которое требует концентрации.",
    "Подумай о том, как гордится тобой семья.",
    "Сделай список того, за что ты благодарен.",
    "Займись изучением новых рецептов безалкогольных напитков."
]


def load_user_data():
    """Загрузка данных пользователей из файла"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_user_data(data):
    """Сохранение данных пользователей в файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def get_user_sobriety_days(user_id):
    """Получение количества дней трезвости пользователя"""
    users_data = load_user_data()
    user_data = users_data.get(str(user_id), {})

    if 'sobriety_start_date' not in user_data:
        return 0

    start_date = datetime.fromisoformat(user_data['sobriety_start_date'])
    current_date = datetime.now()
    days_sober = (current_date - start_date).days
    return max(0, days_sober)


def set_sobriety_start_date(user_id, start_date=None):
    """Установка даты начала трезвости"""
    users_data = load_user_data()

    if str(user_id) not in users_data:
        users_data[str(user_id)] = {}

    if start_date is None:
        start_date = datetime.now()

    users_data[str(user_id)]['sobriety_start_date'] = start_date.isoformat()
    save_user_data(users_data)


def create_main_keyboard():
    """Создание основной клавиатуры с кнопками разделов"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn_motivation = types.KeyboardButton("🌟 Мотивация")
    btn_stop_help = types.KeyboardButton("🛑 Стоп! Помощь")
    btn_counter = types.KeyboardButton("📅 Счетчик дней")
    btn_reset_counter = types.KeyboardButton("🔄 Сбросить счетчик")
    btn_help = types.KeyboardButton("❓ Помощь")

    keyboard.add(btn_motivation, btn_stop_help)
    keyboard.add(btn_counter, btn_reset_counter)
    keyboard.add(btn_help)

    return keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    """Обработчик команды /start"""
    user_id = message.from_user.id

    # Проверяем, есть ли уже данные о пользователе
    users_data = load_user_data()
    if str(user_id) not in users_data:
        set_sobriety_start_date(user_id)

    welcome_text = f"""
Привет, {message.from_user.first_name}! 👋

Добро пожаловать в бота для мотивации трезвости! 🌟

Я здесь, чтобы поддержать тебя на пути к трезвой жизни. 

Мои возможности:
🌟 Мотивационные цитаты для вдохновения
🛑 Экстренная помощь при желании выпить
📅 Счетчик дней трезвости
🔄 Возможность сбросить счетчик

Выбери нужный раздел с помощью кнопок ниже:
"""

    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_keyboard())


@bot.message_handler(func=lambda message: message.text == "🌟 Мотивация")
def send_motivation(message):
    """Отправка мотивационной цитаты"""
    quote = random.choice(MOTIVATIONAL_QUOTES)
    bot.send_message(message.chat.id, f"🌟 {quote}")


@bot.message_handler(func=lambda message: message.text == "🛑 Стоп! Помощь")
def send_stop_help(message):
    """Отправка стоп-предложения"""
    suggestion = random.choice(STOP_SUGGESTIONS)
    help_text = f"""
🛑 СТОП! Ты можешь это преодолеть!

💪 Попробуй это:
{suggestion}

🤝 Помни: это чувство временно и пройдет. Ты сильнее, чем думаешь!

📞 Если нужна дополнительная помощь, обратись к близким или специалистам.
"""
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(func=lambda message: message.text == "📅 Счетчик дней")
def show_counter(message):
    """Показ счетчика дней трезвости"""
    user_id = message.from_user.id
    days_sober = get_user_sobriety_days(user_id)

    if days_sober == 0:
        counter_text = """
📅 Счетчик дней трезвости

🎯 Сегодня твой первый день! Или начни отсчет заново.

Каждый день - это новая возможность. Ты можешь это сделать! 💪
"""
    else:
        counter_text = f"""
📅 Счетчик дней трезвости

🎉 Поздравляю! Ты трезв уже {days_sober} дней!

{"🌟 Отличное начало!" if days_sober < 7 else
        "🔥 Первая неделя позади!" if days_sober < 30 else
        "💎 Целый месяц!" if days_sober < 90 else
        "🏆 Три месяца - это серьезно!" if days_sober < 365 else
        "👑 Год трезвости! Ты герой!"}

Продолжай в том же духе! 💪
"""

    bot.send_message(message.chat.id, counter_text)


@bot.message_handler(func=lambda message: message.text == "🔄 Сбросить счетчик")
def reset_counter(message):
    """Сброс счетчика дней трезвости"""
    user_id = message.from_user.id

    # Создаем inline клавиатуру для подтверждения
    keyboard = types.InlineKeyboardMarkup()
    btn_confirm = types.InlineKeyboardButton("✅ Да, сбросить", callback_data="reset_confirm")
    btn_cancel = types.InlineKeyboardButton("❌ Отмена", callback_data="reset_cancel")
    keyboard.add(btn_confirm, btn_cancel)

    bot.send_message(
        message.chat.id,
        "🔄 Ты уверен, что хочешь сбросить счетчик дней трезвости?",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == "reset_confirm")
def confirm_reset(call):
    """Подтверждение сброса счетчика"""
    user_id = call.from_user.id
    set_sobriety_start_date(user_id)

    bot.edit_message_text(
        "✅ Счетчик сброшен! Начинаем новый отсчет. Ты можешь это сделать! 💪",
        call.message.chat.id,
        call.message.message_id
    )


@bot.callback_query_handler(func=lambda call: call.data == "reset_cancel")
def cancel_reset(call):
    """Отмена сброса счетчика"""
    bot.edit_message_text(
        "❌ Сброс отменен. Продолжай идти к своей цели! 🌟",
        call.message.chat.id,
        call.message.message_id
    )


@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def show_help(message):
    """Показ справки"""
    help_text = """
❓ Справка по боту

Этот бот создан для поддержки людей, выбравших трезвый образ жизни.

🌟 Мотивация - получи вдохновляющую цитату
🛑 Стоп! Помощь - экстренная помощь при желании выпить
📅 Счетчик дней - узнай, сколько дней ты трезв
🔄 Сбросить счетчик - начать отсчет заново

📞 Помни: если тебе нужна профессиональная помощь, обратись к специалистам.

💪 Ты не одинок в этом пути. Каждый день трезвости - это твоя победа!
"""
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(func=lambda message: True)
def default_message(message):
    """Обработчик всех остальных сообщений"""
    bot.send_message(
        message.chat.id,
        "Используй кнопки меню для навигации по боту. Если кнопки не видны, введи /start",
        reply_markup=create_main_keyboard()
    )


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)