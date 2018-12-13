import sqlite3 as sql
from passlib.hash import sha256_crypt


def create():
    "create table if doesnot exist"
    try:
        with sql.connect("data.db") as con:
            con.execute('pragma foreign_keys = ON;')
            con.execute('''CREATE TABLE history (similarity INT NOT NULL,
                   file1 TEXT NOT NULL,
                   file2 TEXT NOT NULL,
                   ids INT references users(id));''')
    except:
        print("Table already exists")


def add_submission(user, sim, file1, file2):
    try:
        with sql.connect("data.db") as con:

            # create a cursor object
            cur = con.cursor()
            # query without concanating so that no sqlinjection
            sqlQuery = "select id from users where name ='%s';" % user
            cur.execute(sqlQuery)
            row = cur.fetchone()

            # if name already used donot create an account
            if row:
                cur.execute("INSERT INTO history (similarity, file1,file2,ids)  VALUES (?,?,?,?)",
                            (sim, file1, file2, row[0]))
                con.commit()
            else:
                # increment val to give it an id
                print("No such name")
    except:
        print("Unexpected Error in insert operation")


def get_all_submissions():
    try:
        with sql.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("select * from history where similarity is not null")
            rows = cur.fetchall()
            return rows
    except:
        print("connection failed")


def get_user_submissions(user):
    try:
        with sql.connect("data.db") as con:
            cur = con.cursor()
            sqlQuery = "select id from users where name ='%s';" % user
            cur.execute(sqlQuery)
            id1 = cur.fetchone()
            if id1:
                sqlQuery = "select * from history where ids = '%d';" % id1[0]
                cur.execute(sqlQuery)
                rows = cur.fetchall()
                return rows
            else:
                return []
    except:
        print("connection failed")
        return []


if __name__ == '__main__':
    create()
    add_submission('nis', 10, 'hcv1', 'hcv2')
    print(get_user_submissions('nis'))
