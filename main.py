
from config import *
import sqlite3
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)
hideBoard = types.ReplyKeyboardRemove() 

QUIZ = [
    {
        "text": "1. Which type of challenge would you most enjoy solving?",
        "options": {
            "Designing a user-friendly app or website": "IT",
            "Writing a short story or creating a piece of art": "Creativity",
            "Helping someone overcome personal difficulties": "Social",
            "Diagnosing a health issue based on symptoms": "Medicine",
            "Fixing or building a mechanical device": "Technical"
        }
    },
    {
        "text": "2. What kind of school projects did you enjoy the most?",
        "options": {
            "Programming or building something digital": "IT",
            "Creative presentations or storytelling": "Creativity",
            "Group discussions and social issues": "Social",
            "Experiments in biology or chemistry": "Medicine",
            "Hands-on construction or engineering tasks": "Technical"
        }
    },
    {
        "text": "3. Which work style best describes you?",
        "options": {
            "Structured and analytical": "IT",
            "Expressive and imaginative": "Creativity",
            "Supportive and emotionally aware": "Social",
            "Careful and detail-focused": "Medicine",
            "Practical and task-oriented": "Technical"
        }
    },
    {
        "text": "4. You have a free weekend. What do you choose to do?",
        "options": {
            "Try coding something new or solve a puzzle": "IT",
            "Draw, write, or film something creative": "Creativity",
            "Volunteer or hang out with friends": "Social",
            "Read about health or science topics": "Medicine",
            "Fix something at home or build a DIY project": "Technical"
        }
    },
    {
        "text": "5. What environment do you see yourself working in?",
        "options": {
            "Remote office or tech company": "IT",
            "Creative studio or media agency": "Creativity",
            "School, center, or hospital with people": "Social",
            "Clinic, lab, or research institution": "Medicine",
            "Workshop, factory, or construction site": "Technical"
        }
    },
    {
        "text": "6. What motivates you the most?",
        "options": {
            "Solving complex logical problems": "IT",
            "Expressing ideas in unique ways": "Creativity",
            "Improving others’ lives and well-being": "Social",
            "Understanding how the human body works": "Medicine",
            "Creating or repairing something physical": "Technical"
        }
    },
    {
        "text": "7. What type of collaboration do you prefer?",
        "options": {
            "Working independently on technical tasks": "IT",
            "Brainstorming creative ideas with others": "Creativity",
            "Interacting and communicating with people": "Social",
            "Sharing knowledge to solve real-life problems": "Medicine",
            "Coordinating hands-on work in a team": "Technical"
        }
    },
    {
        "text": "8. What kind of content are you drawn to online?",
        "options": {
            "Tech trends, programming tutorials": "IT",
            "Art, design, or writing inspiration": "Creativity",
            "Mental health or communication skills": "Social",
            "Science documentaries, health advice": "Medicine",
            "Gadgets, tools, or DIY builds": "Technical"
        }
    },
    {
        "text": "9. If you could instantly gain expertise in one area, which would it be?",
        "options": {
            "Cybersecurity or AI": "IT",
            "Film direction or illustration": "Creativity",
            "Psychology or conflict resolution": "Social",
            "Surgery or disease treatment": "Medicine",
            "Automotive or robotics engineering": "Technical"
        }
    },
    {
        "text": "10. Which compliment would mean the most to you?",
        "options": {
            "“You’re incredibly logical and efficient.”": "IT",
            "“You’re full of original ideas.”": "Creativity",
            "“You really understand and care about people.”": "Social",
            "“You have excellent focus and precision.”": "Medicine",
            "“You’re a hands-on problem solver.”": "Technical"
        }
    }
]
categories = ["IT", "Creativity", "Social", "Medicine", "Technical"]

def init_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            step INTEGER DEFAULT 0,
            IT INTEGER DEFAULT 0,
            Creativity INTEGER DEFAULT 0,
            Social INTEGER DEFAULT 0,
            Medicine INTEGER DEFAULT 0,
            Technical INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Создание пользователя, если нет
def create_user_if_not_exists(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not c.fetchone():
        c.execute('INSERT INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

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
        btn = InlineKeyboardButton(text=option_text, callback_data=str(category))
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

