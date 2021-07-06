import urllib.request as urllib2, psycopg2
from psycopg2 import Error

flag = False

tabel = {
    # 1: "user",
    # 2: "channel",
    # 3: "video",
    # 4: "comment"
}

print("Which one of these do you want to do it?")

counter = 0
for tab in tabel.values():
    counter += 1
    print(str(counter) + ": " + tab)

operate = int(input())

try:

    conn = psycopg2.connect(user="postgres",
                            password="amir20002004",
                            host="localhost",
                            port="5432",
                            database="youtube")
    print("connect to database")

    cursor = conn.cursor()

    data = {
        'username': "",
        'user_id': "",
        'name': "",
        'channel_name': "",
        'description': "",
        'construction_date': "",
        'video_id': "",
        'content': "",
        'is_like': "",
        'reply': "",
        'comment_id': "",
        'is_private': "",
        'channel_id': "",
        'upload_date': "",
        'duration': "",
        'image_thumbnail': "",
        'video_address': "",
        'is_watch': "",
        'password': "",
        'email': "",
        'image': "",
        'join_date': ""
    }

    # add user
    if operate == 1:
        print("Enter the characteristics of the person: ")
        data['username'] = str(input("username: "))
        data['password'] = str(input("password: "))
        data['email'] = str(input("email: "))
        data['image'] = str(input("photo: "))
        data['join_date'] = str(input("date of the joining: "))

        if not "@" in data.get('email'):
            print("Your email is not valid.")
        else:
            sql = """
                        SELECT username FROM "user" WHERE username = %(username)s OR email = %(email)s;
                """

            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()

            if len(output) > 0:
                print("This username or email is already registered.")

            else:
                sql = """ INSERT INTO "user" (username, password, email, image, join_date) VALUES
                         (%(username)s, crypt(%(password)s, gen_salt('bf')), %(email)s, %(image)s, %(join_date)s);"""

                cursor.execute(sql, data)
                conn.commit()

    # make a channel
    elif operate == 2:
        print("Fill the blanks (image is optional): ")
        data['username'] = str(input("username of creator: "))
        data['name'] = str(input("channel name: "))
        data['description'] = str(input("description: "))
        data['image'] = str(input("photo of channel: [Optional]"))
        data['construction_date'] = str(input("date of the constructing: "))

        if data['username'] == "" or data['name'] == "" or data['description'] == "" or data['construction_date'] == "":
            print("The required things still are blank.")
        else:
            sql = """
                        SELECT name FROM channel WHERE name = %(name)s ;
                        """
            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()

            if len(output) > 0:
                print("This channel is already created.")

            else:
                sql = """
                            SELECT user_id FROM "user" WHERE username = %(username)s ;
                            """

                output = []
                cursor.execute(sql, data)
                if cursor.fetchall():
                    output = cursor.fetchall()
                conn.commit()

                if len(output) > 0:
                    data['user_id'] = int(output[0][0])
                    sql = """ INSERT INTO channel (user_id, name, description, image, construction_date) VALUES
                                         (%(user_id)s, %(name)s, %(description)s, %(image)s, %(construction_date)s);"""

                    cursor.execute(sql, data)
                    conn.commit()

    # delete a channel and delete videos of the channel
    elif operate == 3:
        print("Fill the blanks: ")
        data['channel_name'] = str(input("name of the channel: "))

        if data['channel_name'] == "":
            print("The required thing(s) still are/is blank.")

        else:

            sql = """
                        SELECT channel_id FROM channel WHERE name = %(channel_name)s ;
                            """

            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()

            if len(output) > 0:
                data['channel_id'] = int(output[0][0])

                # delete the channel
                sql = """ DELETE FROM channe WHERE id = %(channel_id)s; """
                cursor.execute(sql, data)
                conn.commit()

                # delete comments of videos
                sql = """ SELECT id FROM video WHERE channel_id = %(channel_id)s; """
                output = []
                cursor.execute(sql, data)
                if cursor.fetchall():
                    output = cursor.fetchall()
                conn.commit()

                for i in range(output[0]):
                    data['video_id'] = output[0][i]
                    sql = """ DELETE FROM comment WHERE video_id = %(video_id)s; """
                    cursor.execute(sql, data)
                    conn.commit()

                # delete videos of the channel
                sql = """ DELETE FROM video WHERE channel_id = %(channel_id)s; """
                cursor.execute(sql, data)
                conn.commit()

    # upload a video
    elif operate == 4:
        print("Fill the blanks: ")
        data['channel_name'] = str(input("name of the channel: "))
        data['name'] = str(input("video name: "))
        data['description'] = str(input("description: "))
        data['image_thumbnail'] = str(input("photo of video: "))
        data['upload_date'] = str(input("date of the upload: "))
        data['duration'] = str(input("time of the video: "))
        data['video_address'] = str(input("address of the video: "))

        if data['channel_name'] == "" or data['name'] == "" or data['description'] == "" or data['image_thumbnail'] == ""\
                or data['upload_date'] == "" or data['duration'] == "" or data['video_address'] == "":

            print("The required things still are blank.")

        else:

            sql = """
                        SELECT channel_id FROM channel WHERE name = %(channel_name)s ;
                    """

            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()
            if len(output) > 0:
                data['channel_id'] = int(output[0][0])
                sql = """ INSERT INTO video (channel_id, name, description, image_thumbnail, upload_date, duration, video_address) VALUES
                         (%(channel_id)s, %(name)s, %(description)s, %(image_thimbnail)s, %(upload_date)s, %(duration)s,  %(video_address)s);"""

                cursor.execute(sql, data)
                conn.commit()

    # delete a video and delete comments of the video
    elif operate == 5:
        print("Fill the blanks: ")
        data['channel_name'] = str(input("name of the channel: "))
        data['name'] = str(input("video name: "))
        data['upload_date'] = str(input("date of the upload: "))

        if data['channel_name'] == "" or data['name'] == "" or data['upload_date'] == "":
            print("The required things still are blank.")

        else:

            sql = """
                        SELECT channel_id FROM channel WHERE name = %(channel_name)s ;
                    """

            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()
            if len(output) > 0:
                data['channel_id'] = int(output[0][0])
                sql = """
                            SELECT video_name FROM video WHERE name = %(name)s, upload_date = %(upload_date)s ;
                        """

                output = []
                cursor.execute(sql, data)
                if cursor.fetchall():
                    output = cursor.fetchall()
                conn.commit()
                if len(output) > 0:
                    sql = """ SELECT id FROM video WHERE channel_id = %(channel_id)s, name = %(name)s, upload_date = %(upload_date)s"""
                    output = []
                    cursor.execute(sql, data)
                    if cursor.fetchall():
                        output = cursor.fetchall()
                    conn.commit()

                    data['video_id'] = output[0][0]
                    sql = """ DELETE FROM video WHERE id = %(video_id)s; """
                    cursor.execute(sql, data)
                    conn.commit()

                    sql = """ DELETE FROM comment WHERE video_id = %(video_id)s; """
                    cursor.execute(sql, data)
                    conn.commit()

    # watch a video and like or dislike its
    elif operate == 6:
        print("Fill the blanks parts: ")
        data['username'] = str(input("username: "))
        data['video_id'] = str(input("video_id: "))
        # enter 1(like) or 2(dislike)
        data['is_like'] = int(input("like or dislike: \n 1) like \n 2) dislike"))
        data['is_watch'] = True

        if data['username'] == "" or data['video_id'] == "" or data['is_like'] == "":
            print("The required things still are blank.")

        else:
            if data['is_like'] == 1:
                data['is_like'] = True
            else:
                data['is_like'] = False


            sql = """
                        SELECT id FROM "user" WHERE username = %(username)s;
                    """

            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()

            if len(output) > 0:
                data['user_id'] = output[0][0]
                sql = """ INSERT INTO videoaction (user_id, video_id, is_like, is_watch) VALUES
                                (%(user_id)s, %(video_id)s, %(is_like)s, %(is_watch)s);"""

                cursor.execute(sql, data)
                conn.commit()

    # become member
    elif operate == 7:
        print("Fill the blanks: ")
        data['username'] = str(input("username: "))
        data['channel_name'] = str(input("channel name: "))
        data['join_date'] = str(input("date of the join: "))

        if data['username'] == "" or data['channel_name'] == "" or data['join_date'] == "":
            print("The required things still are blank.")

        else:

            sql = """
                        SELECT id FROM "user" WHERE username = %(username)s ;
                    """

            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()
            if len(output) > 0:
                data['user_id'] = int(output[0][0])
                sql = """ SELECT id FROM channel WHERE name = %(channel_name)s; """

                output = []
                cursor.execute(sql, data)
                if cursor.fetchall():
                    output = cursor.fetchall()
                conn.commit()
                if len(output) > 0:
                    data['channel_id'] = int(output[0][0])
                    sql = """ SELECT id FROM joinchannel WHERE user_id = %(user_id)s channel_id = %(channel_id)s;"""

                    output = []
                    cursor.execute(sql, data)
                    if cursor.fetchall():
                        output = cursor.fetchall()
                    conn.commit()
                    if len(output) > 0:
                        print("you are the member of this channel!")
                    else:
                        sql = """ INSERT INTO joinchannel (user_id, channel_id, join_date) VALUES (%(user_id)s, %(channel_id)s, %(join_date)s);"""

                        cursor.execute(sql, data)
                        conn.commit()
                else:
                    print("This channel is not valid!")
            else:
                print("This user is not valid!")

    # cancel the membership of a channel
    elif operate == 8:
        print("Fill the blanks: ")
        data['username'] = str(input("username: "))
        data['channel_name'] = str(input("channel name: "))

        if data['username'] == "" or data['channel_name'] == "":
            print("The required things still are blank.")

        else:
            sql = """SELECT id FROM "user" WHERE username = %(username)s ;"""

            output = []
            cursor.execute(sql, data)
            if cursor.fetchall():
                output = cursor.fetchall()
            conn.commit()
            if len(output) > 0:
                data['user_id'] = int(output[0][0])
                sql = """ SELECT id FROM channel WHERE name = %(channel_name)s; """

                output = []
                cursor.execute(sql, data)
                if cursor.fetchall():
                    output = cursor.fetchall()
                conn.commit()
                if len(output) > 0:
                    data['channel_id'] = int(output[0][0])
                    sql = """ SELECT id FROM joinchannel WHERE user_id = %(user_id)s channel_id = %(channel_id)s;"""

                    output = []
                    cursor.execute(sql, data)
                    if cursor.fetchall():
                        output = cursor.fetchall()
                    conn.commit()
                    if len(output) > 0:
                        sql = """ DELETE FROM joinchannel (user_id, channel_id) VALUES (%(user_id)s, %(channel_id)s);"""
                        cursor.execute(sql, data)
                        conn.commit()
                    else:
                        print("you are not the member of this channel!")

                else:
                    print("This channel is not valid!")
            else:
                print("This user is not valid!")
    # if flag == False:
    #     sql = """
    #                CREATE EXTENSION pgcrypto;
    #                INSERT INTO "user" (username, password, email, image, joindate) VALUES
    #                 (%(username)s, crypt('12345', gen_salt('bf')), %(email)s, %(image)s, %(joinDate)s);
    #                """
    # else:
    # sql = """
    #                    INSERT INTO "user" (username, password, email, image, joindate) VALUES
    #                     (%(username)s, crypt('12345', gen_salt('bf')), %(email)s, %(image)s, %(joinDate)s);
    #                    """
    # # flag = True
    #
    # data_insert = {
    #     'username': "emad",
    #     'email': "emad@gmail.com",
    #     'image': "emad.jpg",
    #     'joinDate': "2016-06-22 20:10:25-07"
    # }
    #
    # deleteSql = """
    #                    DELETE FROM "user" WHERE username = %(username)s;
    #                    """
    #
    # delete = {
    #     'username': "emad",
    #     'email': "emad@gmail.com",
    #     'image': "emad.jpg",
    #     'joinDate': "2016-06-22 20:10:25-07"
    # }
    #
    # updateSql = """
    #                    UPDATE public."user"
    #                    SET username=%(username)s, email=%(email)s, joindate=%(joinDate)s, image=%(image)s
    #                    WHERE username = %(old_username)s;
    #                        """
    #
    # update = {
    #     'username': "ali",
    #     'email': "emad@gmail.com",
    #     'image': "emad.jpg",
    #     'joinDate': "2016-06-22 20:10:25-07",
    #     'old_username': "amir"
    # }

    # cursor.execute(updateSql, update)
    # conn.commit()
    conn.close()


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
