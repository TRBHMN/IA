#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql.cursors
import datetime 
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





# Add a title and intro text
st.title('Data Analysis')
st.text('This is a web app to explore purchasing data, and see some visual data of the processes.')

text = 'total revenue ==='
st.write(text, totalrev)
text = "total profit ==="
st.write(text, totalprofit)

with st.container():
    st.write(itemxprofit)

st.header("Analysis")
fig = plt.figure(figsize=(10, 4))
sns.scatterplot(x='bought', y='profit',hue='type', data = itemxprofit[itemxprofit.profit.between(50, 40000)])

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

label_point(itemxprofit[itemxprofit.profit.between(50, 40000)].bought, itemxprofit[itemxprofit.profit.between(50, 40000)].profit, itemxprofit[itemxprofit.profit.between(50, 40000)].id, plt.gca())  

st.write("All products, and how many are bought, versus the profit they produce, of only the profit above 50")
st.pyplot(fig)

# sns.barplot(x='id',y='bought',data=itemxprofit)
# st.pyplot(fig)

# st.text("Histogram of all of the products")
# sns.distplot(itemxprofit['profit'], kde=True)
# st.pyplot(fig)
o = total
for index, row in o.iterrows():
    x = row['date']
    date_obj = datetime.datetime.strptime(x, "%A, %B %d, %Y")
    new_format = "%Y/%m/%d"
    new_date_string = date_obj.strftime(new_format)
    o.loc[index, 'date'] = new_date_string
    x = row['date']

x = o.groupby(['date'])['profit'].sum()
x = x.sort_index(ascending=True)

st.write("Profit over time is displayed here. Where it is the profit over every day that we have sold so far")
st.line_chart(data=x, x=index, y=['profit'], width=0, height=0, use_container_width=True)


fig = plt.figure(figsize=(10, 4))
sns.barplot(x='id',y='bought',data=itemxprofit[itemxprofit['bought']>10])
st.pyplot(fig)

fig = plt.figure(figsize=(10, 4))
sns.distplot(itemxprofit['profit'], kde=True)
st.pyplot(fig)

pick = st.radio('Pick a y axis determinant', ('Profit per product','Revenue per product','Amount of things bought per product'))

if pick == 'Profit per product':
    y_axis = ['profit']
elif pick == 'Profit per product':
    y_axis = ['revenue']
elif pick == 'Amount of things bought per product':
    y_axis = ['bought']

pick2 = st.radio('Pick a x axis determinant', ('Type of product (Snack, Drink, Utility)','Date','Original price of the product','Price that the product is sold at', 'Profit per product','Revenue per product','Amount of things bought per product'))
if pick == 'Profit per product':
    x_axis = ['profit']
elif pick == 'Profit per product':
    x_axis = ['revenue']
elif pick == 'Amount of things bought per product':
    x_axis = ['bought']
elif pick == 'Type of product (Snack, Drink, Utility)':
    x_axis = ['type']
elif pick == 'Date':
    x_axis = ['date']
elif pick == 'Price that the product is sold at':
    x_axis = ['price_sold']
elif pick2 == "Original price of the product":
    x_axis = ['og_price']

pick3 = st.radio('Pick the type of graph you would like to display', ("Bar graph", "Line Graph", 'Scatterplot'))


if st.button("Click here to make the graph"):
    if pick3 == 'Bar Graph':
        st.write('Bar graph, ', x_axis, " vs, ", y_axis)
        st.bar_chart(data=itemxprofit, x = x_axis, y= y_axis)
    if pick3 == "Line Graph":
        st.line_chart(data=itemxprofit, x = x_axis, y= y_axis)
# if pick3 == 'Scatterplot':




# https://www.youtube.com/watch?v=VqgUkExPvLY - interesting video which might be able to help with the code.