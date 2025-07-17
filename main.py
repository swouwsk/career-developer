
from config import *
import sqlite3
from openai import OpenAI
import requests
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telebot import types

bot = TeleBot(TOKEN)
hideBoard = types.ReplyKeyboardRemove() 
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HUGGINGFACE_API_TOKEN = KEY 

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

profession_info = {
    "designer": {
        "description": "🎨 A designer creates visual concepts to communicate ideas. Skills: creativity, Adobe tools, UX/UI.",
        "pros": [
            "Creative and expressive work",
            "High demand in digital industries",
            "Remote work opportunities"
        ],
        "cons": [
            "Tight deadlines",
            "Client revisions and feedback loops",
            "Competitive field"
        ]
    },
    "doctor": {
        "description": "🩺 A doctor diagnoses and treats illnesses. Skills: biology, empathy, strong responsibility.",
        "pros": [
            "High social value and respect",
            "Good income potential",
            "Life-saving impact"
        ],
        "cons": [
            "Long education and training",
            "High stress and responsibility",
            "Irregular working hours"
        ]
    },
    "programmer": {
        "description": "💻 A programmer writes code for apps and systems. Skills: Python, logic, problem-solving.",
        "pros": [
            "High salaries",
            "Remote work and freelance options",
            "Constant learning opportunities"
        ],
        "cons": [
            "Sedentary lifestyle",
            "Debugging stress",
            "Fast-changing technologies"
        ]
    },
    "teacher": {
        "description": "📚 A teacher educates students and supports learning. Skills: communication, patience, subject knowledge.",
        "pros": [
            "Impact on future generations",
            "Stable employment",
            "Vacation periods"
        ],
        "cons": [
            "Often underpaid",
            "Emotional exhaustion",
            "Challenging student behavior"
        ]
    },
    "psychologist": {
        "description": "🧠 Psychologists help people understand their behavior and emotions. Skills: empathy, analysis, listening.",
        "pros": [
            "Meaningful and fulfilling work",
            "Flexibility in private practice",
            "Diverse career paths"
        ],
        "cons": [
            "Emotionally demanding",
            "Lengthy education",
            "Client dependency"
        ]
    },
    "engineer": {
        "description": "🛠️ Engineers design, build, and improve systems, machines, and structures using science and math. Skills: problem-solving, analysis, technical and math knowledge.",
        "pros": [
            "High demand in many fields",
            "Good salary potential",
            "Opportunity to innovate and create"
        ],
        "cons": [
            "Can be stressful under deadlines",
            "Long or irregular work hours",
            "Requires continuous learning"
        ]
    }
}

categories = ["IT", "Creativity", "Social", "Medicine", "Technical"]

category_to_professions = {
    "IT": [
        "Frontend Developer",
        "Data Analyst",
        "Cybersecurity Specialist",
        "AI Engineer",
        "Game Developer"
    ],
    "Medicine": [
        "Psychologist",
        "Veterinarian",
        "Nurse",
        "Dentist",
        "Medical Laboratory Technician"
    ],
    "Technical": [
        "Electrician",
        "Architect",
        "Car Mechanic",
        "Construction Worker",
        "Engineer"
    ],
    "Creativity": [
        "Writer",
        "Musician",
        "Photographer",
        "Actor",
        "Designer"
    ],
    "Social": [
        "Sociologist",
        "Historian",
        "Political Analyst",
        "Psychologist",
        "Teacher"
    ]
}


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
    bot.send_message(message.chat.id, """Hello! 🙌 I am here to help teenagers and young 
                     adults discover their ideal professions 
                     and receive personalized career advice. 💪 ) 
""")
    info(message)
    
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
"""
💫 Here are the available commands you can use:

/start — Get started with the bot.
/quiz — Take a quiz to discover category that match your interests.
/categories — View categories and their professions.
/profession [name] — Get information about a specific profession (e.g., /profession designer).
/proflist — List all available professions you can learn about.
/advice — Receive career advice and tips.
/info — Display a list of all available commands.

""")
    


@bot.message_handler(commands=['quiz'])
def handle_quiz(message):
    user_id = message.from_user.id
    create_user_if_not_exists(user_id)

    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("SELECT step FROM users WHERE user_id = ?", (user_id,))
    step = c.fetchone()[0]
    conn.close()

    if step >= len(QUIZ):
        # Спрашиваем, хочет ли пройти заново
        send_existing_result(user_id)
    else:
        # Проходит впервые
        reset_quiz_progress(user_id)
        send_question(user_id)

