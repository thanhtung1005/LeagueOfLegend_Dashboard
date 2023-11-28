import pymysql

from app import db, createApp


connection = pymysql.connect(
    host='localhost',
    user='root',
    # Change your password here
    passwd='your_password'
)

app = createApp()
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS `lolchampions`;")
connection.close()
app.app_context().push()
db.drop_all()
db.create_all()
