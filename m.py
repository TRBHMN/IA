import pymysql

# Connect to the database
conn = pymysql.connect(
    host='learningcomputerscience.com',port=3306, user='9_8_BT', password='linuxASW!',database='9_8_BT'
)

# Create a cursor object
cursor = conn.cursor()

# Execute a SELECT query
cursor.execute("SELECT * FROM recipt")

# Fetch the results
results = cursor.fetchall()

# Loop through the results
for result in results:
    print(result)

# Close the cursor and connection
cursor.close()
conn.close()