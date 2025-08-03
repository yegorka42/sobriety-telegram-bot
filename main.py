import os
import telebot
from datetime import datetime, timedelta
import json

# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("Ошибка: BOT_TOKEN не найден в переменных окружения")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# Словарь для хранения данных пользователей (в реальном проекте лучше использовать базу данных)
user_data = {}

def save_user_data():
    """Сохранение данных пользователей (в реальном проекте - в БД)"""
    try:
        with open('user_data.json', 'w', encoding='utf-8') as f:
            # Преобразуем datetime в строки для JSON
            data_to_save = {}
            for user_id, data in user_data.items():
                data_to_save[user_id] = data.copy()
                if 'sobriety_start' in data_to_save[user_id]:
                    data_to_save[user_id]['sobriety_start'] = data_to_save[user_id]['sobriety_start'].isoformat()
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")

def load_user_data():
    """Загрузка данных пользователей"""
    global user_data
    try:
        with open('user_data.json', 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            # Преобразуем строки обратно в datetime
            for user_id, data in loaded_data.items():
                if 'sobriety_start' in data:
                    data['sobriety_start'] = datetime.fromisoformat(data['sobriety_start'])
                user_data[user_id] = data
    except FileNotFoundError:
        user_data = {}
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        user_data = {}

def get_sobriety_days(user_id):
    """Получить количество дней трезвости"""
    if user_id not in user_data or 'sobriety_start' not in user_data[user_id]:
        return 0
    
    start_date = user_data[user_id]['sobriety_start']
    return (datetime.now() - start_date).days

def format_sobriety_message(days):
    """Форматирование сообщения о трезвости"""
    if days == 0:
        return "🎯 Сегодня ваш первый день! Вы можете это сделать!"
    elif days == 1:
        return "🌟 Поздравляю! У вас 1 день трезвости!"
    elif days < 7:
        return f"💪 Отлично! У вас {days} дней трезвости!"
    elif days < 30:
        weeks = days // 7
        remaining_days = days % 7
        if remaining_days == 0:
            return f"🏆 Превосходно! У вас {weeks} недель{'а' if weeks < 5 else ''} трезвости!"
        else:
            return f"🏆 Превосходно! У вас {weeks} недель{'а' if weeks < 5 else ''} и {remaining_days} дней трезвости!"
    elif days < 365:
        months = days // 30
        remaining_days = days % 30
        if remaining_days == 0:
            return f"🎊 Невероятно! У вас {months} месяц{'а' if months < 5 else 'ев'} трезвости!"
        else:
            return f"🎊 Невероятно! У вас {months} месяц{'а' if months < 5 else 'ев'} и {remaining_days} дней трезвости!"
    else:
        years = days // 365
        remaining_days = days % 365
        return f"🏅 Легенда! У вас {years} год{'а' if years < 5 else ''} и {remaining_days} дней трезвости!"

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = str(message.from_user.id)
    username = message.from_user.first_name or "Друг"
    
    welcome_text = f"""
🌟 Привет, {username}! 

Я бот для поддержки трезвости. Вместе мы сможем отслеживать ваш прогресс и поддерживать мотивацию!

📋 Доступные команды:
/start - начать работу с ботом
/setdate - установить дату начала трезвости
/status - узнать текущий статус
/motivation - получить мотивационное сообщение
/tips - полезные советы
/help - помощь

💪 Каждый день трезвости - это победа! Давайте начнем ваш путь к здоровой жизни.
"""
    
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['setdate'])
def set_date_command(message):
    user_id = str(message.from_user.id)
    
    # Устанавливаем сегодняшнюю дату как начало трезвости
    if user_id not in user_data:
        user_data[user_id] = {}
    
    user_data[user_id]['sobriety_start'] = datetime.now()
    save_user_data()
    
    response = """
🎯 Отлично! Сегодня официально начинается ваш путь к трезвости!

📅 Дата начала: сегодня
🌱 Каждый день будет считаться как новая победа!

Используйте /status чтобы проверить свой прогресс.
💪 Вы можете это сделать!
"""
    
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['status'])
def status_command(message):
    user_id = str(message.from_user.id)
    
    if user_id not in user_data or 'sobriety_start' not in user_data[user_id]:
        bot.send_message(message.chat.id, 
                        "📋 Сначала установите дату начала трезвости командой /setdate")
        return
    
    days = get_sobriety_days(user_id)
    status_message = format_sobriety_message(days)
    
    # Добавляем дополнительную информацию
    start_date = user_data[user_id]['sobriety_start'].strftime("%d.%m.%Y")
    
    full_message = f"""
{status_message}

📅 Дата начала: {start_date}
📊 Всего дней: {days}

{get_milestone_message(days)}
"""
    
    bot.send_message(message.chat.id, full_message)