def send_existing_result(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("SELECT IT, Creativity, Social, Medicine, Technical FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()

    scores = dict(zip(categories, row))
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    max_score = top[0][1]
    top_categories = [cat for cat, score in top if score == max_score]

    result_text = "ℹ️ You have already completed the quiz.\n\n"
    result_text += "✅ Your most suitable directions:\n"
    result_text += "\n".join(f"• {cat}" for cat in top_categories)
    result_text += "\n\n📊 Your scores:\n"
    result_text += "\n".join(f"{cat}: {score}" for cat, score in top)

    # Кнопки
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 Retake quiz", callback_data="restart_quiz"))
    markup.add(InlineKeyboardButton("🚫 No, thanks", callback_data="cancel_quiz"))

    bot.send_message(user_id, result_text, reply_markup=markup, parse_mode="Markdown")

def reset_quiz_progress(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("""
        UPDATE users SET step = 0,
        IT = 0, Creativity = 0, Social = 0, Medicine = 0, Technical = 0
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()

@bot.callback_query_handler(func=lambda call: call.data in ["restart_quiz", "cancel_quiz"])
def handle_quiz_choice(call):
    user_id = call.from_user.id
    if call.data == "restart_quiz":
        reset_quiz_progress(user_id)
        bot.answer_callback_query(call.id, "Quiz restarted!")
        send_question(user_id)
    else:
        bot.answer_callback_query(call.id, "Quiz not restarted.")
        bot.send_message(user_id, "Okay, let me know when you're ready 👁️👄👁️")

def send_question(user_id):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('SELECT step FROM users WHERE user_id = ?', (user_id,))
    step = c.fetchone()[0]
    conn.close()

    if step >= len(QUIZ):
        send_result(user_id)     
        return                  

    if step == 0:
        bot.send_message(user_id, "💯 Let's start the quiz to discover your ideal profession!")


    q = QUIZ[step]
    markup = InlineKeyboardMarkup()
    for option_text, category in q['options'].items():
        btn = InlineKeyboardButton(text=option_text, callback_data=str(category))
        markup.add(btn)
    bot.send_message(user_id, q['text'], reply_markup=markup)

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
    max_score = top[0][1]

    # Все категории с максимальным баллом
    top_categories = [cat for cat, score in top if score == max_score]

    result_text = "✍️ Based on your answers, your most suitable career directions:\n"
    for cat in top_categories:
        result_text += f"• {cat}\n"

    # Полный список баллов
    result_text += "\n📊 Full scores:\n"
    for cat, score in top:
        result_text += f"{cat}: {score}\n"

    bot.send_message(user_id, result_text, parse_mode="Markdown")
    bot.send_message(user_id, "🕺Thank you for taking the quiz! You can now use /profession to learn more about specific careers.")

@bot.message_handler(commands=['profession'])
def handle_profession(message):
    user_input = message.text.split(maxsplit=1)

    if len(user_input) == 1:
        bot.send_message(message.chat.id,
                         "❗ Please provide a profession name.\nExample: /profession designer")
        return

    profession = user_input[1].strip().lower()

    if profession in profession_info:
        prof = profession_info[profession]
        text = f"{prof['description']}\n\n" \
               f"✅ *+ Pros:*\n" + '\n'.join(f"• {p}" for p in prof['pros']) + "\n\n" \
               f"⚠️ *- Cons:*\n" + '\n'.join(f"• {c}" for c in prof['cons'])
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id,
                         f"❌ Sorry, I don't have info about '{profession}'.\nTry another or type /list to see available professions.")

@bot.message_handler(commands=['categories'])
def send_categories_with_professions(message):
    response = "*📚 Categories and Their Professions\n (ATTENTION❗ I don't have all professions from this list. To check available professions type /list):*\n\n"
    for category, professions in category_to_professions.items():
        response += f"*{category}*:\n"
        for prof in professions:
            response += f"• {prof}\n"
        response += "\n"

    bot.send_message(message.chat.id, response, parse_mode="Markdown")

@bot.message_handler(commands=['proflist'])
def list_professions(message):
    all_profs = ",\n ".join(profession_info.keys())
    bot.send_message(message.chat.id, f"📋 Available professions:\n{all_profs}")

    



@bot.message_handler(commands=['advice'])
def career_advice(message):
    bot.send_message(message.chat.id, "✍️ Send me your career question or situation, and I’ll try to help!")

@bot.message_handler(func=lambda message: True)
def handle_question(message):
    if message.text.startswith("/"):
        return 
    bot.send_message(message.chat.id, "🤖 Thinking... Please wait.")
    answer = get_career_advice_from_huggingface(message.text)
    bot.send_message(message.chat.id, answer)

def get_career_advice_from_huggingface(question):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    prompt = f"You are a helpful career advisor. Give a short, practical response to the question: '{question}'"
    
    response = requests.post(
        HUGGINGFACE_API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    try:
        result = response.json()
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        elif 'generated_text' in result:
            return result['generated_text']
        elif 'error' in result:
            return "❌ Error: " + result['error']
        else:
            return "⚠️ Couldn't generate a response."
    except Exception as e:
        return "🚫 Something went wrong."


if __name__ == '__main__':
    init_db()
    bot.polling(none_stop=True)

