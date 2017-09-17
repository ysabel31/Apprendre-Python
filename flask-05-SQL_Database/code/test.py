import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

'''
#drop_table = "DROP TABLE users"
#cursor.execute(drop_table)

#create_table = "CREATE TABLE users( id int, username text,password text)"
#cursor.execute(create_table)

# 1 row
#user = (1,'jose','asdf')
#cursor.execute(insert_query,user)

#connection.commit
'''

# Many users
users = [   
            (1,'jose','asdf'),
            (2,'rolf','trol'),
            (3,'anne','gobelin')
        ]
insert_query = "INSERT INTO users VALUES (?, ?, ?)"

cursor.executemany(insert_query,users)
connection.commit()

select_query = "SELECT id,username,password FROM USERS"    
#print("debut select")
for row in cursor.execute(select_query):
    print(row)
#print("fin select")
connection.close()