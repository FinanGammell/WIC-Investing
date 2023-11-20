import requests
import csv
import time

tsv_file = "ETF.tsv"

tickers = []

with open(tsv_file, 'r', newline='') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    next(tsv_reader)
    for row in tsv_reader:
        tickers.append(row[0])

passed = []

tsv_file = "stage1.tsv"
with open(tsv_file, 'w', newline='') as file:
    file.write(f"TICKER\t6m\t1y\t5y\t10y\tSTATUS\n")

    

def update(content):
    tsv_file = "stage1.tsv"
    with open(tsv_file, 'a', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(content)
        

for ticker in tickers:
    try:
        stock = ticker
        key = "DJXCSAQZKJCLJ0FI"
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={stock}&apikey={key}'
        r = requests.get(url)
        data = r.json()

        dates = ["2023-10-06","2023-04-06","2022-10-07","2018-10-05","2013-10-04"]

        today = float(data["Weekly Adjusted Time Series"][dates[0]]["5. adjusted close"])

        def percent_change(interval):
            try:
                close = float(data["Weekly Adjusted Time Series"][dates[interval]]["5. adjusted close"])
                return [close, (today-close)/close]
            except:
                return ["N/A", 0]

        intervals = dict(m6 = percent_change(1)[1], y1 = percent_change(2)[1], y5 = percent_change(3)[1], y10 = percent_change(4)[1])

        references = dict(m6 = 0.04, y1 = 0.15, y5 = 0.5, y10 = 1.5)

        exceed = 0
        results = []
        for item in intervals:
            results.append(intervals[item])

            if intervals[item] > references[item]:
                exceed = exceed + 1

        if exceed >= 3:
            print(f"{stock} Passed")
            update([stock]+results+["Passed"])
            passed.append(stock)

        else:
            print(f"{stock} did not Pass")
            update([stock]+results+["Failed"])

    except:
        print(f"{stock} not present in data base.")
        update([stock,"N/A","N/A","N/A","N/A","Not present in data base."])

    time.sleep(2)


print(passed)