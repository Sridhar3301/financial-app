import os
import requests
from dotenv import load_dotenv


load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def get_company_news(company_name: str, limit: int = 5):
    """
    Fetch recent real news articles specifically related to a company.
    """

    if not NEWS_API_KEY:
        return {
            "error": "NEWS_API_KEY is not configured."
        }

    url = "https://newsapi.org/v2/everything"

    # Exact company-name search
    query = f'"{company_name}"'

    params = {
        "q": query,
        "searchIn": "title,description",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit,
        "apiKey": NEWS_API_KEY,
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        articles = []

        for article in data.get("articles", []):

            articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt"),
                "url": article.get("url"),
            })

        return articles

    except requests.RequestException as e:

        return {
            "error": str(e)
        }