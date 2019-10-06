import sqlite3,os,sys
import time

USER_ID_DB_FILE_NAME="user.db"
TALK_DB_FILE="talk.db"


## make file 
mkflg=True#(not(os.path.exists(os.path.join(conf,USER_ID_DB_FILE_NAME))and(os.path.exists(os.path.join(conf,TALK_DB_FILE)))))

## Load FIle
user_con = sqlite3.connect(USER_ID_DB_FILE_NAME)
user_cur=user_con.cursor()

talk_con = sqlite3.connect(TALK_DB_FILE)
talk_cur=talk_con.cursor()

if mkflg:
    ##########################
    '''
    user.db:: user_table(user_id,name,date)
    talk.db:: talk_his_table(user_id,text,date)
    // data is unixtime.
    '''

    user_cur.execute("create table user_table(user_id text primary key,name text,date integer)")
    talk_cur.execute("create table talk_his_table(user_id text primary key,text text,date integer)")

    user_con.commit();talk_con.commit()

def set_talk_history(user_id,text="",date=int(time.time())):
    talk_cur.execute("insert into talk_his_table(user_id,text,date) values(?,?,?)",(user_id,text,date))
    talk_con.commit()

def set_new_user(user_id,name,date=int(time.time())):
    try:
        user_cur.execute("insert into user_table(user_id,name,date) values(?,?,?)",(user_id,name,date))
        user_con.commit()
    except:
        pass
    
def change_user_name(user_id,name):
    user_cur.execute(f"update user_table set name = {name} where user_id={user_id}")
    user_con.commit()

def get_talk_his_table():
    talk_cur.execute("select * from talk_his_table")
    return (talk_cur.fetchall())

if __name__ == "__main__":
    set_new_user("test","testuser")
    set_talk_history("test","ahoxsa")
    a=get_talk_his_table()
    print(a)
    print(1000+1)




     

