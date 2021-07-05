import urllib.request as urllib2, psycopg2
from psycopg2 import Error

flag = False

try:
    conn = psycopg2.connect(user="postgres",
                            password="amir20002004",
                            host="localhost",
                            port="5432",
                            database="youtube")
    print("connect to database")

    # if flag == False:
    #     sql = """
    #                CREATE EXTENSION pgcrypto;
    #                INSERT INTO "user" (username, password, email, image, joindate) VALUES
    #                 (%(username)s, crypt('12345', gen_salt('bf')), %(email)s, %(image)s, %(joinDate)s);
    #                """
    # else:
    sql = """
                       INSERT INTO "user" (username, password, email, image, joindate) VALUES
                        (%(username)s, crypt('12345', gen_salt('bf')), %(email)s, %(image)s, %(joinDate)s);
                       """
    # flag = True

    data_insert = {
                      'username': "emad",
                      'email': "emad@gmail.com",
                      'image': "emad.jpg",
                      'joinDate': "2016-06-22 20:10:25-07"
    }

    deleteSql = """
                       DELETE FROM "user" WHERE username = %(username)s;
                       """

    delete = {
        'username': "emad",
        'email': "emad@gmail.com",
        'image': "emad.jpg",
        'joinDate': "2016-06-22 20:10:25-07"
    }

    updateSql = """
                           UPDATE public."user"
                           SET username=%(username)s, email=%(email)s, joindate=%(joinDate)s, image=%(image)s
                           WHERE username = %(old_username)s;
                           """

    update = {
        'username': "ali",
        'email': "emad@gmail.com",
        'image': "emad.jpg",
        'joinDate': "2016-06-22 20:10:25-07",
        'old_username': "amir"
    }

    cursor = conn.cursor()
    cursor.execute(updateSql, update)
    conn.commit()
    conn.close()


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

