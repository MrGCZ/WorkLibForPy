#encoding=utf-8
import pymysql

class jdbc_connect:

    #cursor="";
    #db=False;

    def __init__(self, host, username, password, database):
        try:
            jdbc_connect.db = pymysql.connect(host=host,
                                              port=3306,
                                              user=username,
                                              password=password,
                                              database=database
                                              )
            jdbc_connect.cursor = self.db.cursor()
        except BaseException:
            print("连接数据库异常")
            self.db.close()

    def select(self, sql):
        jdbc_connect.cursor.execute(sql)
        rlist = self.cursor.fetchall()
        return rlist

    def insert(self, sql):
       try:
        jdbc_connect.cursor.execute(sql)
        jdbc_connect.db.commit()
       except pymysql.DataError:
            jdbc_connect.db.rollback()
            print("执行添加操作失败")
            return "1"
       else:
           return "0"

    def update(self, sql):
        try:
            jdbc_connect.cursor.execute(sql)
            jdbc_connect.db.commit()
        except pymysql.DataError:
            jdbc_connect.db.rollback()
            print("执行修改操作失败")
            return "1"
        else:
            return "0"

    def delete(self, sql):
        try:
            jdbc_connect.cursor.execute(sql)
            jdbc_connect.db.commit()
        except pymysql.DataError:
            jdbc_connect.db.rollback()
            print("执行删除操作失败")
            return "1"
        else:
            return "0"

    def closedb(self):
        try:
            self.cursor.close()
            self.db.close()
        except BaseException:
            print("db close error")

    def dickey_convert2_dbkey(self, converted_key, convert_type):
        query_sql = "select convert2_key from etl_convert_dictkey_mapping t where t.convert_type=\'" + convert_type + \
                    "\' and t.converted_key=\'" + converted_key + "\'"
        # print(query_sql)
        convert2_type = self.select(query_sql)[0][0]
        return convert2_type


if __name__ == "__main__":
    connect1 = jdbc_connect("localhost", "root", "1026", "ia2")
    connect1.dickey_convert2_dbkey("windcode", "sec_info")

    # print(connect1)
    # rlist = connect1.select("select * from t_book")
    # print(rlist)
    # print(type(rlist))
