from logic import *
from config import *
import sqlite3
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)
hideBoard = types.ReplyKeyboardRemove() 

QUIZ = [
    {
        "text": "Which type of challenge would you most enjoy solving?",
        "options": {
            "Designing a user-friendly app or website": {"IT": 1},
            "Writing a short story or creating a piece of art": {"Creativity": 1},
            "Helping someone overcome personal difficulties": {"Social": 1},
            "Diagnosing a health issue based on symptoms": {"Medicine": 1},
            "Fixing or building a mechanical device": {"Technical": 1}
        }
    },
    {
        "text": "What kind of school projects did you enjoy the most?",
        "options": {
            "Programming or building something digital": {"IT": 1},
            "Creative presentations or storytelling": {"Creativity": 1},
            "Group discussions and social issues": {"Social": 1},
            "Experiments in biology or chemistry": {"Medicine": 1},
            "Hands-on construction or engineering tasks": {"Technical": 1}
        }
    },
    {
        "text": "Which work style best describes you?",
        "options": {
            "Structured and analytical": {"IT": 1},
            "Expressive and imaginative": {"Creativity": 1},
            "Supportive and emotionally aware": {"Social": 1},
            "Careful and detail-focused": {"Medicine": 1},
            "Practical and task-oriented": {"Technical": 1}
        }
    },
    {
        "text": "You have a free weekend. What do you choose to do?",
        "options": {
            "Try coding something new or solve a puzzle": {"IT": 1},
            "Draw, write, or film something creative": {"Creativity": 1},
            "Volunteer or hang out with friends": {"Social": 1},
            "Read about health or science topics": {"Medicine": 1},
            "Fix something at home or build a DIY project": {"Technical": 1}
        }
    },
    {
        "text": "What environment do you see yourself working in?",
        "options": {
            "Remote office or tech company": {"IT": 1},
            "Creative studio or media agency": {"Creativity": 1},
            "School, center, or hospital with people": {"Social": 1},
            "Clinic, lab, or research institution": {"Medicine": 1},
            "Workshop, factory, or construction site": {"Technical": 1}
        }
    },
    {
        "text": "What motivates you the most?",
        "options": {
            "Solving complex logical problems": {"IT": 1},
            "Expressing ideas in unique ways": {"Creativity": 1},
            "Improving others’ lives and well-being": {"Social": 1},
            "Understanding how the human body works": {"Medicine": 1},
            "Creating or repairing something physical": {"Technical": 1}
        }
    },
    {
        "text": "What type of collaboration do you prefer?",
        "options": {
            "Working independently on technical tasks": {"IT": 1},
            "Brainstorming creative ideas with others": {"Creativity": 1},
            "Interacting and communicating with people": {"Social": 1},
            "Sharing knowledge to solve real-life problems": {"Medicine": 1},
            "Coordinating hands-on work in a team": {"Technical": 1}
        }
    },
    {
        "text": "What kind of content are you drawn to online?",
        "options": {
            "Tech trends, programming tutorials": {"IT": 1},
            "Art, design, or writing inspiration": {"Creativity": 1},
            "Mental health or communication skills": {"Social": 1},
            "Science documentaries, health advice": {"Medicine": 1},
            "Gadgets, tools, or DIY builds": {"Technical": 1}
        }
    },
    {
        "text": "If you could instantly gain expertise in one area, which would it be?",
        "options": {
            "Cybersecurity or AI": {"IT": 1},
            "Film direction or illustration": {"Creativity": 1},
            "Psychology or conflict resolution": {"Social": 1},
            "Surgery or disease treatment": {"Medicine": 1},
            "Automotive or robotics engineering": {"Technical": 1}
        }
    },
    {
        "text": "Which compliment would mean the most to you?",
        "options": {
            "“You’re incredibly logical and efficient.”": {"IT": 1},
            "“You’re full of original ideas.”": {"Creativity": 1},
            "“You really understand and care about people.”": {"Social": 1},
            "“You have excellent focus and precision.”": {"Medicine": 1},
            "“You’re a hands-on problem solver.”": {"Technical": 1}
        }
    }
]
categories = ["IT", "Creativity", "Social", "Medicine", "Technical"]

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Hello! I am here to help teenagers and young 
                     adults discover their ideal professions 
                     and receive personalized career advice. ) 
""")
    info(message)
    
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
"""
Here are the available commands you can use:

/start — Get started with the bot and see available options.
/quiz — Take a quiz to discover professions that match your interests.
/profession [name] — Get information about a specific profession (e.g., /profession designer).
/advice — Receive career advice and tips.
/goals — Set or review your career goals.
/faq — Browse frequently asked questions about careers.
/info — Display a list of all available commands.

""")
    



@bot.message_handler(commands=['quiz'])
def handle_quiz(message):
    bot.send_message(message.chat.id, "Let's start the quiz to discover your ideal profession!")
    user_id = message.from_user.id
    create_user_if_not_exists(user_id)
    send_question(user_id)

# Отправка вопроса
def send_question(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT step FROM users WHERE user_id = ?', (user_id,))
    step = c.fetchone()[0]
    conn.close()

    if step >= len(QUIZ):
        send_result(user_id)
        return

    q = QUIZ[step]
    markup = InlineKeyboardMarkup()
    for option_text, category in q['options'].items():
        btn = InlineKeyboardButton(text=option_text, callback_data=category)
        markup.add(btn)
    bot.send_message(user_id, q['text'], reply_markup=markup)

# Обработка выбора ответа
@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    user_id = call.from_user.id
    category = call.data

    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute(f'''
        UPDATE users
        SET {category} = {category} + 1,
            step = step + 1
        WHERE user_id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

    bot.answer_callback_query(call.id)
    send_question(user_id)

# Отправка результата
def send_result(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''
        SELECT IT, Creativity, Social, Medicine, Technical
        FROM users WHERE user_id = ?
    ''', (user_id,))
    scores = dict(zip(categories, c.fetchone()))
    conn.close()

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_category = top[0][0]
    result_text = f"✅ Based on your answers, your strongest direction is: *{top_category}*"
    bot.send_message(user_id, result_text, parse_mode="Markdown")

# Запуск
if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)

