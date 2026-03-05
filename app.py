import streamlit as st
import re

# Настройка страницы
st.set_page_config(page_title="Хантер", layout="centered")

# Главный заголовок
st.title("🎯 ХАНТЕР: КОНТАКТЫ")
st.write("Вставьте текст — я вытащу номера и ссылки.")

# Поле ввода
raw_text = st.text_area("СЮДА КИДАЙ ТЕКСТ:", height=300)

# Кнопка поиска
if st.button("🚀 НАЙТИ ВСЕ КОНТАКТЫ"):
    if raw_text:
        # Умный поиск телефонов (РФ, РБ, СНГ)
        phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_text)))
        links = list(set(re.findall(r'https?://\S+', raw_text)))

        st.divider()

        if phones:
            st.subheader(f"✅ Найдено номеров: {len(phones)}")
            for p in phones:
                clean_p = re.sub(r'[^\d+]', '', p)
                if not clean_p.startswith('+') and len(clean_p) > 10:
                    clean_p = '+' + clean_p
                # Кнопка на весь экран для телефона
                st.link_button(f"📞 ПОЗВОНИТЬ {p}", f"tel:{clean_p}")
        
        if links:
            st.subheader("🔗 Ссылки:")
            for l in links:
                st.link_button("ОТКРЫТЬ ССЫЛКУ", l)

        if not phones and not links:
            st.warning("Ничего не найдено. Попробуйте другой текст.")
    else:
        st.error("Поле пустое!")
