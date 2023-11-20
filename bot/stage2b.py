import requests
from print import etfs
import csv

tickers = etfs

output = []

for ticker in tickers:
        stock = ticker
        key = "DJXCSAQZKJCLJ0FI"
        
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={stock}&apikey={key}'
        r = requests.get(url)
        price = r.json()

        try:
                y2023p = float(price["Weekly Adjusted Time Series"]["2023-10-06"]["5. adjusted close"])
                y2022p = float(price["Weekly Adjusted Time Series"]["2022-10-07"]["5. adjusted close"])
                y2021p = float(price["Weekly Adjusted Time Series"]["2021-10-08"]["5. adjusted close"])
                y2020p = float(price["Weekly Adjusted Time Series"]["2020-10-09"]["5. adjusted close"])
                y2019p = float(price["Weekly Adjusted Time Series"]["2019-10-04"]["5. adjusted close"])
                y2018p = float(price["Weekly Adjusted Time Series"]["2018-10-05"]["5. adjusted close"])
                
                avg_annual_return = (((y2023p-y2022p)/y2022p) + ((y2022p-y2021p)/y2021p) + ((y2021p-y2020p)/y2020p) + ((y2020p-y2019p)/y2019p) + ((y2019p-y2018p)/y2018p))/5
        except:
                avg_annual_return = "N/A"  
                      
        output.append((ticker, avg_annual_return))


sorted_list = sorted(output, key=lambda x: x[1], reverse=True)

file_path = 'etfs_returns.tsv'

with open(file_path, 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    tsvfile.write(f"TICKER\tRETURN\n")
    for item in sorted_list:
        writer.writerow([item[0], item[1]])

print(sorted_list)