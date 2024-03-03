import telebot
import requests
from config import token, chat_id, message_reply_id, group
from datetime import datetime

bot = telebot.TeleBot(token)

days = {
    '0' : 'Понедельник - день бездельник',
    '1' : 'Вторник - повторник',
    '2' : 'Среда - тамода',
    '3' : 'Четверг - все заботы я отверг',
    '4' : 'Пятница - пьяница',
    '5' : 'Суббота - не работа',
    '6' : 'Воскресенье - день веселья'
}

pairs = {
        '1' : '09:00 - 10:30',
        '2' : '10:40 - 12:10',
        '3' : '12:40 - 14:10',
        '4' : '14:20 - 15:50',
        '5' : '16:20 - 17:50',
        '6' : '18:00 - 19:30',
        '7' : '19:40 - 21:10'
    }

types = {
    'ЛК' : 'Лекция(прогуливаем)',
    'ПР' : 'Практика',
    'ЛАБ': 'Лабораторная работа'
}

def get_current_week_number():
    current_date = datetime.now()
    start_date = datetime(year=current_date.year, month=2, day=5)
    delta = current_date - start_date
    week_number = delta.days // 7 + 1
    return week_number


def get_me_schedule(week, group):
    try:
        response = requests.get('https://group-hw.ru/api/getSchedule', params = {'type': 'students','week': week,'param': group,'token': 'null'})
        return response.json()
    except:
        return None    
    
def send_message(chat_id, message, message_reply_id):
    bot.send_message(chat_id, message, reply_to_message_id=message_reply_id)


def main():
    schedule = get_me_schedule(get_current_week_number(), group)
    if schedule:
        days_schedule = schedule['response']['items']['lessons']
        for day, lessons in days_schedule.items():
            day_name = days.get(day, "Неизвестный день")
            daily_schedule_message = f"{day_name}:\n\n"
            if lessons: 
                for lesson_num, lesson_info in lessons.items():
                    pair_time = pairs.get(lesson_num, "Неизвестное время")
                    title = lesson_info['title']
                    cab = lesson_info['cab']
                    prep = lesson_info['prep']
                    type_of_lesson = types.get(lesson_info['type'], lesson_info['type'])
                    daily_schedule_message += f"{pair_time}\n{title},\n{cab}, {prep},\n{type_of_lesson}\n\n"
            else:
                daily_schedule_message += "Ура! Пар нет. 🎉🎊🥳\n"
            send_message(chat_id, daily_schedule_message, message_reply_id)
    else:
        send_message(chat_id, "Не удалось получить расписание.", message_reply_id)

if __name__ == '__main__':
    main()