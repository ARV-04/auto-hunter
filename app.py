import streamlit as st
import re
import pandas as pd

# Настройка Агрегатора
st.set_page_config(page_title="Хантер: Агрегатор", layout="wide")

st.title("🎯 АВТО-ХАНТЕР: СБОР БАЗЫ")
st.write("Сбор и выгрузка запросов по запчастям для монетизации.")

# Поле для ввода кучи текста из чатов
raw_text = st.text_area("ВСТАВЬ ТЕКСТ ИЗ ЧАТОВ (Viber, TG, Сайты):", height=250)

if st.button("🚀 ОБРАБОТАТЬ И ВНЕСТИ В БАЗУ"):
    if raw_text:
        # Ищем телефоны (РФ, РБ, СНГ)
        phones = list(set(re.findall(r'(?:\+|\b)(?:\d[\s\-]?){10,14}\d', raw_text)))
        
        if phones:
            st.success(f"✅ Найдено новых контактов: {len(phones)}")
            
            # Создаем Библиотеку (Таблицу)
            df = pd.DataFrame(phones, columns=["Контакт"])
            
            # Вывод таблицы на экран (твоя витрина)
            st.subheader("📊 ТВОЯ ТЕКУЩАЯ БАЗА ЗАПЧАСТЕЙ:")
            st.table(df)
            
            # Кнопка СКАЧАТЬ (то, что ты будешь продавать сервисам)
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 СКАЧАТЬ БАЗУ В EXCEL (ДЛЯ ПАРТНЕРОВ)",
                data=csv,
                file_name='hunter_base_export.csv',
                mime='text/csv',
            )
            
            st.divider()
            # Кнопки для быстрого обзвона
            for p in phones:
                clean_p = re.sub(r'[^\d+]', '', p)
                st.link_button(f"📞 ПОЗВОНИТЬ {p}", f"tel:{clean_p}")
        else:
            st.warning("Номера не найдены.")
    else:
        st.error("Поле пустое!")

st.caption("Бизнес-платформа: ARV-04 | Режим Агрегатора Активен")
