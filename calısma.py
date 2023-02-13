
import numpy as np
import pandas as pd
import datetime as dt

# Değişkenler
#
# Invoice: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


df_ = pd.read_excel("online_retail_II.xlsx", sheet_name="Year 2010-2011")
df= df_.copy()
df
df.isnull().sum()
df.dropna(inplace=True)
df.describe().T
df= df[~df["Invoice"].str.contains("C", na= False)]
df.head()
df["InvoiceDate"].max()
today_date= dt.datetime(2011,12,11)
type(today_date)
df["TotalPrice"]= df["Quantity"] * df["Price"]

rfm = df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate:(today_date - InvoiceDate.max()).days,
                                     "Invoice": lambda Invoice : Invoice.nunique(),
                                     "TotalPrice": lambda TotalPrice: TotalPrice.sum()})
rfm.columns = ["recency","frequency" ,"monetary"]
rfm.describe().T
rfm["recency_score"]= pd.qcut(rfm["recency"],5 ,labels=[5,4,3,2,1])
rfm["monetary_score"]= pd.qcut(rfm["monetary"],5 , labels=[1, 2,3,4,5])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm
rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str)+
                    rfm["frequency_score"].astype(str))
rfm
seg_map= {
    r'[1-2][1-2]' : "hibernating",
    r'[1-2][3-4]' : "at_Risk",
    r'[1-2]5' : "cant_loose",
    r'3[1-2]' : "about_to_sleep",
    r'33' : "need_attention",
    r'[3-4][4-5]' : "loyal_customers",
    r'41' : "promising",
    r'51' : "new_customers",
    r'[4-5][2-3]' : "potential_loyalists",
    r'5[4-5]' : "champions"
}
rfm["segment"] = rfm["RFM_SCORE"].replace(seg_map, regex=True)
rfm[rfm["segment"]=="cant_loose"].head()
rfm.to_csv("rfm2.csv")