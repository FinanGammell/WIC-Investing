import requests
import csv
import time
from print import stocks

tickers = stocks
removed = []

output = []


for ticker in tickers:
        stock = ticker
        key = "DJXCSAQZKJCLJ0FI"

        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={stock}&apikey={key}'
        r = requests.get(url)
        income = r.json()
        try:
                y2022 = float(income["annualReports"][0]["totalRevenue"])
                y2021 = float(income["annualReports"][1]["totalRevenue"])
                y2020 = float(income["annualReports"][2]["totalRevenue"])
                y2019 = float(income["annualReports"][3]["totalRevenue"])
                y2018 = float(income["annualReports"][4]["totalRevenue"])

                avg_revenue_growth =(((y2022-y2021)/y2021)+((y2021-y2020)/y2020)+((y2020-y2019)/y2019)+((y2019-y2018)/y2018))/4
        except:
                avg_revenue_growth = "N/A"
        print("1.",avg_revenue_growth)

        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={stock}&apikey={key}'
        r = requests.get(url)
        earnings = r.json()
        try:
                y2023e = float(earnings["annualEarnings"][0]["reportedEPS"])
                y2022e = float(earnings["annualEarnings"][1]["reportedEPS"])
                y2021e = float(earnings["annualEarnings"][2]["reportedEPS"])
                y2020e = float(earnings["annualEarnings"][3]["reportedEPS"])
                y2019e = float(earnings["annualEarnings"][4]["reportedEPS"])
                y2018e = float(earnings["annualEarnings"][5]["reportedEPS"])
                
                avg_earnings_growth = (((y2023e-y2022e)/y2022e)+((y2022e-y2021e)/y2021e)+((y2021e-y2020e)/y2020e)+((y2020e-y2019e)/y2019e)+((y2019e-y2018e)/y2018e))/5
        except:
                avg_earnings_growth = "N/A"
        print("2.",avg_earnings_growth)

        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={stock}&apikey={key}'
        r = requests.get(url)
        balance = r.json()
        try:
                assets = float(balance["annualReports"][0]["totalCurrentAssets"])
                liabilities = float(balance["annualReports"][0]["totalCurrentLiabilities"])
                
                current_ratio = assets/liabilities
        except:
                current_ratio = "N/A"
        print("3.",current_ratio)

        try:
                total_debt = float(balance["annualReports"][0]["shortLongTermDebtTotal"])
                shareholder_equity = float(balance["annualReports"][0]["totalShareholderEquity"])

                de_ratio = total_debt/shareholder_equity
        except:
                de_ratio = "N/A"
        print("4.",de_ratio)
        
        try:
                net_income = float(income["annualReports"][0]["netIncome"])
                total_assets = float(balance["annualReports"][0]["totalAssets"])

                roa = net_income/total_assets
        except:
                roa = "N/A"
        print("5a.",roa)

        try:
                cogs = float(income["annualReports"][0]["costofGoodsAndServicesSold"])
                inv2022 = float(balance["annualReports"][0]["inventory"])
                inv2021 = float(balance["annualReports"][1]["inventory"])

                inventory_turnover = cogs/((inv2022+inv2021)/2)
        except:
                inventory_turnover = "N/A"
        print("5b.",inventory_turnover)

        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={stock}&apikey={key}'
        r = requests.get(url)
        price = r.json()
        try:
                stock_price = float(price["Weekly Adjusted Time Series"]["2023-10-06"]["5. adjusted close"])

                pe_ratio = stock_price/y2023e
        except:
                pe_ratio = "N/A"
        print("6a.",pe_ratio)

        try:
                outstanding_shares = float(balance["annualReports"][0]["commonStockSharesOutstanding"])

                pb_ratio = stock_price/(shareholder_equity/outstanding_shares)
        except:
                pb_ratio = "N/A"
        print("6b.",pb_ratio)

        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={stock}&apikey={key}'
        r = requests.get(url)
        cashflow = r.json()
        try:
                operating_cash_flow = float(cashflow["annualReports"][0]["operatingCashflow"])

                pcf_ratio = stock_price/(operating_cash_flow/outstanding_shares)
        except:
                pcf_ratio = "N/A"
        print("6c.",pcf_ratio)

        try:
                y2023p = stock_price
                y2022p = float(price["Weekly Adjusted Time Series"]["2022-10-07"]["5. adjusted close"])
                y2021p = float(price["Weekly Adjusted Time Series"]["2021-10-08"]["5. adjusted close"])
                y2020p = float(price["Weekly Adjusted Time Series"]["2020-10-09"]["5. adjusted close"])
                y2019p = float(price["Weekly Adjusted Time Series"]["2019-10-04"]["5. adjusted close"])
                y2018p = float(price["Weekly Adjusted Time Series"]["2018-10-05"]["5. adjusted close"])
                
                avg_annual_return = (((y2023p-y2022p)/y2022p) + ((y2022p-y2021p)/y2021p) + ((y2021p-y2020p)/y2020p) + ((y2020p-y2019p)/y2019p) + ((y2019p-y2018p)/y2018p))/5
        except:
                avg_annual_return = "N/A"        
        print(avg_annual_return)

        output.append([ticker, avg_revenue_growth, avg_earnings_growth, current_ratio, de_ratio, roa, inventory_turnover, pe_ratio, pb_ratio, pcf_ratio, avg_annual_return])
        time.sleep(2)

print(output)

file_path = 'fundamentals.tsv'

with open(file_path, 'w', newline='') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')
    writer.writerows([["ticker", "avg_revenue_growth", "avg_earnings_growth", "current_ratio", "de_ratio", "roa", "inventory_turnover", "pe_ratio", "pb_ratio", "pcf_ratio", "avg_annual_return"]]+output)

rank = {}
for item in tickers:
        rank[item] = 0
print(rank)

for i in range(1,11):
        intermediate_rank = []
        null_list = []

        if i == 1 or i == 2 or i == 3 or i == 5 or i == 6 or i == 10:
                state = True
        else:
                state = False
        
        for item in output:
                try:
                        intermediate_rank.append((float((item[i])),item[0]))
                except:
                        null_list.append((item[i],item[0]))

        intermediate_rank.sort(reverse=state)
        
        intermediate_rank = intermediate_rank + null_list
   
        print(i, intermediate_rank)

        if i == 1 or i == 2:
                multiplicity = 0.125
        if i == 3:
                multiplicity = 0.1
        if i == 4 or i == 6 or i == 8 or i == 9:
                multiplicity = 0.05
        if i == 5 or i == 7:
                multiplicity = 0.075
        if i == 10:
                multiplicity = 0.3

        for item in tickers:
                for index, tuple_item in enumerate(intermediate_rank):
                        if tuple_item[1] == item:
                                position = index
                                current_value = rank[item] 
                                rank[item] = current_value + position*multiplicity

ranked_dict = dict(sorted(rank.items(), key=lambda item: item[1]))
print(ranked_dict)

file_path = 'ranked.tsv'

with open(file_path, 'w') as file:
        file.write(f"TICKER\tSCORE\n")
        for ticker, score in ranked_dict.items():
                file.write(f"{ticker}\t{score}\n")