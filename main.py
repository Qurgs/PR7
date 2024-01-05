
import telebot
from telebot import types
from datetime import datetime

TOKEN = '6867522737:AAGJZ_SF2csWu4Fkskjl4u45F9UX53jqSr0'
bot = telebot.TeleBot(TOKEN)
users = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Для начала работы введите свой ID:")
    bot.register_next_step_handler(message, get_user_id)

@bot.message_handler(commands=['MAINreport'])
def handle_main_report(message):
    chat_id = message.chat.id
    sorted_users = sorted(users.values(), key=lambda x: x.get('referral_id', ''))

    if not sorted_users:
        bot.send_message(chat_id, "Нет информации о пользователях.")
        return

    report_text = ""
    for user_info in sorted_users:
        user_id = user_info.get('id', 'N/A')
        name = user_info.get('name', 'N/A')
        surname = user_info.get('surname', 'N/A')
        tasks_by_date = user_info.get('tasks_by_date', {})
        salary_destination = user_info.get('salary_destination', 'N/A')
        referral_id = user_info.get('referral_id', 'N/A')

        report_text += f"ID: {user_id}\nИмя: {name}\nФамилия: {surname}\n"

        if tasks_by_date:
            report_text += "Задания выполнены:\n"
            for task_date, task_count in tasks_by_date.items():
                report_text += f"Дата: {task_date.strftime('%Y-%m-%d')}, Количество: {task_count}\n"
        else:
            report_text += "Задания выполнены: 0\n"

        report_text += f"Способ получения зарплаты: {salary_destination}\nID реферала: {referral_id}\n\n"

    bot.send_message(chat_id, report_text)

@bot.message_handler(commands=['currentdate'])
def handle_current_date(message):
    chat_id = message.chat.id
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot.send_message(chat_id, f"Текущая дата и время: {current_date}")

@bot.message_handler(commands=['tasksfordate'])
def handle_tasks_for_date(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите дату для отчета (в формате ГГГГ-ММ-ДД):")
    bot.register_next_step_handler(message, get_report_date)

def get_report_date(message):
    chat_id = message.chat.id
    report_date_str = message.text

    try:
        report_date = datetime.strptime(report_date_str, "%Y-%m-%d")
    except ValueError:
        bot.send_message(chat_id, "Неверный формат даты. Пожалуйста, введите дату в правильном формате.")
        return

    users[chat_id].setdefault('tasks_by_date', {}).setdefault(report_date, 0)  # Устанавливаем значение по умолчанию
    users[chat_id]['current_report_date'] = report_date
    bot.send_message(chat_id, f"Сколько заданий вы выполнили для {report_date_str}?")
    bot.register_next_step_handler(message, get_task_count_for_date)

def get_task_count_for_date(message):
    chat_id = message.chat.id
    task_count = message.text

    if 'current_report_date' in users[chat_id]:
        report_date = users[chat_id]['current_report_date']

        # Сохраняем количество заданий для указанной даты
        users[chat_id].setdefault('tasks_by_date', {})[report_date] = int(task_count)

        bot.send_message(chat_id, f"Количество заданий для {report_date.strftime('%Y-%m-%d')} сохранено.")
    else:
        bot.send_message(chat_id, "Произошла ошибка. Пожалуйста, повторите попытку.")

def get_user_id(message):
    chat_id = message.chat.id
    user_id = message.text
    users[chat_id] = {'id': user_id}
    bot.send_message(chat_id, "Теперь введите свое имя:")
    bot.register_next_step_handler(message, get_user_name)

def get_user_name(message):
    chat_id = message.chat.id
    user_name = message.text
    users[chat_id]['name'] = user_name
    bot.send_message(chat_id, "Теперь введите свою фамилию:")
    bot.register_next_step_handler(message, get_user_surname)

def get_user_surname(message):
    chat_id = message.chat.id
    user_surname = message.text
    users[chat_id]['surname'] = user_surname
    bot.send_message(chat_id, "Куда вам скидывать зарплату?")
    bot.register_next_step_handler(message, get_salary_destination)

def get_salary_destination(message):
    chat_id = message.chat.id
    salary_destination = message.text
    users[chat_id]['salary_destination'] = salary_destination
    bot.send_message(chat_id, "Введите ID вашего реферала (если нет, оставьте пустым):")
    bot.register_next_step_handler(message, get_referral_id)

def get_referral_id(message):
    chat_id = message.chat.id
    referral_id = message.text
    users[chat_id]['referral_id'] = referral_id

    # Здесь вы можете сохранить информацию о пользователе в базе данных или выполнить другие действия

    bot.send_message(chat_id, "Спасибо! Ваша информация сохранена.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
