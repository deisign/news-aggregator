import feedparser
import streamlit as st
import pandas as pd

# List of RSS feeds
RSS_FEEDS = {
    "Лента.ру — Калмыкия": "https://lenta.ru/rss/articles/russia/kalmykiya/",
    "Кавказский Узел — Ингушетия": "https://www.kavkaz-uzel.eu/rss/ingushetia",
    "Фортанга — Ингушетия": "https://fortanga.org/feed/",
    "Вести Калмыкия": "https://vesti-kalmykia.ru/feed/rss/news?format=feed",
}

# Function to fetch and parse RSS feed
def fetch_rss_feed(url):
    feed = feedparser.parse(url)
    if feed.bozo:
        st.error(f"Error fetching RSS feed: {url}")
        return None
    return feed

# Function to display news articles
def display_articles(feed, source_name):
    if not feed or not feed.entries:
        st.warning(f"No articles found for {source_name}.")
        return
    
    st.subheader(f"Новости из {source_name}")
    articles = [
        {"Заголовок": entry.title, "Дата": entry.published, "Ссылка": entry.link}
        for entry in feed.entries
    ]
    df = pd.DataFrame(articles)
    st.dataframe(df)

    for entry in feed.entries:
        st.markdown(f"**[{entry.title}]({entry.link})**")
        st.markdown(f"*Дата публикации*: {entry.published}")
        st.markdown("---")

# Streamlit app
st.title("Агрегатор новостей из Калмыкии и Ингушетии")

# Sidebar for feed selection
selected_feed = st.sidebar.selectbox("Выберите источник новостей", list(RSS_FEEDS.keys()))

# Fetch and display articles
if selected_feed:
    feed_url = RSS_FEEDS[selected_feed]
    feed = fetch_rss_feed(feed_url)
    display_articles(feed, selected_feed)
