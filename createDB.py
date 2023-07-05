import pymysql

from app import db, createApp
from app.models import Champion


connection = pymysql.connect(
    host='localhost',
    user='root',
    passwd='your_password'
)

app = createApp()
cursor = connection.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS `lolchampions`;")
connection.close()
app.app_context().push()
db.drop_all()
db.create_all()
