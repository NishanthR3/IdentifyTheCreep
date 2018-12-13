import sqlite3 as sql
from passlib.hash import sha256_crypt
from flask import session

val = [0]


def create():
    "create table if doesnot exist"
    try:
        with sql.connect("data.db") as con:
            con.execute('''CREATE TABLE users (name TEXT NOT NULL,
                   password TEXT NOT NULL,
                   id INT PRIMARY KEY NOT NULL);''')
    except:
        with sql.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("select count(*) from users")
            row = cur.fetchone()
            val[0] = row[0]


def register(request):
    "register new user"
    try:
        user = request.form['username']
        password = request.form['password']
        # hashing password
        password = sha256_crypt.encrypt(password)

        with sql.connect("data.db") as con:

            # create a cursor object
            cur = con.cursor()

            # query without concanating so that no sqlinjection
            cur.execute("select count(*) from users")
            row = cur.fetchone()
            val[0] = row[0]
            sqlQuery = "select name from users where name ='%s';" % user
            cur.execute(sqlQuery)
            row = cur.fetchone()
            # if name already used donot create an account
            if row:
                print(user)
                return False
            else:

                # increment val to give it an id
                val[0] += 1
                cur.execute("INSERT INTO users (name, password,id)  VALUES (?,?,?)",
                            (user, password, val[0]))
                con.commit()
                session['username'] = user
                return True
    except:
        return False


def allUsers():
    "output all users"
    try:
        with sql.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("select * from users where name is not null")
            rows = cur.fetchall()
            return rows
    except:
        return []


def authenticate(request):
    "authenticate usres"
    user = request.form['username']
    password = request.form['password']

    with sql.connect("data.db") as con:
        cur = con.cursor()

        sqlQuery = "select password from users where name ='%s';" % user
        cur.execute(sqlQuery)
        row = cur.fetchone()
        # initialize status to false
        status = False

        if row:
                # verify password
            session['username'] = user
            status = sha256_crypt.verify(password, row[0])
        return status


if __name__ == '__main__':
    create()
    tmp = ['nishanth', 'asjklajd']
    register(tmp)
    tmp = ['baby', 'asjklajd']
    register(tmp)
    allUsers()
    authenticate(tmp)
    tmp = ['nishanth', 'aldkalsdksldk']
    authenticate(tmp)
