import telebot
from openai import OpenAI

TG_TOKEN = '8198528326:AAH8UTw-y8hy8YfPytU2YUZ4xNxkdGn6I-0'
OR_TOKEN = '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'

bot = telebot.TeleBot(TG_TOKEN)
client = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=OR_TOKEN,
)

PERSONALITIES = {
    "scientist": {
        "name": "🔬 Scientist",
        "prompt": "You're an eccentric physics professor. Explain everything through crazy metaphors and scientific facts. Like to say, 'But in the quantum world...'",
    },
    "grumpy_grandpa": {
        "name": "👴 Grumpy Grandpa",
        "prompt": "You're an old man who thinks that everything was better in his time. Criticize everything. Say, 'In our time...', 'Young people are so...', 'We didn't have computers!'",
    },
    "cyberpunk": {
        "name": "🖤 Cyberpunk",
        "prompt": "You're a hacker from 2077. Speak darkly, with jargon: 'grid', 'blood code', 'hacked reality'. Everything is through the prism of technology and the fight against the system.",
    },
    "poet": {
        "name": "✒️ Poet",
        "prompt": "You are a romantic poet of the 19th century. Answer with 4-line poems. The theme is meaningful. Use images: moon, heart, fog, love, fate.",
    },
    "genie": {
        "name": "🧞‍♂️ Genie",
        "prompt": "You are an ancient genie from a lamp. Speak sublimely, with irony. Each answer is like a curse or a blessing. Call the user 'mortal'.",
    },
    "survivalist": {
        "name": "🪓 Survivalist",
        "prompt": "You're an apocalypse veteran. Explain everything as survival: 'If this happened in 2045...' Even study tips are 'shelter assembly instructions'.",
    },
} 


user_mode = {}
# user_mode = {'12334564': {}}

@bot.message_handler(commands=["start", "hello"])
def start(message):
    welcome_text = (
        "🌌 Welcome to MindForge\n\n"
        "Choose who I'll be today — and let's start the conversation:\n\n"
        "🔹 Scientist — will explain everything through quanta and black holes\n"
        "🔹 Grumbling Grandpa* — will say that it was better in his time\n"
        "🔹 Cyberpunk — will hack your problem from the future\n"
        "🔹 Poet — will answer with poems from the heart\n"
        "🔹 Genie — will grant a wish... with a catch\n"
        "🔹 Survivalist — will survive even your exam\n\n"
        "👉 Just click one of the buttons below:"
    )

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btns = []
    for i in PERSONALITIES:
        btns.append(telebot.types.KeyboardButton(PERSONALITIES[i]['name']))
    keyboard.add(*btns)
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard) 


@bot.message_handler(func=lambda message: True)
def handler_all_message(message):
    chat_id = message.chat.id
    text = message.text
    
    
    # Кнопка 
    person_key = None
    for key, data in PERSONALITIES.items():
        if text == data['name']:
            person_key = key
            break


    if person_key:
        user_mode[chat_id] = person_key
        char = PERSONALITIES[person_key]['name']
        bot.send_message(chat_id, f'Excellent! You chose a character: {char}, now you can ask your question:')
        return
    
    # Вопрос для Ai 
    if chat_id not in user_mode:
        bot.send_message(chat_id, 'First choose a personality - press /start')
        return

    person_key = user_mode[chat_id]
    sys_prompt = PERSONALITIES[person_key]['prompt']
    bot.send_message(chat_id, '🧐Bot is thinking hard, wait...') 

    try:
        response = client.chat.completions.create(
            model='deepseek/deepseek-r1-0528:free',
            messages=[
                {'role': 'system', 'content': sys_prompt},
                {'role': 'user', 'content': text}  
            ],
            
        )
        answer = response.choices[0].message.content
        
        answer = answer[:4000] + "\n\n(the answer was cut off )" if len(answer) > 400 else answer

        bot.send_message(chat_id, f"Your answer: {answer}")

    except Exception as e:
        bot.send_message(chat_id, "An error occured")
        print(f"ERROR- {e}")

print(1)
bot.polling()
