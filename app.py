import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# 1. Конфігурація ключа
genai.configure(api_key="AIzaSyCynp57Iq--JUUdNjsDCeCYq0lSSDDSELA")

# 2. Функція з ПРИМУСОВИМ пріоритетом Gemma
def get_best_model():
    try:
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
       
            # Список пріоритетів (найновіші версії)
        priority_list = [
            'models/gemini-2.5-flash', # Те, що на скріншоті
            'models/gemma-3-12b',      # Gemma з лімітом 14.4K
            'models/gemini-2.0-flash', # Запасний стабільний варіант
            'models/gemini-1.5-flash'  # Технічна назва 2.5 для старих бібліотек
        ]
        
        
        for name in priority_list:
            if name in all_models:
                return genai.GenerativeModel(name), name
        
        if all_models:
            return genai.GenerativeModel(all_models[0]), all_models[0]
    except Exception:
        return None, None

# 3. Дизайн (без змін)
st.set_page_config(page_title="Cipher AI", page_icon="👁️")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #ffd700; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    h1 { text-shadow: 0 0 10px #ffd700; text-align: center; }
    .stTextInput input { border: 1px solid #ffd700 !important; background-color: #111 !important; color: #ffd700 !important; }
    .stChatMessage { background-color: #111; border: 1px solid #ffd700; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("👁️ УГОДА З БІЛЛОМ")

# Кнопка для ручного скидання, якщо модель застрягла
if st.sidebar.button("🔄 Оновити силу (скинути модель)"):
    for key in ["model", "model_name"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Ініціалізація
if "model" not in st.session_state:
    model, model_name = get_best_model()
    if model:
        st.session_state.model = model
        st.session_state.model_name = model_name
    else:
        st.error("Сила демона не знайдена! Перевір ключ.")

# Відображення поточної моделі
if "model_name" in st.session_state:
    st.write(f"🌐 **Поточна модель:** `{st.session_state.model_name}`")

# Пам'ять чату
if "messages" not in st.session_state:
    st.session_state.messages = []

# Виведення історії
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Поле введення
if prompt := st.chat_input("Запитай щось у щоденника..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    full_prompt = f"System: Ти демон Білл Шифр. Хитрий, зверхній. Відповідай коротко.\nUser: {prompt}"

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = st.session_state.model.generate_content(full_prompt)
            bill_text = response.text
            message_placeholder.write(bill_text)
            st.session_state.messages.append({"role": "assistant", "content": bill_text})
        except exceptions.ResourceExhausted:
            message_placeholder.error("👁️ ЛІМІТ ПЕРЕВИЩЕНО! Зачекай хвилину!")
        except Exception as e:
            message_placeholder.error(f"Угода зірвалася: {e}")