import streamlit as st
import re

# 1. Настройка: Название вкладки на русском
st.set_page_config(page_title="Хантер", layout="centered")

# Убираем английские менюшки (скрываем их)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #ff4b4b; color: white; font-weight: bold; font-size: 20px;
    }
    </style>
    """, unsafe_allow_code=True)

# 2. Витрина
st.title("🎯 ХАНТЕР: КОНТАКТЫ")
st.write("Вставь текст — получи кликабельные номера для звонка.")

# 3. Поле для работы
raw_text = st.text_area("СЮДА КИДАЙ ТЕКСТ (КУКИ, ЧАТЫ И Т.Д.):", height=250)

# 4. Кнопка «Пуск»
if st.button("🚀 НАЙТИ ВСЕ НОМЕРА"):
    if raw_text:
        # Ищет любые номера (РФ, РБ, СНГ)
        phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_text)))
        links = list(set(re.findall(r'https?://\S+', raw_text)))

        st.divider()

        if phones:
            st.subheader(f"✅ Найдено номеров: {len(phones)}")
            for p in phones:
                # Делаем чистый номер для звонка
                clean_p = re.sub(r'[^\d+]', '', p)
                if not clean_p.startswith('+') and len(clean_p) > 10:
                    clean_p = '+' + clean_p
                # Кнопка звонка на весь экран
                st.link_button(f"📞 ПОЗВОНИТЬ {p}", f"tel:{clean_p}")
        
        if links:
            st.subheader("🔗 Ссылки:")
            for l in links:
                st.link_button("ОТКРЫТЬ ССЫЛКУ", l)

        if not phones and not links:
            st.warning("Ничего не нашел. Проверь текст!")
    else:
        st.error("Поле пустое!")
