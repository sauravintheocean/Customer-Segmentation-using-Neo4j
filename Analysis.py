import pandas as pd
#import modules
import matplotlib.pyplot as plt # for plotting graphs
import seaborn as sns # for plotting graphs
import datetime as dt




#df1 = pd.read_csv("CSP554/data.csv", encoding= 'unicode_escape')
data = pd.read_excel("Online Retail.xlsx")
data.head()
data.info()

data.isnull().sum()

filtered_data=data[['Country','CustomerID']].drop_duplicates()
test = data['CustomerID'].drop_duplicates()

filtered_data.Country.value_counts()[:5].plot(kind='bar')

uk_data=data[data.Country=='United Kingdom']
uk_data.info()
uk_data.describe()

uk_data = uk_data[(uk_data['Quantity']>0)]

uk_data=uk_data[['CustomerID','InvoiceDate','InvoiceNo','Quantity','UnitPrice']]
uk_data['TotalPrice'] = uk_data['Quantity'] * uk_data['UnitPrice']
uk_data['InvoiceDate'].min(),uk_data['InvoiceDate'].max()
PRESENT = dt.datetime(2011,12,10)
uk_data['InvoiceDate'] = pd.to_datetime(uk_data['InvoiceDate'])

uk_data.info()

uk_data.head()

rfm= uk_data.groupby('CustomerID').agg({'InvoiceDate': lambda date: (PRESENT - date.max()).days,
                                        'InvoiceNo': lambda num: len(num),
                                        'TotalPrice': lambda price: price.sum()})

rfm.columns

rfm.columns=['monetary','frequency','recency']

rfm.info()

rfm['recency'] = rfm['recency'].astype(int)

rfm.info()

rfm.head()

rfm['r_quartile'] = pd.qcut(rfm['recency'], 4, ['1','2','3','4'])
rfm['f_quartile'] = pd.qcut(rfm['frequency'], 4, ['4','3','2','1'])
rfm['m_quartile'] = pd.qcut(rfm['monetary'], 4, ['4','3','2','1'])

rfm.head()

rfm['RFM_Score'] = rfm.r_quartile.astype(str)+ rfm.f_quartile.astype(str) + rfm.m_quartile.astype(str)
rfm.head()

rfm[rfm['RFM_Score']=='111'].sort_values('monetary', ascending=False).head()




