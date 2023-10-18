import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)

headers = {'User-Agent': "email@address.com"}
cik_ticker = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers)

#change to dictionary
cik_ticker_dict = cik_ticker.json()

#return the number & list of securities/companies that the api provides
df = pd.DataFrame.from_dict(cik_ticker_dict,orient='index')
df['cik_str'] = df['cik_str'].astype(str).str.zfill(10)
cik = df.at[df.index[0],'cik_str']

#print(df)
#sys.exit()

# get company facts data using the cik you get from above for a particular company
company_facts = requests.get(
    f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
    headers=headers
    )

# filing metadata
#print(company_facts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['label'])
#print(company_facts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['description'])
#print(company_facts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units'])
df = pd.DataFrame(company_facts.json()['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'])
#print(df)
#sys.exit()

# concept data // financial statement line items
accounting_fig = company_facts.json()['facts']['us-gaap']
#for k, v in accounting_fig.items():
#   print(k)


# different amounts of data available per concept['Revenues']['units']['USD'])
#df = pd.DataFrame(company_facts.json()['facts']['us-gaap']['AccountsPayable']['Revenues']['units']['USD'])
#df = pd.DataFrame(company_facts.json()['facts']['us-gaap']['Revenues']['units']['USD'])
#df = pd.DataFrame(company_facts.json()['facts']['us-gaap']['Assets']
# print(df)

# get company concept data e.g. Assets / Account Payable / or others
companyConcept = requests.get(
    (
    f'https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}'
     #f'/us-gaap/AccountsPayableCurrent.json'
     f'/us-gaap/Assets.json'
    ),
    headers=headers
    )

# get all filings data
df = pd.DataFrame.from_dict((companyConcept.json()['units']['USD']))

# get assets from 10Q forms and reset index
df = df[df['form'] == '10-Q']
df = df.reset_index(drop=True)
print(df)

# plot a line chart
df.plot(x='end', y='val')
plt.show()