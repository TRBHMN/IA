import pymysql.cursors
import pandas as pd


lis = []

# Connect to the database
conn = pymysql.connect(
    host='learningcomputerscience.com',port=3306, user='test_remote', password='test_remote!',database='9_8_BT', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

# Create a cursor object
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM recipt")

# Fetch the results
results = cursor.fetchall()

# Loop through the results
for result in results:
    # print(result)
    for i in lis:
        lis[i] = result

total = pd.DataFrame.from_dict(lis)

print(total)

# Close the cursor and connection
cursor.close()
conn.close()