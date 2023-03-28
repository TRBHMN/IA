import streamlit

#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql.cursors
import datetime 
from difflib import SequenceMatcher
sns.set(rc={'figure.figsize':(10,5)})


lis = []
lis2= []
# Connect to the database
conn = pymysql.connect(
    host='learningcomputerscience.com',port=3306, user='test_remote', password='test_remote!',database='9_8_BT', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

# Create a cursor object
cursor = conn.cursor()

with st.sidebar:
    add_item = st.button("Would you like to add a new item to the inventory?")
    if add_item:
        with st.form("my_form"):
            add_type = st.radio(
                "Choose the type of product it would be...",
                ("Snack", "Drink", "Utility"))
            if add_type == "Snack":
                typ = 'snacks'
            elif add_type == "Drink":
                typ = 'drinks'
            elif add_type == "Utility":
                typ = 'utilities'
            IDn =107
            st.write(IDn)
            add_name = st.text_input("", "Name of product?")
            add_og_price = st.number_input("What is the orignial price of the product", value=0.0, step=0.1)
            add_price_sold = st.number_input("What is the price you want to sell the product for?", value=0.0, step=0.1)
            sent = st.form_submit_button("Publish/Send off to the inventory")
                
            if sent:
                cursor = conn.cursor()
                sql = "INSERT INTO items (name, id, price_sold, type, og_price) VALUES (%s, %s, %s, %s, %s)"
                values = (add_name, IDn, add_price_sold, typ, add_og_price)
cursor.execute(sql, values)
conn.commit()

# Execute a SELECT query
cursor.execute("SELECT * FROM recipt")
results = cursor.fetchall()
for result in results:
    # print(result)
    lis.append(result)
total = pd.DataFrame.from_dict(lis)

cursor.execute("SELECT * FROM items")
results = cursor.fetchall()
for result in results:
    # print(result)
    lis2.append(result)
items = pd.DataFrame.from_dict(lis2)
items = items.set_index("name")

conn.close()

for index, row in total.iterrows():
    x = row['item']
    y = index
    if row['quantity_bought'] == 0:
        total.loc[index, 'quantity_bought'] = 1
    if row['revenue'] == 0:
        for index, row in items.iterrows():
            if index == x:
                c = row['price_sold']
                total.loc[y, 'revenue'] = c

t = total
t['profit'] = 0
profit = 0
for index, row in t.iterrows():
    y = index
    x = row['item']
    a = row['revenue']
    b = row['quantity_bought']
    for index, row in items.iterrows():
        if x == index:
            c = row['og_price']
            profit = (a - (b*c))
            t.loc[y, 'profit'] = profit

itemxprofit = items
itemxprofit['profit'] = 0
itemxprofit['revenue'] = 0
puprofit = 0

for index, row in itemxprofit.iterrows():
    x = index
    for index, row in t.iterrows():
        if x == row['item']:
            c = t.loc[index, 'profit']
            y = t.loc[index, 'revenue']
            itemxprofit.at[x, 'profit'] += c
            itemxprofit.at[x, 'revenue'] += y

itemxprofit['bought'] = 0

for index, row in t.iterrows():
    x = row['item']
    c = row['quantity_bought']
    for index, row in itemxprofit.iterrows():
        if index == x:
            itemxprofit.at[index, 'bought'] += c

totalrev= 0 
totalprofit = 0
for index, rows in t.iterrows():
    totalrev = totalrev + t.loc[index,'revenue']
    totalprofit = totalprofit + t.loc[index,'profit']


o = total
for index, row in o.iterrows():
    x = row['date']
    date_obj = datetime.datetime.strptime(x, "%A, %B %d, %Y")
    new_format = "%Y/%m/%d"
    new_date_string = date_obj.strftime(new_format)
    o.loc[index, 'date'] = new_date_string

o = o.round(decimals = 2)
x = o.groupby(['date'])['profit','revenue'].sum()
x = x.sort_index(ascending=False)


st.write(total)