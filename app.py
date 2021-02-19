import mysql.connector
import json
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Docker!'


@app.route('/widgets', methods=['GET', 'POST'])
def get_widgets():
    mysqldb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        database="inventory"
    )
    cursor = mysqldb.cursor()
    cursor.execute("SELECT * FROM widgets")

    row_headers = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    json_data = []

    for result in results:
        json_data.append(dict(zip(row_headers, result)))

    cursor.close()

    return json.dumps(json_data)


@app.route('/add', methods=['POST'])
def set_widgets():
    mysqldb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        database="inventory"
    )
    cursor = mysqldb.cursor()
    json_data = request.get_json()

    cursor.execute(f'INSERT INTO widgets VALUES("{json_data["name"]}", "{json_data["description"]}")')
    mysqldb.commit()
    cursor.close()

    return 'item added'


@app.route('/db')
def db_init():
    mysqldb = mysql.connector.connect(
        host="mysqldb",
        user="root"
    )
    cursor = mysqldb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mysqldb = mysql.connector.connect(
        host="mysqldb",
        user="root",
        database="inventory"
    )
    cursor = mysqldb.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return 'init database'


if __name__ == "__main__":
    app.run(host="0.0.0.0")
