#encoding=utf-8
import pymysql
from WindPy import w
from utils.CommonUtils import *


class jdbc_connect:

    cursor = ""
    db = False

    def __init__(self, host, username, password, database):
        try:
            self.db = pymysql.connect(host=host,
                                              port=3306,
                                              user=username,
                                              password=password,
                                              database=database
                                              )
            self.cursor = self.db.cursor()
        except BaseException:
            print("连接数据库异常")
            self.db.close()

    def select(self, sql):
        self.cursor.execute(sql)
        rlist = self.cursor.fetchall()
        return rlist

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.DataError:
            self.db.rollback()
            print("执行添加操作失败")
            return "1"
        else:
            return "0"

    # 批量执行，速度更快
    def sql_many(self, sql, replace_param):
        '''
        :param sql:
        :param replace_param: 替换掉的sql中的字符，是一个嵌套的可迭代对象
        :return:
        '''
        try:
            self.cursor.executemany(sql, replace_param)
            self.db.commit()
        except pymysql.DataError:
            self.db.rollback()
            print("执行添加操作失败")
            return "1"
        else:
            return "0"

    # 批量执行，速度更快
    def sql_many_by_step(self, sql, replace_param, step=1000):
        '''
        :param sql:
        :param replace_param: 替换掉的sql中的字符，是一个嵌套的可迭代对象 [(),(),(),(),()...]
        :param step: 每次执行的语句
        :return:
        '''
        try:
            for split_list in CommonUtils.list_split_by_step(replace_param, step):
                self.cursor.executemany(sql, split_list)
                self.db.commit()
        except pymysql.DataError:
            self.db.rollback()
            print("执行添加操作失败")
            return "1"
        else:
            return "0"

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.DataError:
            self.db.rollback()
            print("执行修改操作失败")
            return "1"
        else:
            return "0"

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except pymysql.DataError:
            self.db.rollback()
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
            query_sql = "select convert2_key from etl_convert_dictkey_mapping t where t.convert_type='%s' " \
                        "and t.converted_key='%s'" % (convert_type, converted_key)
            ##print(query_sql)
            convert2_type = self.select(query_sql)[0][0]
            return convert2_type
        except Exception:
            return ''

    # convert key of dict to bdkey, return converted dict
    def dict_to_dbdict(self, dict, convert_type):
        rdict = {}
        for key in dict.keys():
            if self.dictkey_to_dbkey(key, convert_type) != '':
                rdict[self.dictkey_to_dbkey(key, convert_type)] = dict[key]
        return rdict

    def dict_insert(self, insert_data, insert_table, start_row=0):
        for i in range(start_row, len(insert_data[list(insert_data.keys())[0]])):
            sql_str = str("insert into " + insert_table + "(" + ",".join(insert_data.keys()) + ") values(" +
                          "'%s'," * (len(insert_data.keys()) - 1) + "'%s')")
            re_str = ','.join(["insert_data['%s'][i]" % k for k in insert_data.keys()])
            ex_sql_str = sql_str % eval(re_str)
            try:
                self.cursor.execute(ex_sql_str)
                self.db.commit()
            except Exception:
                self.db.rollback()
                # raise

    def dict_insert_bulk(self, insert_data, insert_table, start_row=0):
        keysli = list(insert_data.keys())
        para_list = []
        # 注意这种写法下 %s不带引号 不写成`%s`
        sql_str = str("insert into " + insert_table + "(" + ",".join(insert_data.keys()) + ") values(" +
                      "%s," * (len(insert_data.keys()) - 1) + "%s)")
        for i in range(start_row, len(insert_data[keysli[0]])):
            re_str = ','.join(["insert_data['%s'][i]" % k for k in insert_data.keys()])
            re_list = eval(re_str)
            para_list.append(re_list)
        self.sql_many_by_step(sql_str, para_list)
        self.db.commit()


if __name__ == "__main__":
    connect1 = jdbc_connect("localhost", "root", "1026", "ia2")
    # connect1.dickey_convert2_dbkey("windcode", "sec_info")
    li = list("a,s,d".split(','))
    print(li)

    # sql = "insert into sec_id_temp(`type`,`sec_id`) values (%s,%s)"
    # a= []
    # b= ('11','123123')
    # a.append(b)
    # a.append(("stock","0000.SZ"))
    # print(a)
    #
    # connect1.sql_many(sql,a)



    # w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
    # w.isconnected()  # 判断WindPy是否已经登录成功
    # dict1 = {}
    # # wind api
    # b = w.wss("000001.OF,000005.OF,000009.OF",
    #           "trade_code,windcode,sec_name,sec_englishname,exchange_cn,ipo_date,isin_code,fund_fullname,name_official")
    # print(b)
    #
    # # convert to dict
    # for i in range(len(b.Fields)):
    #     dict1[b.Fields[i]] = b.Data[i]
    #
    # print(connect1.dictkey_to_dbkey('windcode', 'sec_info'))
    #
    # print('$dict1$')
    # print(dict1)
    # dict2 = connect1.dict_to_dbdict(dict1, "sec_info")
    # print('$dict2$')
    # print(dict2)
    #
    # connect1.dict_insert(dict2, 'mkt_sec_info')


    # print(connect1)
    # rlist = connect1.select("select * from t_book")
    # print(rlist)
    # print(type(rlist))12312311
