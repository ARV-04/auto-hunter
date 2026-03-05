import streamlit as st
import re

# 1. Настройка страницы (Чистый русский интерфейс)
st.set_page_config(page_title="Авто Хантер AI", page_icon="🎯")

# 2. Защита паролем
password = st.sidebar.text_input("Пароль доступа:", type="password")
if password != "MINSK2026":
    st.warning("⚠️ Введите пароль в боковой панели для работы с системой.")
    st.stop()

# 3. Основной интерфейс
st.title("🎯 Авто Хантер: СНГ")
st.write("Универсальный поиск контактов для всех стран СНГ. Находит телефоны, почты и ссылки.")

# 4. Поле ввода
raw_text = st.text_area("Вставьте ваш текст сюда:", height=250, placeholder="Текст из чатов, сайтов или базы данных...")

# 5. Обработка данных
if st.button("🚀 Найти все контакты"):
    if raw_text:
        # Улучшенная регулярка: ищет номера от 7 до 15 цифр, начинающиеся с + или цифр (РФ, РБ, КЗ, УЗ и др.)
        phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_text)))
        emails = list(set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)))
        urls = list(set(re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', raw_text)))

        st.divider()

        # Результаты: Телефоны
        if phones:
            st.subheader(f"📞 Контактные номера ({len(phones)})")
            for p in phones:
                # Очищаем номер для клика (оставляем только + и цифры)
                clean_p = re.sub(r'[^\d+]', '', p)
                if not clean_p.startswith('+') and len(clean_p) > 10:
                    clean_p = '+' + clean_p
                st.link_button(f"📞 Позвонить {p}", f"tel:{clean_p}")
        
        # Почты и Ссылки
        if emails or urls:
            col1, col2 = st.columns(2)
            with col1:
                if emails:
                    st.subheader("📧 Почты:")
                    for e in emails: st.info(e)
            with col2:
                if urls:
                    st.subheader("🔗 Ссылки:")
                    for u in urls: st.link_button("Открыть ссылку", u)

        if not phones and not emails and not urls:
            st.warning("Контакты не обнаружены. Попробуйте вставить другой текст.")
    else:
        st.error("Ошибка: Поле ввода пустое!")
