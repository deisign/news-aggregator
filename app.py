import streamlit as st
import feedparser
from datetime import datetime

# --- Функции для работы с RSS ---
def fetch_rss_news(rss_feeds):
    news_list = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published if 'published' in entry else "Не указано",
                "source": feed_url
            })
    return news_list

# --- Данные: RSS ссылки ---
rss_feeds = [
    # Калмыкия
    'https://riakalm.ru/rss',
    'https://kalmykia-news.net/rss',
    'https://kalmtv.ru/rss',
    'https://vesti-kalmykia.ru/rss',
    'https://kalmykia-online.ru/rss',
    # Ингушетия
    'https://ingushmedia.ru/rss',  # Пример сайта для Ингушетии
    'https://fortanga.org/feed',
    'https://magastimes.ru/feed',
]

# --- Интерфейс Streamlit ---
st.title("Агрегатор новостей Калмыкии и Ингушетии")
st.sidebar.header("Фильтры")

# Получение данных из RSS
news = fetch_rss_news(rss_feeds)

# Фильтрация по источнику
sources = list(set([n['source'] for n in news]))
selected_sources = st.sidebar.multiselect("Выберите источники", options=sources, default=sources)

# Фильтрация по ключевым словам
keywords = st.sidebar.text_input("Фильтр по ключевым словам", "")

# Применение фильтров
filtered_news = [
    n for n in news
    if n['source'] in selected_sources and (keywords.lower() in n['title'].lower() or keywords == "")
]

# Отображение новостей
st.subheader(f"Найдено новостей: {len(filtered_news)}")
for item in filtered_news:
    st.markdown(f"### [{item['title']}]({item['link']})")
    st.markdown(f"*Источник:* {item['source']}")
    st.markdown(f"*Дата публикации:* {item['published']}")
    st.write("---")

# Информация о приложении
st.sidebar.info(
    """
    Это приложение создано для агрегирования новостей из регионов Калмыкия и Ингушетия.
    Источники: RSS-ленты указанных сайтов и агрегаторов.
    """
)
