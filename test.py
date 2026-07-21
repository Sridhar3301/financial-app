from services.market_data import get_market_data
from services.news_data import get_company_news


print("\n========== MARKET DATA ==========\n")

market_data = get_market_data("INFY.NS")

print(market_data)


print("\n========== NEWS ==========\n")

news = get_company_news("Infosys")

print(news)