#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql.cursors
import datetime 
from difflib import SequenceMatcher
sns.set(rc={'figure.figsize':(10,5)})

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
                try:
                    cursor.execute(sql, values)
                    conn.commit()
                except:
                    st.write("connection failed : didnt send")
                    # cursor.close()
                    # conn.close()

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



# ANALYSIS


st.markdown("<h1 style='text-align: center; color: red;'>Data Analysis</h1>", unsafe_allow_html=True)
st.write('This is a web app to explore purchasing data, and see some visual data of the processes.')

text = 'total revenue ==='
st.write(text, totalrev)
text = "total profit ==="
st.write(text, totalprofit)
st.write("Statistics from the day-to-day sales within the club are below...")
st.write(x)

# Search Bar
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons" icon-4x>{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

columm1, columm2 = st.columns(2, gap= "large")
with columm1:
    icon("search")
with columm2:
    st.write("Over here, you can search throughout the items, and find a specific product or another, if you want to look at all the products, and their statistics? Search ALL")
with st.form("Search Bar"):
    selected = st.text_input("", "ALL")
    colum1, colum2 = st.columns(2, gap= "large")
    with colum1:
        name_search = st.form_submit_button("Search in Product Names")
    with colum2:
        ID_search = st.form_submit_button("Search in ID Number")

#Table


with st.container():
    if selected == "ALL":
        st.write(itemxprofit)
    if selected != "":
        if name_search:
            List = []
            for index, row in itemxprofit.iterrows():
                similarity = SequenceMatcher(None, selected, index).ratio()
                # st.write(similarity)
                List.append([similarity, index])
            List.sort(key=lambda x: x[0])
            sorteditems = itemxprofit
            sorteditems['sim'] = 0
            for index, row in sorteditems.iterrows():
                for i in range(len(List)):
                    if index == List[i][1]:
                        sorteditems.loc[index, 'sim'] = List[i][0]
            sortitems = sorteditems.sort_values(by=['sim'], ascending=False)
            st.write(sortitems)
        elif ID_search:
            st.write(itemxprofit[itemxprofit['id'] == selected])


#Graphs
st.markdown("<h2 style='text-align: left; color: white;'>Graphs</h2>", unsafe_allow_html=True)
fig = plt.figure(figsize=(10, 4))
sns.scatterplot(x='bought', y='profit',hue='type', data = itemxprofit[itemxprofit.profit.between(50, 40000)])

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))

label_point(itemxprofit[itemxprofit.profit.between(50, 40000)].bought, itemxprofit[itemxprofit.profit.between(50, 40000)].profit, itemxprofit[itemxprofit.profit.between(50, 40000)].id, plt.gca())  

st.write("All products, and how many are bought, versus the profit they produce, of only the profit above 50")
st.pyplot(fig)


o = total
for index, row in o.iterrows():
    x = row['date']
    try:
        date_obj = datetime.datetime.strptime(x, "%A, %B %d, %Y")
        new_format = "%Y/%m/%d"
        new_date_string = date_obj.strftime(new_format)
        o.loc[index, 'date'] = new_date_string
    except:
        x = row['date']

x = o.groupby(['date'])['profit'].sum()
x = x.sort_index(ascending=True)

st.write("Profit over time is displayed here. Where it is the profit over every day that we have sold so far")
st.line_chart(data=x, x=index, y=['profit'], width=0, height=0, use_container_width=True)


# fig = plt.figure(figsize=(10, 4))
# sns.barplot(x='id',y='bought',data=itemxprofit[itemxprofit['bought']>10])
# st.pyplot(fig)

st.write("Over here, we have the distribution of products and how many of they are in the zone where they do not produce enough profit, and the density of that location")
fig = plt.figure(figsize=(10, 4))
sns.distplot(itemxprofit['profit'], kde=True)
st.pyplot(fig)

st.markdown("<h2 style='text-align: left; color: white;'>Make your own graph</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    pick = st.radio('Pick a y axis determinant', ('Profit per product','Revenue per product','Amount of things bought per product'))

    if pick == 'Profit per product':
        y_axis = 'profit'
    elif pick == 'Revenue per product':
        y_axis = 'revenue'
    elif pick == 'Amount of things bought per product':
        y_axis = 'bought'

with col2:
    pick2 = st.radio('Pick a x axis determinant', ('Type of product (Snack, Drink, Utility)','Item'))
    if pick2 == 'Item':
        x_axis = 'name'
    elif pick2 == 'Type of product (Snack, Drink, Utility)':
        x_axis = 'type'

with st.container():
    result = st.button("Click here to make the graph")
    if result:
        st.write('Bar graph, ', x_axis, " vs, ", y_axis)
        pro = itemxprofit.groupby([x_axis])[y_axis].sum().to_frame()
        st.bar_chart(data=pro, x = index, y= [y_axis])



# https://www.youtube.com/watch?v=VqgUkExPvLY - interesting video which might be able to help with the code.