import streamlit as st
from gigachat import GigaChat

# Настройка страницы
st.set_page_config(page_title="WB Helper AI", page_icon="📈")

st.title("🚀 WB Smart Assistant")

# Авторизация в боковой панели
with st.sidebar:
    st.header("🔑 Доступ")
    giga_key = st.text_input("GigaChat API Key", type="password")
    st.caption("Получи ключ на developers.sber.ru")

# Создаем вкладки
tab1, tab2 = st.tabs(["📝 Описания товаров", "💬 Ответы на отзывы"])

# ВКЛАДКА 1: ОПИСАНИЯ
with tab1:
    product_name = st.text_input("Товар", placeholder="Например: Спортивная бутылка")
    features = st.text_area("Характеристики", placeholder="Объем 0.5л, пищевой пластик")

    if st.button("Создать описание"):
        if not giga_key:
            st.warning("Вставь ключ в боковую панель!")
        else:
            with GigaChat(credentials=giga_key, verify_ssl_certs=False) as giga:
                prompt = f"Напиши продающее описание для WB: {product_name}. Характеристики: {features}. С эмодзи и структурой."
                res = giga.chat(prompt)
                st.success("Готово!")
                st.write(res.choices[0].message.content)

# ВКЛАДКА 2: ОТВЕТЫ НА ОТЗЫВЫ
with tab2:
    st.subheader("Генератор вежливых ответов")

    rating = st.slider("Оценка покупателя (звезд)", 1, 5, 5)
    review_text = st.text_area("Текст отзыва покупателя", placeholder="Например: Товар пришел разбитый, я в ярости!")

    col1, col2 = st.columns(2)
    with col1:
        brand_name = st.text_input("Ваш бренд", value="Наш Магазин")
    with col2:
        add_bonus = st.checkbox("Предложить скидку/подарок за плохой отзыв")

    if st.button("Сгенерировать ответ"):
        if not giga_key:
            st.warning("Вставь ключ в боковую панель!")
        else:
            with GigaChat(credentials=giga_key, verify_ssl_certs=False) as giga:
                # Промпт для умного ответа
                review_prompt = f"""
                Ты — менеджер службы заботы бренда '{brand_name}'. 
                Клиент оставил отзыв с оценкой {rating} звезд.
                Текст отзыва: "{review_text}"

                ЗАДАЧА:
                Напиши вежливый, человечный ответ. 
                - Если оценка 4-5: поблагодари, пригласи за новыми покупками.
                - Если оценка 1-3: извинись, посочувствуй, предложи решение (проверить товар при получении или связаться с поддержкой).
                {"Добавь предложение о бонусе или промокоде на следующую покупку." if add_bonus else ""}
                Не используй шаблоны, пиши искренне.
                """

                try:
                    with st.spinner("Менеджер пишет ответ..."):
                        res = giga.chat(review_prompt)
                        answer = res.choices.message.content
                        st.info("Рекомендуемый ответ:")
                        st.write(answer)
                except Exception as e:
                    st.error(f"Произошла ошибка: {e}")
