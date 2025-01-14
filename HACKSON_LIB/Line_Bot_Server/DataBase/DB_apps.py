import os
import sqlite3
import time

##DB 読み込み
USER_ID_DB_FILE_NAME = os.path.join(os.path.dirname(__file__), "user.db")
TALK_DB_FILE = os.path.join(os.path.dirname(__file__), "talk.db")

# print(USER_ID_DB_FILE_NAME,TALK_DB_FILE)
## make file 
mkflg = not (os.path.exists(USER_ID_DB_FILE_NAME))

class DB:
    ## Load FIle
    user_con = sqlite3.connect(USER_ID_DB_FILE_NAME, check_same_thread=False)
    user_cur = user_con.cursor()

    talk_con = sqlite3.connect(TALK_DB_FILE, check_same_thread=False)
    talk_cur = talk_con.cursor()

    def __init__(self):
        if mkflg:
            ##########################
            '''
            user.db:: user_table(user_id,name,date)
            talk.db:: talk_his_table(user_id,text,date)
            // data is unixtime.
            '''
            print("DB is　MADE")

            DB.user_cur.execute("create table user_table(user_id text primary key,name text,date integer)")
            DB.talk_cur.execute("create table talk_his_table(user_id text,text text,date integer)")

            DB.user_con.commit()
            DB.talk_con.commit()

    def set_talk_history(self, user_id, text="", date=int(time.time())):
        DB.talk_cur.execute("insert into talk_his_table(user_id,text,date) values(?,?,?)", (user_id, text, date))
        DB.talk_con.commit()

    def set_new_user(self, user_id, name, date=int(time.time())):
        try:
            DB.user_cur.execute("insert into user_table(user_id,name,date) values(?,?,?) select user_id from user",
                                (user_id, name, date))
            DB.user_con.commit()
        except:
            pass

    def change_user_name(self, user_id, name):
        DB.user_cur.execute(f"update user_table set name = {name} where user_id={user_id}")
        DB.user_con.commit()

    def get_talk_his_table(self):
        DB.talk_cur.execute("select * from talk_his_table")
        return (DB.talk_cur.fetchall())

    def get_talk_his_table_from_userId(self, userId) -> list:
        cmd = f"select text from talk_his_table where user_id = '{userId}'"
        DB.talk_cur.execute(cmd)
        dblist = DB.talk_cur.fetchall()
        print(dblist)
        a = [i[0] for i in dblist if i[0] is not None]
        return ",".join(a)

if __name__ == "__main__":
    # set_new_user("test","testuser")
    # set_talk_history("test","ahoxsa")
    # a=get_talk_his_table()
    # print(a)
    # print(1000+1)
    #
    pass
