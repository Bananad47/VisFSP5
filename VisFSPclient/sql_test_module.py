import json
import pymysql


def create_sql_connection(func):
    def import_settings():
        with open("sql_settings.json","r") as file:
            settings = json.load(file)
            return settings

    def create_connection():
        settings = import_settings()
        connection = pymysql.connect(
            host = settings["DB_ip"],
            port = settings["DB_port"],
            user = settings["DB_login"],
            password = settings["DB_password"],
            database = settings["DB_name"],
            cursorclass = pymysql.cursors.DictCursor)

        return connection, settings["Main_table_name"]

    def pass_connection(*args,**kwargs):
        connection, table = create_connection()
        cur = connection.cursor()
        return func(*args,**kwargs,cur = cur, table = table,con = connection)
    return pass_connection




@create_sql_connection
def sql_all_data(limit,cur = "",table = "",con = ""):
    cur.execute("SELECT * FROM {} ORDER BY id DESC LIMIT {}".format(table,limit))
    rows = cur.fetchall()
    return rows




@create_sql_connection
def sql_search_data(id,cur = "",table = "",con = ""):
    cur.execute("SELECT * FROM {} WHERE id = {}".format(table,id))
    row = cur.fetchone()
    return row




@create_sql_connection
def last_item_id(cur = "",table = "",con = ""):
    cur.execute("SELECT * FROM {} ORDER BY id DESC LIMIT 1".format(table))
    Id = str(cur.fetchone()["id"])
    return Id

@create_sql_connection
def new_rows(num,cur = "",table = "",con = ""):
    cur.execute("SELECT * FROM {} ORDER BY id DESC LIMIT {}".format(table,num))
    return cur.fetchall()[::-1]



@create_sql_connection
def statistic(date_from,date_to,cur="",table="",con = ""):
    l = []
    date_to += " 23:59:59"
    date_from += " 0:00:00"
    cur.execute("SELECT COUNT(1) FROM `{}` WHERE date >= '{}' AND date <= '{}' AND `status` = '1'".format(table,date_from,date_to))
    l.append(cur.fetchone()["COUNT(1)"])
    cur.execute("SELECT COUNT(1) FROM `{}` WHERE date >= '{}' AND date <= '{}' AND `status` = '2'".format(table,date_from,date_to))
    l.append(cur.fetchone()["COUNT(1)"])
    cur.execute("SELECT COUNT(1) FROM `{}` WHERE date >= '{}' AND date <= '{}' AND `status` = '3'".format(table,date_from,date_to))
    l.append(cur.fetchone()["COUNT(1)"])
    return l


@create_sql_connection
def updateSettings(l1,l2,num, cur = "",table = "",con = ""):
    names = ['diag_w', 'diag_b', 'corner_w', 'corner_b', 'front_rib_w', 'front_rib_b', 'side_rib_w', 'side_rib_b', 'turn_w', 'turn_b', 'position_w', 'position_b', 'length_overlarge_w', 'length_overlarge_b', 'length_extrasmall_w', 'length_extrasmall_b', 'width_overlarge_w', 'width_overlarge_b', 'width_extrasmall_w', 'width_extrasmall_b',"spot_w","spot_b","actual_tolerance"]
    for name,value in zip(names,l2):
        cur.execute(f"UPDATE tolerance SET `{name}` = '{value}' WHERE `id` = {int(num)}")
        con.commit()
    names2 = ["length","width","diag","position","turn","squareness","rib","corner","crack","spot"]
    for i,num in zip(l1,names2):
        cur.execute(f"UPDATE tools SET `{num}` = {i}")
        con.commit()
    cur.execute("UPDATE `service` SET `change_tools` = '1'")
    con.commit()
    return 0


@create_sql_connection
def settingsData(num,cur = "", table = "",con = ""):
    names = ['diag_w', 'diag_b', 'corner_w', 'corner_b', 'front_rib_w', 'front_rib_b', 'side_rib_w', 'side_rib_b', 'squareness_w', 'squareness_b', 'turn_w', 'turn_b', 'position_w', 'position_b', 'length_overlarge_w', 'length_overlarge_b', 'length_extrasmall_w', 'length_extrasmall_b', 'width_overlarge_w', 'width_overlarge_b', 'width_extrasmall_w', 'width_extrasmall_b',"spot_w","spot_b"]
    cur.execute(f"SELECT * FROM `tolerance` WHERE `id` = {num}")
    l = cur.fetchone()
    cur.execute("SELECT * FROM `tools`")
    l2 = cur.fetchone()
    return l2,l


@create_sql_connection
def checkUpdate(cur = "", table = "",con = ""):
    cur.execute("SELECT * FROM `service`")
    ans = cur.fetchone()
    if ans["scan"] == 1:
        cur.execute("UPDATE `service` SET `scan` = '0'")
        con.commit()
    return ans


@create_sql_connection
def search(data,datestart,datefinish,cur = "", table = "", con = ""):
    if not True in data:
        return []
    l = " or ".join([f"status = {i}" for x,i in zip(data,range(1,4)) if x])

    s = f"SELECT * FROM `{table}` WHERE date >= '{datestart}' AND date <= '{datefinish}' AND ({l})"
    cur.execute(s)
    k = cur.fetchall()
    return k


@create_sql_connection
def getPassword(cur = "", table = "", con = ""):
    cur.execute("SELECT `password` FROM `service`")
    return cur.fetchone()
