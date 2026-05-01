import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions
import random

# 1. КОНФІГУРАЦІЯ (Встав свій новий ключ нижче)
# Ключ має бути з "Gema Project"
API_KEY = "AIzaSyBBPXf8seI-8xAHZx95t7WXgaT2ddzkkXQ" 
genai.configure(api_key=API_KEY)

# --- ФУНКЦІЯ ДЛЯ ВИМОГ ПРОЄКТУ (Function Calling) ---
def manipulate_reality(action: str):
    """Змінює вигляд інтерфейсу сайту (магія Білла)."""
    if action == "change_color":
        colors = ["#4B0082", "#2e0854", "#1a1a1a", "#320129", "#000000"]
        st.session_state.bg_color = random.choice(colors)
        return "Реальність викривлена! Колір змінено."
    return "Хаос уже близько..."

tools = [manipulate_reality]

# 2. ФУНКЦІЯ ВИБОРУ МОДЕЛІ
def get_best_model():
    try:
        # Отримуємо список усіх доступних моделей для твого ключа
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Список пріоритетів (твоя 2.5 на першому місці)
        priority_list = [
            'models/gemini-2.5-flash', 
            'models/gemini-1.5-flash', # Технічна назва 2.5
            'models/gemini-2.0-flash', 
            'models/gemma-3-12b'
        ]
        
        for name in priority_list:
            if name in all_models:
                # Підключаємо інструменти (tools) для виконання вимог проєкту
                return genai.GenerativeModel(name, tools=tools), name
        
        if all_models:
            return genai.GenerativeModel(all_models[0], tools=tools), all_models[0]
    except Exception as e:
        return None, str(e)
    return None, "No models found"

# 3. ДИЗАЙН (UI)
if "bg_color" not in st.session_state:
    st.session_state.bg_color = "#000"

st.set_page_config(page_title="Cipher AI", page_icon="👁️")
st.markdown(f"""
    <style>
    .stApp {{ background-color: {st.session_state.bg_color}; color: #ffd700; transition: 2s; }}
    h1 {{ text-shadow: 0 0 10px #ffd700; text-align: center; }}
    .stTextInput input {{ border: 1px solid #ffd700 !important; background-color: #111 !important; color: #ffd700 !important; }}
    .stChatMessage {{ background-color: #111; border: 1px solid #ffd700; border-radius: 10px; }}
    </style>
""", unsafe_allow_html=True)

st.title("👁️ УГОДА З БІЛЛОМ")

# 4. БЕЗПЕЧНА ІНІЦІАЛІЗАЦІЯ (Щоб не було помилок як на скріншоті 3bc018)
if "model" not in st.session_state:
    model, model_name = get_best_model()
    if model:
        st.session_state.model = model
        st.session_state.model_name = model_name
        st.session_state.chat = model.start_chat(history=[])
    else:
        st.error(f"🚨 Помилка підключення: {model_name}. Перевір API ключ!")
        st.stop()

# Бокова панель з інфою для викладача
with st.sidebar:
    st.write(f"🤖 Модель: `{st.session_state.model_name}`")
    st.write("🛠️ Паттерн: **Function Calling**")
    if st.button("🔄 Оновити силу"):
        st.session_state.clear()
        st.rerun()

# 5. ЛОГІКА ЧАТУ
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Запитай щось у щоденника..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Спеціальна інструкція в кожному запиті
            full_prompt = f"Ти Білл Шифр. Якщо користувач просить змінити колір, магію або хаос — ОБОВ'ЯЗКОВО викликай функцію manipulate_reality(action='change_color'). Промпт: {prompt}"
            
            response = st.session_state.chat.send_message(full_prompt)
            
            # Перевірка на виклик функції (Requirement Check)
            if response.candidates[0].content.parts[0].function_call:
                msg = manipulate_reality("change_color")
                bill_text = f"Я ВИКРИВИВ ТВОЮ РЕАЛЬНІСТЬ! {msg}"
                st.write(bill_text)
                st.session_state.messages.append({"role": "assistant", "content": bill_text})
                st.rerun()
            else:
                bill_text = response.text
                st.write(bill_text)
                st.session_state.messages.append({"role": "assistant", "content": bill_text})

        except exceptions.ResourceExhausted:
            st.error("👁️ ЛІМІТ ПЕРЕВИЩЕНО! Зачекай хвилину!")
        except Exception as e:
            st.error(f"Угода зірвалася: {e}")