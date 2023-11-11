import pymysql

conn = pymysql.connect(host='localhost',user='root',password="",db='project_oop')
cur = conn.cursor()



def mysqlconnect(test):

    cur.execute(test)
    output = cur.fetchall()
    return(output)
    



if __name__ == "__main__":
    mysqlconnect("select * from flight")
