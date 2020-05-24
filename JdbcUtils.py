#encoding=utf-8
import pymysql
from WindPy import w


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

    def dictkey_to_dbkey(self, converted_key, convert_type):
        try:
            query_sql = "select convert2_key from etl_convert_dictkey_mapping t where t.convert_type=\'" + convert_type + \
                        "\' and t.converted_key=\'" + converted_key + "\'"
            # print(query_sql)
            convert2_type = self.select(query_sql)[0][0]
            return convert2_type
        except:
            return converted_key

    # convert key of dict to bdkey, return converted dict
    def dict_to_dbdict(self, dict, convert_type):
        rdict = {}
        for key in dict.keys():
            rdict[self.dictkey_to_dbkey(key, convert_type)] = dict[key]
        return rdict


if __name__ == "__main__":
    connect1 = jdbc_connect("localhost", "root", "1026", "ia2")
    # connect1.dickey_convert2_dbkey("windcode", "sec_info")



    w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
    w.isconnected()  # 判断WindPy是否已经登录成功
    dict1 = {}
    # wind api
    b = w.wss("000001.OF,000005.OF,000009.OF",
              "trade_code,windcode,sec_name,sec_englishname,exchange_cn,ipo_date,isin_code,fund_fullname,name_official")
    print(b)

    # convert to dict
    for i in range(len(b.Fields)):
        dict1[b.Fields[i]] = b.Data[i]

    print(dict1)

    print(connect1.dict_to_dbdict(dict1, "sec_info"))
    print(connect1.dict_to_dbdict(dict1, "sec_info"))

    # print(connect1)
    # rlist = connect1.select("select * from t_book")
    # print(rlist)
    # print(type(rlist))12312311
