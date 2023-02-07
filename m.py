import pymysql.cursors

# Connect to the database
conn = pymysql.connect(
    host='learningcomputerscience.com',port=3306, user='9_8_BT', password='linuxASW!',database='9_8_BT', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

# Create a cursor object
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT ID FROM recipt")

# Fetch the results
results = cursor.fetchall()

# Loop through the results
for result in results:
    print(result)

# Close the cursor and connection
cursor.close()
conn.close()