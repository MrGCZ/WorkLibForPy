from WindPy import w
from utils.JdbcUtils import *
import time


class WindUtils:

    db_connect = JdbcConnect("localhost", "root", "1026", "ia2")

    def __init__(self):
        w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
        w.isconnected()  # 判断WindPy是否已经登录成功

    def getStock(self):
        a = w.wsd("600030.SH", "CLOSE", "20190101", "20200101")
        return a

    # sec_id can be single sec_id or sec_id list string
    def get_sec_info(self, sec_id):
        # b = w.wss("000001.OF,000005.OF,000009.OF",
        #           "trade_code,windcode,sec_name,sec_englishname,exchange_cn,ipo_date,isin_code,fund_fullname,name_official")

        fund_info = w.wss(sec_id, "trade_code,windcode,sec_name,sec_englishname"
                                  ",exchange_cn,ipo_date,isin_code,fund_fullname,name_official"
                                  ",curr,sec_type,mkt,exch_eng,exchange_cn,sec_status,comp_name"
                          )
        return fund_info

    @classmethod
    def get_edb_data(self, code_id, begin_date, end_date):
        '''
        获取wind经济数据EDB
        :param code_id: string
        :param begin_date:
        :param end_date:
        :return:
        '''
        edb_data = w.edb(code_id, begin_date, end_date, "Fill=Previous")
        return edb_data

    # 获取市场行情
    def get_mkt_quotes(self):
        mkt_q = w.wsd("000001.SZ", "pre_close,open,low,high,close,volume,volume_btin,amt,amount_btin,"
                                   "dealnum,volume_aht,amount_aht,chg,pct_chg,pct_chg_b,swing,vwap,"
                                   "adjfactor,close2,turn,free_turn_n,oi,oi_chg,oi_index,oichange,"
                                   "oiamount,pre_settle,settle,chg_settlement,pctchange_close,"
                                   "pct_chg_settlement,lastradeday_s,trade_status,susp_days,susp_reason",
                                   "2020-06-15", "2020-06-22",
                                   "unit=1;bondPriceType=2;adjDate=20200623")
        return mkt_q

    @classmethod
    def convert2dict(cls, wind_data):
        rdict = {}
        for i in range(len(wind_data.Fields)):
            rdict[wind_data.Fields[i]] = wind_data.Data[i]
        return rdict

    # 获取证券代码列表
    # get_from_wind是否从wind获取 否则从数据库直接获取
    @classmethod
    def get_sec_id_list(cls, sec_type, get_from_wind=0, sql_execute_step=1000, time_string=time.strftime("%Y-%m-%d", time.localtime())):
        if get_from_wind:
            sec_type_map = {'fund_nav': 'a201010700000000',  # 净值型基金
                            'stock_a': 'a001010100000000'  # A股
                            }
            sec_id_list = w.wset("sectorconstituent", "date=%s;sectorid=%s" % (time_string, sec_type_map[sec_type])).Data[1]
            # sec_id_list = ['600000.SS','6000001.SS', '0000001.SZ']
            # 写入本地，增加缓存机制
            sql_para = []
            sql = "insert into sec_id_temp(`type`,`sec_id`, `update_date`) values (%s,%s,%s);"
            for sec_id in sec_id_list:
                sql_para.append((sec_type, sec_id, time.strftime("%Y-%m-%d", time.localtime())))
            WindUtils.db_connect.sql_many_by_step(sql, sql_para, sql_execute_step)
            WindUtils.db_connect.closedb()
        else:
            sql = "select sec_id from sec_id_temp where type = '%s' " \
                  "and update_date = (select max(update_date) from sec_id_temp where type='%s')" % (sec_type, sec_type)
            print("execute sql :" + sql)
            sec_id_list = list(i[0] for i in WindUtils.db_connect.select(sql))
        return sec_id_list


if __name__ == "__main__":

    windUtils = WindUtils()
    # a = windUtils.get_sec_info("000003.OF,000001.OF")
    # b = windUtils.convert2dict(a)
    # print(b)
    # con1 = utils.JdbcUtils.jdbc_connect("localhost", "root", "1026", "ia2")
    # dict2 = con1.dict_to_dbdict(b, "sec_info")
    # print('$dict2$')
    # print(dict2)
    #
    # con1.dict_insert(dict2, 'mkt_sec_info')
    # a = windUtils.get_mkt_quotes()
    # a = windUtils.get_sec_id_list("stock_a", 0)
    # print(a)
