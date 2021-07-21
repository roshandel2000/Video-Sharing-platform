import random
import string
import urllib.request as urllib2, psycopg2
from datetime import datetime

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

operation = int(input())

try:

    conn = psycopg2.connect(user="postgres",
                            password="amir20002004",
                            host="localhost",
                            port="5432",
                            database="videoSharingPlatform")
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

    allowTypes = ['jpg', 'png', 'jpeg', 'gif']

    # add user
    if operation == 1:
        print("Enter the characteristics of the person: ")
        data['username'] = str(input("username: "))
        data['password'] = str(input("password: "))
        data['email'] = str(input("email: "))
        data['image'] = str(input("photo: "))
        data['join_date'] = str(input("date of the joining: "))

        # check the data that are not blank
        if data['username'] == "" or data['password'] == "" or data['email'] == "" or data['image'] == "" or data['join_date'] == "":
            print("The required things still are blank.")

        else:
            # check the format of email
            if not ("@" in data.get('email')):
                print("Your email is not valid!")

            # check the format of image
            elif not (data['image'].split('.')[1] in allowTypes):
                print("The image format is not valid!")

            else:
                sql = """SELECT username FROM "user" WHERE username = %(username)s OR email = %(email)s;"""

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check the entrance username is not duplicate
                if len(output) > 0:
                    print("This username or email is already registered!")

                # insert the new user into db
                else:
                    sql = """ INSERT INTO "user" (username, password, email, image, join_date) VALUES
                             (%(username)s, crypt(%(password)s, gen_salt('bf')), %(email)s, %(image)s, %(join_date)s);"""

                    cursor.execute(sql, data)
                    conn.commit()

    # make a channel
    elif operation == 2:
        print("Fill the blanks (image is optional): ")
        data['username'] = str(input("username of creator: "))
        data['channel_name'] = str(input("channel name: "))
        data['description'] = str(input("description: "))
        data['image'] = str(input("photo of channel: [Optional] "))
        data['construction_date'] = str(input("date of the constructing: "))

        # check the data that are not blank
        if data['username'] == "" or data['channel_name'] == "" or data['description'] == "" or data['construction_date'] == "":
            print("The required things still are blank.")

        else:

            # check the format of image
            if len(data['image']) > 0 and not (data['image'].split('.')[1] in allowTypes):
                print("The image format is not valid!")

            else:
                sql = """SELECT name FROM channel WHERE name = %(channel_name)s;"""

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check the name of channel that is not duplicate
                if len(output) > 0:
                    print("This channel is already created.")

                else:
                    sql = """SELECT id FROM "user" WHERE username = %(username)s ;"""

                    cursor.execute(sql, data)
                    output = cursor.fetchall()
                    conn.commit()

                    # check validation of the user
                    if len(output) > 0:
                        data['user_id'] = int(output[0][0])

                        # insert the new channel into db
                        sql = """ INSERT INTO channel (user_id, name, description, image, construction_date) VALUES
                                             (%(user_id)s, %(channel_name)s, %(description)s, %(image)s, %(construction_date)s);"""

                        cursor.execute(sql, data)
                        conn.commit()
                    else:
                        print("This user is not valid!")

    # delete a channel and delete videos of the channel
    elif operation == 3:
        print("Fill the blanks: ")
        # data['channel_name'] = str(input("name of the channel: "))

        # check the data that are not blank
        if data['channel_name'] == "":
            print("The required thing(s) still are/is blank.")

        else:

            sql = """SELECT id FROM channel WHERE name = %(channel_name)s ;"""

            cursor.execute(sql, data)
            output = cursor.fetchall()
            conn.commit()

            # check the validation of channel
            if len(output) > 0:
                data['channel_id'] = int(output[0][0])

                # delete comments of videos from db
                sql = """ SELECT id FROM video WHERE channel_id = %(channel_id)s; """
                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                for i in range(len(output[0])):
                    data['video_id'] = output[0][i]
                    sql = """ DELETE FROM comment WHERE video_id = %(video_id)s; """
                    cursor.execute(sql, data)
                    conn.commit()

                # delete videos of the channel from db
                sql = """ DELETE FROM video WHERE channel_id = %(channel_id)s; """
                cursor.execute(sql, data)
                conn.commit()

                # delete the channel from db
                sql = """ DELETE FROM channel WHERE id = %(channel_id)s; """
                cursor.execute(sql, data)
                conn.commit()

            else:
                print("This channel is not valid!")

    # upload a video
    elif operation == 4:
        print("Fill the blanks: ")
        data['channel_name'] = str(input("name of the channel: "))
        data['name'] = str(input("video name: "))
        data['description'] = str(input("description: "))
        data['image_thumbnail'] = str(input("photo of video: "))
        data['upload_date'] = str(input("date of the upload: "))
        data['duration'] = str(input("time of the video: "))
        data['video_address'] = str(input("address of the video: "))

        # check the data that are not blank
        if data['channel_name'] == "" or data['name'] == "" or data['description'] == "" or data['image_thumbnail'] == ""\
                or data['upload_date'] == "" or data['duration'] == "" or data['video_address'] == "":

            print("The required things still are blank.")

        else:

            # check the format of image
            if not (data['image_thumbnail'].split('.')[1] in allowTypes):
                print("The image format is not valid!")

            else:

                sql = """SELECT id FROM channel WHERE name = %(channel_name)s;"""

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check the validation of the channel
                if len(output) > 0:
                    data['channel_id'] = int(output[0][0])

                    # insert the video into db
                    sql = """ INSERT INTO video (channel_id, name, description, image_thumbnail, upload_date, duration, video_address) VALUES
                             (%(channel_id)s, %(name)s, %(description)s, %(image_thumbnail)s, %(upload_date)s, %(duration)s,  %(video_address)s);"""

                    cursor.execute(sql, data)
                    conn.commit()
                else:
                    print("This channel is not valid!")

    # delete a video and delete comments of the video
    elif operation == 5:
        print("Fill the blanks: ")
        data['channel_name'] = str(input("name of the channel: "))
        data['name'] = str(input("video name: "))
        data['upload_date'] = str(input("date of the upload: "))

        # check the data that are not blank
        if data['channel_name'] == "" or data['name'] == "" or data['upload_date'] == "":
            print("The required things still are blank.")

        else:
            sql = """SELECT id FROM channel WHERE name = %(channel_name)s;"""

            cursor.execute(sql, data)
            output = cursor.fetchall()
            conn.commit()

            # check the validation of the channel
            if len(output) > 0:
                data['channel_id'] = int(output[0][0])
                sql = """SELECT video_name FROM video WHERE name = %(name)s, upload_date = %(upload_date)s ;"""

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check the validation of the video
                if len(output) > 0:
                    sql = """ SELECT id FROM video WHERE channel_id = %(channel_id)s, name = %(name)s, upload_date = %(upload_date)s"""
                    cursor.execute(sql, data)
                    output = cursor.fetchall()
                    conn.commit()

                    data['video_id'] = output[0][0]

                    # delete the video from db
                    sql = """ DELETE FROM video WHERE id = %(video_id)s; """
                    cursor.execute(sql, data)
                    conn.commit()

                    # delete comments of the video
                    sql = """ DELETE FROM comment WHERE video_id = %(video_id)s; """
                    cursor.execute(sql, data)
                    conn.commit()

                else:
                    print("This video is not valid!")

            else:
                print("This channel is not valid!")

    # watch a video and like or dislike its
    elif operation == 6:
        print("Fill the blanks parts: ")
        data['username'] = str(input("username: "))
        data['video_id'] = str(input("video_id: "))
        # enter 1(like) or 2(dislike)
        data['is_like'] = int(input("like or dislike: \n 1) like \n 2) dislike"))
        data['is_watch'] = True

        # check the data that are not blank
        if data['username'] == "" or data['video_id'] == "" or data['is_like'] == "":
            print("The required things still are blank.")

        else:
            if data['is_like'] == 1:
                data['is_like'] = True
            else:
                data['is_like'] = False

            sql = """SELECT id FROM "user" WHERE username = %(username)s;"""

            cursor.execute(sql, data)
            output = cursor.fetchall()
            conn.commit()

            # check the validation of the user
            if len(output) > 0:
                data['user_id'] = output[0][0]

                # insert like/dislike and watching a video into db
                sql = """ INSERT INTO videoaction (user_id, video_id, is_like, is_watch) VALUES
                                (%(user_id)s, %(video_id)s, %(is_like)s, %(is_watch)s);"""

                cursor.execute(sql, data)
                conn.commit()
            else:
                print("This user is not valid!")

    # become member
    elif operation == 7:
        print("Fill the blanks: ")
        data['username'] = str(input("username: "))
        data['channel_name'] = str(input("channel name: "))
        data['join_date'] = str(input("date of the join: "))

        # check the data that are not blank
        if data['username'] == "" or data['channel_name'] == "" or data['join_date'] == "":
            print("The required things still are blank.")

        else:

            sql = """SELECT id FROM "user" WHERE username = %(username)s;"""

            cursor.execute(sql, data)
            output = cursor.fetchall()
            conn.commit()

            # check the validation of the user
            if len(output) > 0:
                data['user_id'] = int(output[0][0])
                sql = """ SELECT id FROM channel WHERE name = %(channel_name)s; """

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check the validation of the channel
                if len(output) > 0:
                    data['channel_id'] = int(output[0][0])
                    sql = """ SELECT id FROM joinchannel WHERE user_id = %(user_id)s channel_id = %(channel_id)s;"""

                    cursor.execute(sql, data)
                    output = cursor.fetchall()
                    conn.commit()

                    # check that the user is a member of the channel or not
                    if len(output) > 0:
                        print("you are the member of this channel!")

                    else:
                        # insert membership of the user into db
                        sql = """ INSERT INTO joinchannel (user_id, channel_id, join_date) VALUES (%(user_id)s, %(channel_id)s, %(join_date)s);"""

                        cursor.execute(sql, data)
                        conn.commit()

                else:
                    print("This channel is not valid!")

            else:
                print("This user is not valid!")

    # cancel the membership of a channel
    elif operation == 8:
        print("Fill the blanks: ")
        data['username'] = str(input("username: "))
        data['channel_name'] = str(input("channel name: "))

        # check the data that are not blank
        if data['username'] == "" or data['channel_name'] == "":
            print("The required things still are blank.")

        else:
            sql = """SELECT id FROM "user" WHERE username = %(username)s ;"""

            cursor.execute(sql, data)
            output = cursor.fetchall()
            conn.commit()

            # check the validation of the user
            if len(output) > 0:
                data['user_id'] = int(output[0][0])
                sql = """ SELECT id FROM channel WHERE name = %(channel_name)s; """

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check the validation of the channel
                if len(output) > 0:
                    data['channel_id'] = int(output[0][0])
                    sql = """ SELECT id FROM joinchannel WHERE user_id = %(user_id)s channel_id = %(channel_id)s;"""

                    cursor.execute(sql, data)
                    output = cursor.fetchall()
                    conn.commit()

                    # check the user is member of the channel or not
                    if len(output) > 0:

                        # delete the membership of user in channel from db
                        sql = """ DELETE FROM joinchannel (user_id, channel_id) VALUES (%(user_id)s, %(channel_id)s);"""
                        cursor.execute(sql, data)
                        conn.commit()
                    else:
                        print("you are not the member of this channel!")

                else:
                    print("This channel is not valid!")

            else:
                print("This user is not valid!")

    # add comment
    elif operation == 9:
        print("Fill the blanks: ")
        data['username'] = str(input("username: "))
        data['video_id'] = str(input("video id: "))
        data['content'] = str(input("comment: "))

        # check the data that are not blank
        if data['username'] == "" or data['name'] == "" or data['content'] == "":
            print("The required things still are blank.")

        else:

            sql = """SELECT id FROM "user" WHERE username = %(username)s;"""

            cursor.execute(sql, data)
            output = cursor.fetchall()
            conn.commit()

            # check the validation of the user
            if len(output) > 0:

                data['user_id'] = int(output[0][0])
                sql = """SELECT id FROM video WHERE id = %(video_id)s;"""

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()
                if len(output) > 0:

                    # insert the comment of the video into db
                    sql = """ INSERT INTO comment (video_id, content) VALUES
                                     (%(video_id)s, %(content)s);"""
                    cursor.execute(sql, data)
                    conn.commit()

                    sql = """ SELECT id FROM comment WHERE (video_id, content) VALUES
                                                         (%(video_id)s, %(content)s);"""
                    cursor.execute(sql, data)
                    conn.commit()

                    # insert the relation comment into commentCreation of db
                    sql = """ INSERT INTO commentcreation (video_id, content) VALUES
                                                         (%(video_id)s, %(content)s);"""
                    cursor.execute(sql, data)
                    conn.commit()


                else:
                    print("This video is not valid!")

            else:
                print("This user is not valid!")

    # make a playlist
    elif operation == 10:
        print("Fill the blanks: ")
        data['username'] = str(input("username of creator: "))
        data['name'] = str(input("name: "))
        data['video_id'] = str(input("video id: "))
        # 1(private), 2(public)
        data['is_private'] = int(input("privacy: \n1) private\n2)public"))

        # check the data that are not blank
        if data['username'] == "" or data['name'] == "" or data['video_id'] == "" or data['is_private'] == "":
            print("The required things still are blank.")
        else:

            # check the privacy
            if data['is_private'] == 1:
                data['is_private'] = True
            elif data['is_private'] == 2:
                data['is_private'] = False

            else:

                sql = """SELECT id FROM "user" WHERE username = %(username)s ;"""

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check validation of the user
                if len(output) > 0:
                    data['user_id'] = int(output[0][0])

                    # insert the new playlist into db
                    sql = """ INSERT INTO playlist (user_id, name, is_private) VALUES
                                                 (%(user_id)s, %(name)s, %(is_private)s);"""

                    cursor.execute(sql, data)
                    conn.commit()
                else:
                    print("This user is not valid!")

    # add a video to the playlist
    elif operation == 11:
        print("Fill the blanks: ")
        data['username'] = str(input("username of creator: "))
        data['name'] = str(input("name: "))
        data['video_id'] = str(input("video id: "))

        # check the data that are not blank
        if data['username'] == "" or data['name'] == "" or data['video_id'] == "" or data['is_private'] == "":
            print("The required things still are blank.")
        else:

            # check the privacy
            if data['is_private'] == 1:
                data['is_private'] = True
            elif data['is_private'] == 2:
                data['is_private'] = False

            else:

                sql = """SELECT id FROM "user" WHERE username = %(username)s ;"""

                cursor.execute(sql, data)
                output = cursor.fetchall()
                conn.commit()

                # check validation of the user
                if len(output) > 0:
                    data['user_id'] = int(output[0][0])

                    # insert the new playlist into db
                    sql = """ INSERT INTO playlist (user_id, name, is_private) VALUES
                                                         (%(user_id)s, %(name)s, %(is_private)s);"""

                    cursor.execute(sql, data)
                    conn.commit()
                else:
                    print("This user is not valid!")

    # auto generate data
    elif operation == 12:
        count = 0
        while count < 10:
            dt = datetime.now()
            count += 1
            data['username'] = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
            data['password'] = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
            data['email'] = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 5))+("@gmail.com")
            data['image'] = ''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
            data['join_date'] = dt.strftime("%Y-%m-%d %H:%M:%S")

            # insert the new user into db
            sql = """ INSERT INTO "user" (username, password, email, image, join_date) VALUES
                                (%(username)s, crypt(%(password)s, gen_salt('bf')), %(email)s, %(image)s, %(join_date)s);"""

            cursor.execute(sql, data)
            conn.commit()

    conn.close()


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
