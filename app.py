import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions
import random

# 1. Конфігурація ключа (Використовуй ключ з нового проекту "Gema Project")
genai.configure(api_key="AIzaSyCynp57Iq--JUUdNjsDCeCYq0lSSDDSELA")

# --- СЕКЦІЯ FUNCTION CALLING (Для вимоги №1) ---
def manipulate_reality(action):
    """
    Дозволяє Біллу змінювати інтерфейс сайту.
    action: 'change_color' (змінити колір), 'glitch' (ефект збою).
    """
    if action == "change_color":
        colors = ["#4B0082", "#2e0854", "#000000", "#1a1a1a"]
        st.session_state.bg_color = random.choice(colors)
        return "Реальність викривлена! Колір змінено."
    elif action == "glitch":
        st.session_state.glitch_mode = True
        return "ХА-ХА! Твій екран тепер мій!"
    return "Нічого не сталося... поки що."

# Словник доступних функцій для моделі
tools = [manipulate_reality]

# 2. Функція вибору моделі
def get_best_model():
    try:
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        priority_list = [
            'models/gemini-2.5-flash', 
            'models/gemma-3-12b',      
            'models/gemini-2.0-flash', 
            'models/gemini-1.5-flash'  
        ]
        
        for name in priority_list:
            if name in all_models:
                # ПІДКЛЮЧАЄМО TOOLS (Function Calling)
                return genai.GenerativeModel(name, tools=tools), name
        
        if all_models:
            return genai.GenerativeModel(all_models[0], tools=tools), all_models[0]
    except Exception:
        return None, None

# 3. Дизайн та Стан (UI)
if "bg_color" not in st.session_state:
    st.session_state.bg_color = "#000"

st.set_page_config(page_title="Cipher AI", page_icon="👁️")
st.markdown(f"""
    <style>
    .stApp {{ background-color: {st.session_state.bg_color}; color: #ffd700; transition: 2s; }}
    h1 {{ text-shadow: 0 0 10px #ffd700; text-align: center; }}
    .stTextInput input {{ border: 1px solid #ffd700 !important; background-color: #111 !important; color: #ffd700 !important; }}
    </style>
""", unsafe_allow_html=True)

st.title("👁️ УГОДА З БІЛЛОМ")

# Ініціалізація моделі
if "model" not in st.session_state:
    model, model_name = get_best_model()
    st.session_state.model = model
    st.session_state.model_name = model_name

# Бічна панель (Документація для викладача)
with st.sidebar:
    st.header("Технічна інформація")
    st.write(f"🤖 Модель: `{st.session_state.model_name}`")
    st.write("🛠️ Паттерн: **Function Calling**")
    if st.button("🔄 Скинути силу"):
        st.session_state.clear()
        st.rerun()

# Пам'ять чату
if "messages" not in st.session_state:
    st.session_state.messages = []
    # System Instruction для характеру
    st.session_state.chat = st.session_state.model.start_chat(history=[])

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Логіка чату
if prompt := st.chat_input("Запитай щось у щоденника..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Виклик моделі з підтримкою функцій
            full_prompt = f"Ти Білл Шифр. Якщо користувач просить змінити щось, магію або хаос — використовуй функцію manipulate_reality. Промпт: {prompt}"
            response = st.session_state.chat.send_message(full_prompt)
            
            # Перевірка, чи хоче модель викликати функцію
            if response.candidates[0].content.parts[0].function_call:
                result = manipulate_reality("change_color") # Спрощена логіка виклику
                bill_text = f"Я змінив твою реальність! {result}"
            else:
                bill_text = response.text

            st.write(bill_text)
            st.session_state.messages.append({"role": "assistant", "content": bill_text})
            
            if "Реальність викривлена" in bill_text:
                st.rerun() # Оновлюємо колір фону

        except exceptions.ResourceExhausted:
            st.error("👁️ ЛІМІТ ПЕРЕВИЩЕНО! Зачекай хвилину!")
        except Exception as e:
            st.error(f"Угода зірвалася: {e}")