import requests
import datetime
from twilio.rest import Client
import os
import datetime as dt

API_PRICES_KEY = os.environ['API_PRICES_KEY']
API_NEWS_KEY = os.environ['API_NEWS_KEY']
account_sid = os.environ['ACCOUNT_SID']
auth_token = os.environ['AUTH_TOKEN']
my_nr = os.environ['MY_NR']


time_now = dt.datetime.now().date()
STOCK = "TSLA"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
URL_NEWS = f"https://newsapi.org/v2/everything?q=tesla&from={time_now}&sortBy=publishedAt&apiKey={API_NEWS_KEY}"
URL_STOCK_PRICES = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&interval=5min&apikey={API_PRICES_KEY}'


r = requests.get(URL_STOCK_PRICES)
data = r.json()

yesterday = datetime.date.today() - datetime.timedelta(days=1)
before_yesterday = datetime.date.today() - datetime.timedelta(days=2)
data_yesterday = data['Time Series (Daily)'][f"{yesterday}"]['4. close']
data_before_yesterday = data['Time Series (Daily)'][f"{before_yesterday}"]['4. close']

difference = float(data_yesterday) - float(data_before_yesterday)
percent = float(str.format("{0:.2f}", 100 * difference/float(data_before_yesterday)))


def check_news():
    news_request = requests.get(URL_NEWS)
    data_news = news_request.json()

    news = data_news['articles'][:3]
    news_titles = []

    for article in news:
        news_titles.append(article["title"] + "\n" + article["url"])

    return "\n\n".join(news_titles)


def send_message(text):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'{text}',
        from_='+19894991090',
        to='my_nr'
    )

    print(message.status)


if percent <= -2:
    text = f"😰Tesla stock price dropped down by 🔻{percent}%\n"\
           f"Last price on close: {data_yesterday}$\n"\
           f"{check_news()}"
    send_message(text)
elif percent >= 2:
    text = f"😊Tesla stock price rice up by 🔺{percent}%\n"\
           f"Last price on close: {data_yesterday}$"\
           f"{check_news()}"
    send_message(text)