def get_milestone_message(days):
    """Получить сообщение о достижении вехи"""
    if days == 7:
        return "🎉 Поздравляю с первой неделей! Это важная веха!"
    elif days == 30:
        return "🎊 Месяц трезвости! Вы на правильном пути!"
    elif days == 90:
        return "🏆 Три месяца! Ваша сила воли впечатляет!"
    elif days == 365:
        return "🏅 ГОД ТРЕЗВОСТИ! Вы настоящий герой!"
    elif days % 100 == 0 and days > 0:
        return f"🌟 {days} дней - круглая дата! Продолжайте в том же духе!"
    else:
        return "💪 Продолжайте двигаться вперед! Каждый день важен!"

@bot.message_handler(commands=['motivation'])
def motivation_command(message):
    motivational_quotes = [
        "💪 'Трезвость - это не лишение себя чего-то, а обретение всего.' - Неизвестный автор",
        "🌟 'Каждый день трезвости - это день, когда вы выбираете себя.' - Неизвестный автор",
        "🏆 'Сильные люди не избегают трудностей, они их преодолевают.'",
        "🌱 'Изменения начинаются с одного решения, принятого в один момент.'",
        "⭐ 'Вы сильнее, чем думаете, и способны на большее, чем можете представить.'",
        "🎯 'Каждый новый день - это новая возможность стать лучше.'",
        "💎 'Ваша жизнь стоит всех усилий, которые вы в неё вкладываете.'",
        "🚀 'Трезвость - это свобода быть собой без искажений.'"
    ]
    
    import random
    quote = random.choice(motivational_quotes)
    
    bot.send_message(message.chat.id, f"🌈 Мотивация дня:\n\n{quote}")

@bot.message_handler(commands=['tips'])
def tips_command(message):
    tips = """
💡 Полезные советы для поддержания трезвости:

🏃‍♂️ Физическая активность:
• Регулярные прогулки на свежем воздухе
• Занятия спортом или йогой
• Дыхательные упражнения

🧠 Ментальное здоровье:
• Медитация и осознанность
• Ведение дневника эмоций
• Изучение новых навыков

👥 Социальная поддержка:
• Общение с поддерживающими людьми
• Участие в группах поддержки
• Избегание триггерных ситуаций

🎯 Цели и хобби:
• Постановка новых целей
• Развитие творческих способностей
• Волонтерство и помощь другим

💤 Здоровый образ жизни:
• Регулярный сон (7-9 часов)
• Здоровое питание
• Достаточное количество воды

Используйте /motivation для ежедневной поддержки! 💪
"""
    
    bot.send_message(message.chat.id, tips)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
🤖 Помощь по командам бота:

/start - запустить бота и получить приветствие
/setdate - установить сегодня как начало трезвости
/status - узнать количество дней трезвости
/motivation - получить мотивационную цитату
/tips - полезные советы для поддержания трезвости
/help - показать это сообщение

📝 Как использовать бота:
1. Начните с команды /setdate
2. Каждый день проверяйте /status
3. Используйте /motivation когда нужна поддержка
4. Читайте /tips для полезных советов

💬 Также вы можете просто писать мне сообщения - я отвечу с поддержкой!

🆘 Если нужна профессиональная помощь, обратитесь к специалистам по зависимостям.
"""
    
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    """Обработка всех остальных сообщений"""
    user_id = str(message.from_user.id)
    
    # Простые ответы на ключевые слова
    text = message.text.lower()
    
    if any(word in text for word in ['помощь', 'плохо', 'тяжело', 'срыв', 'хочу выпить']):
        response = """
🤗 Я понимаю, что сейчас может быть трудно. Помните:

💪 Вы уже проделали огромную работу
🌟 Каждый момент трезвости ценен
🎯 Эти чувства временны и пройдут

Попробуйте:
• Глубоко подышать 5 минут
• Выпить стакан воды
• Позвонить другу или близкому
• Сделать небольшую прогулку

Используйте /motivation для вдохновения или /tips для практических советов.

🆘 Если нужна профессиональная помощь, не стесняйтесь обратиться к специалисту.
"""
    elif any(word in text for word in ['спасибо', 'благодарю', 'благодарность']):
        response = "🌟 Пожалуйста! Я рад помочь вам на этом пути. Вы делаете важную работу! 💪"
    elif any(word in text for word in ['как дела', 'привет', 'здравствуй']):
        response = f"Привет! 👋 Как ваши дела с трезвостью? Проверьте свой статус командой /status или получите мотивацию - /motivation"
    else:
        response = """
💬 Спасибо за сообщение! 

Я здесь, чтобы поддержать вас на пути к трезвости. Используйте:
• /status - узнать свой прогресс
• /motivation - получить поддержку
• /tips - полезные советы
• /help - все команды

💪 Помните: каждый день трезвости - это победа!
"""
    
    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
    print("🤖 Бот для поддержки трезвости запущен...")
    
    # Загружаем данные пользователей при запуске
    load_user_data()
    
    # Запускаем бота
    try:
        bot.infinity_polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"Ошибка: {e}")
        # Сохраняем данные при завершении
        save_user_data()
