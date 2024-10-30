import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"




STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_APIKEY = "8A6I8XNZWGM2N48C"
parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_APIKEY

}
stock_request = requests.get(STOCK_ENDPOINT, params= parameters)
stock_request.raise_for_status()




stock_data = stock_request.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
yesterday_data = data_list[0]
yesterdays_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

print(yesterdays_closing_price, day_before_yesterday_closing_price)

difference =(float(yesterdays_closing_price) - float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterdays_closing_price))*100)
print(diff_percent)

count =2
stock_data_dates = []
for dates in stock_data:
    stock_data_dates = dates
    count +=1
    if count == 2:
        break
print(stock_data_dates)



NEWS_API_KEY = "1174fcc621674b2e94d0f60bfc16df17"
news_params = {
    "apiKey":NEWS_API_KEY,
    "q":COMPANY_NAME,

}
if abs(diff_percent) > 0:
    news_response = requests.get(NEWS_ENDPOINT,params= news_params )
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%: Headline: {article ['title']}. \n Brief: {article['description']}" for article in three_articles]

    account_sid = 'AC58191149a1437a08b7300fc9cc6828d0'
    auth_token = 'a11a1500740e9334394e6ec715c42d3b'
    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=article,
            to='whatsapp:+14045184625'
        )

        print(message.sid)


"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""