import streamlit as st
from openai import OpenAI

# Настройка страницы в стиле "Dark Mode"
st.set_page_config(page_title="WB Ghostwriter AI", page_icon="📝")

# Заголовок и описание
st.title("🚀 WB Ghostwriter AI")
st.subheader("Генератор продающих описаний для маркетплейсов")

# Боковая панель для настроек
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите API Ключ (OpenAI/GigaChat/DeepSeek)", type="password")
    model_choice = st.selectbox("Выбор модели", ["gpt-3.5-turbo", "gpt-4-mini"])
    temperature = st.slider("Креативность текста", 0.0, 1.0, 0.7)

# Основной интерфейс
col1, col2 = st.columns(2)

with col1:
    product_name = st.text_input("Название товара", placeholder="Например: Массажер для шеи")
    features = st.text_area("Ключевые характеристики", placeholder="Например: 3 режима, подогрев, зарядка от USB, кожа")

with col2:
    keywords = st.text_area("SEO-ключи (через запятую)", placeholder="массажер, подарок маме, релакс")

if st.button("✨ Сгенерировать идеальное описание"):
    if not api_key:
        st.error("Сначала введи API ключ в боковом меню!")
    elif not product_name:
        st.warning("Введи хотя бы название товара.")
    else:
        with st.spinner('Нейронка колдует...'):
            try:
                # Настройка клиента (здесь можно подставить любой эндпоинт)
                client = OpenAI(api_key=api_key)

                prompt = f"""
                Ты — профессиональный копирайтер и эксперт по SEO-оптимизации на маркетплейсах Wildberries и Ozon. 
                Твоя задача: превратить сухие факты о товаре в текст, который заставляет купить.

                ДАННЫЕ ТОВАРА:
                Название: {product_name}
                Характеристики: {features}
                SEO-ключи: {keywords}

                ПЛАН ТЕКСТА:
                1. Заголовок: Привлекательный, с использованием главного ключа.
                2. Эмоциональное вступление: Какую проблему решает товар? (2-3 предложения).
                3. Список преимуществ: Используй буллиты (эмодзи), раскрой характеристики через выгоду для клиента.
                4. Сценарии использования: Где и как применять (в подарок, в офис, для дома).
                5. Призыв к действию: Заряди на покупку и добавление бренда в избранное.

                ПРАВИЛА:
                - Используй все SEO-ключи ЕСТЕСТВЕННО (не просто списком).
                - Тон: Дружелюбный, экспертный.
                - Никакой воды и пустых фраз типа "самый лучший товар в мире".
                - Используй абзацы, чтобы текст было удобно читать с телефона.

                ПИШИ НА РУССКОМ ЯЗЫКЕ.
                """

                response = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )

                result = response.choices[0].message.content

                # Вывод результата
                st.success("Готово! Копируй и вставляй в карточку:")
                st.markdown("---")
                st.markdown(result)
                st.button("📋 Скопировать (в разработке)")  # Для вайба
            except Exception as e:
                st.error(f"Ошибка: {e}")

# Футер
st.info("💡 Лайфхак: Добавь больше характеристик, чтобы текст был точнее.")
