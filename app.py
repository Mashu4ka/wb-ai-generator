import streamlit as st
from openai import OpenAI

# 1. Настройка внешнего вида страницы
st.set_page_config(
    page_title="WB Ghostwriter AI", 
    page_icon="✍️", 
    layout="centered"
)

# Кастомный CSS для стиля (фиолетовый в стиле WB)
st.markdown("""
    <style>
    .main { background-color: #f5f5f7; }
    .stButton>button { background-color: #8a2be2; color: white; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 WB Ghostwriter AI")
st.markdown("##### Создавай топовые описания для маркетплейсов за секунды")

# 2. Боковая панель (Sidebar) для настроек
with st.sidebar:
    st.header("⚙️ Настройки ИИ")
    # Ключ от DeepSeek (можно получить на ://deepseek.com)
    api_key = st.text_input("Введите DeepSeek API Key", type="password")
    
    st.divider()
    style = st.selectbox("Стиль текста", ["Продающий", "Заботливый", "Технический/Лаконичный"])
    temperature = st.slider("Креативность", 0.1, 1.0, 0.7)
    
    st.info("DeepSeek API в 10 раз дешевле ChatGPT, поэтому мы используем его! 🚀")

# 3. Основная форма ввода
col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Название товара", placeholder="Например: Термос из стали")
    features = st.text_area("Характеристики", placeholder="1 литр, держит холод 24ч, в комплекте чехол", height=150)

with col2:
    keywords = st.text_area("SEO-ключи", placeholder="подарок мужчине, туризм, термос для чая", height=150)

st.divider()

# 4. Логика работы
if st.button("✨ Сгенерировать описание"):
    if not api_key:
        st.error("Ошибка: Введите API ключ DeepSeek в боковом меню!")
    elif not product_name:
        st.warning("Внимание: Укажите название товара.")
    else:
        try:
            # Инициализация клиента DeepSeek
            client = OpenAI(api_key=api_key, base_url="https://deepseek.com")
            
            with st.spinner('Нейросеть анализирует рынок и пишет текст...'):
                # Формируем промпт
                prompt = f"""
                Ты — эксперт-копирайтер по Wildberries и Ozon. 
                Напиши описание товара '{product_name}' в стиле '{style}'.
                
                ХАРАКТЕРИСТИКИ: {features}
                ОБЯЗАТЕЛЬНЫЕ SEO-КЛЮЧИ: {keywords}
                
                СТРУКТУРА:
                1. Заголовок с главным ключом.
                2. Завлекающее вступление.
                3. Список преимуществ с эмодзи.
                4. Блок "Почему выбирают нас".
                5. Призыв к действию.
                
                Правила: Текст должен быть легким, без 'воды', ключи вплетаются незаметно.
                """

                # Запрос к DeepSeek
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                
                result_text = response.choices.message.content
                
                # Вывод результата
                st.success("Готово! Текст оптимизирован для WB.")
                st.markdown("---")
                st.markdown(result_text)
                
                # Кнопка копирования
                st.copy_to_clipboard(result_text)
                st.toast("Текст скопирован в буфер обмена!")

        except Exception as e:
            st.error(f"Произошла ошибка: {e}")

# Футер
st.markdown("---")
st.caption("Developed by Young Founder 🚀 | Version 1.0 (DeepSeek Powered)")
