#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql.cursors
sns.set(rc={'figure.figsize':(10,5)})


lis = []
lis2= []
# Connect to the database
conn = pymysql.connect(
    host='learningcomputerscience.com',port=3306, user='test_remote', password='test_remote!',database='9_8_BT', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

# Create a cursor object
cursor = conn.cursor()

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

# Close the cursor and connection
cursor.close()
conn.close()

def findrev(x):
    for index, row in items.iterrows():
        if x == index:
            c = row['price_sold']
            return c

for index, row in total.iterrows():
    x = row['item']
    if row['quantity_bought'] == 0:
        total.loc[index, 'quantity_bought'] = 1
    if row['revenue'] == 0:
        total.loc[index, 'revenue'] = findrev(x)

totalrev= 0 
for index, rows in total['revenue']:
    totalrev = totalrev + row['revenue']

def findprofit(a,x,b):
    profit = 0
    for index, row in items.iterrows():
        if x == index:
            c = row['og_price']
            profit = (a - (b*c))
    return profit

totalprofit = 0.00
t = total
t['profit'] = 0
for index, row in t.iterrows():
    x = row['item']
    a = row['revenue']
    b = row['quantity_bought']
    g = float(findprofit(a,x,b))
    t.loc[index, 'profit'] = g
    totalprofit = totalprofit + g


itemxprofit = items
itemxprofit['profit'] = 0
puprofit = 0

for index, row in itemxprofit.iterrows():
    x = index
    for index, row in t.iterrows():
        if x == index:
            c = row['profit']
            puprofit += c
    itemxprofit.loc[x, 'profit'] = puprofit
    puprofit = 0

itemxprofit['bought'] = 0

for index, row in t.iterrows():
    x = row['item']
    c = row['quantity_bought']
    for index, row in itemxprofit.iterrows():
        if index == x:
            itemxprofit.at[index, 'bought'] += c




# Add a title and intro text
st.title('Data Analysis')
st.text('This is a web app to explore purchasing data, and see some visual data of the processes.')

text = 'total revenue ===', totalrev
st.write(text)
text = "total profit ===", totalprofit
st.text(text)

st.write(itemxprofit)



# https://www.youtube.com/watch?v=VqgUkExPvLY - interesting video which might be able to help with the code.