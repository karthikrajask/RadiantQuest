import streamlit as st
import requests
from datetime import datetime

# 🔑 Replace with your own NewsAPI key
NEWS_API_KEY = "775836b2b9a54495bba579b5d42f38cf"

def fetch_solar_news(query="solar energy india"):
    """Fetch latest solar energy news in India using NewsAPI."""
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"language=en&"
        f"sortBy=publishedAt&"
        f"apiKey={NEWS_API_KEY}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error("⚠️ Could not fetch news at this time. Try again later.")
        return []

def show_news_page():
    st.title("📰 Solar News & Insights")
    st.markdown("Stay updated with the **latest solar energy developments in India** – from government schemes to manufacturing and grid updates.")

    # 🔍 Search bar
    user_query = st.text_input("🔍 Search Solar News", placeholder="e.g., solar panels, government policy, Adani...")

    # 📌 Category quick filters
    categories = ["General", "Policy", "Technology", "Industry", "International"]
    selected_category = st.radio("📌 Filter by Category:", categories, horizontal=True)

    # 🌍 State filter (no neighbours now)
    state_filter = st.selectbox(
        "📍 Filter by State",
        ["All India", "Tamil Nadu", "Kerala", "Karnataka", "Maharashtra", "Delhi", "Gujarat"],
        index=0
    )

    # Adjust query based on category
    if selected_category == "Policy":
        query = "solar policy india OR renewable energy policy"
    elif selected_category == "Technology":
        query = "solar technology india OR renewable innovation"
    elif selected_category == "Industry":
        query = "solar industry india OR renewable energy market"
    elif selected_category == "International":
        query = "solar energy world OR renewable global"
    else:
        query = "solar energy india OR renewable energy india"

    # If user searched something, override category
    if user_query.strip():
        query = user_query.strip()

    # If state selected (not "All India"), narrow query
    if state_filter != "All India":
        query = f"{state_filter} solar"

    # Fetch news
    articles = fetch_solar_news(query=query)

    # Fallback if no results
    if not articles and state_filter != "All India":
        st.warning(f"⚡ No recent solar news found for **{state_filter}**. Showing all-India news instead.")
        articles = fetch_solar_news(query="solar India")

    if not articles:
        st.info("⚡ No news available right now. Try another keyword or check later.")
        return

    # 📰 Show news cards
    for article in articles[:10]:  # Limit to 10 news items
        with st.container():
            st.subheader(article["title"])

            if article.get("urlToImage"):
                st.image(article["urlToImage"], use_container_width=True)

            published = article.get("publishedAt", "")
            if published:
                try:
                    published = datetime.fromisoformat(
                        published.replace("Z", "+00:00")
                    ).strftime("%d %b %Y, %I:%M %p")
                except Exception:
                    published = published

            st.caption(f"🗓 {published} | 📰 {article.get('source', {}).get('name', '')}")
            st.write(article.get("description", ""))
            st.markdown(f"[Read full article 🔗]({article['url']})")
            st.markdown("---")
