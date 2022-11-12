import psycopg2
import psycopg2.extras
from .config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME

print(f'Make sure that the "Backend Server" is using the same database "{DATABASE_NAME}"')
#connect to the db 
conn = psycopg2.connect(
            host = DATABASE_HOST,
            database=DATABASE_NAME,
            user = DATABASE_USERNAME,
            password = DATABASE_PASSWORD)

#cursor 
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print('Connecting to the PostgreSQL database...')

cur.execute('SELECT version()')

db_version = cur.fetchone()

print(f'The surrent postgresql version is {db_version}')
#commit the transcation 
# con.commit()

#close the cursor
# cur.close()

#close the connection
# con.close()