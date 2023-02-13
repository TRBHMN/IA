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

# def findrev(x):
#     for index, row in items.iterrows():
#         if x == index:
#             c = row['price_sold']
#             return c


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
puprofit = 0

for index, row in itemxprofit.iterrows():
    x = index
    for index, row in t.iterrows():
        if x == row['item']:
            c = t.loc[index, 'profit']
            itemxprofit.at[x, 'profit'] += c

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





# Add a title and intro text
st.title('Data Analysis')
st.text('This is a web app to explore purchasing data, and see some visual data of the processes.')

text = 'total revenue ==='
st.write(text, totalrev)
text = "total profit ==="
st.write(text, totalprofit)

st.write(t)
st.write(itemxprofit)



# https://www.youtube.com/watch?v=VqgUkExPvLY - interesting video which might be able to help with the code.