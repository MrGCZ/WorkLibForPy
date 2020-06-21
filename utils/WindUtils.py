from WindPy import w
import utils.JdbcUtils

class WindUtils:

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
    def convert2dict(cls, wind_data):
        rdict = {}
        for i in range(len(wind_data.Fields)):
            rdict[wind_data.Fields[i]] = wind_data.Data[i]
        return rdict


if __name__ == "__main__":
    windUtils = WindUtils()
    a = windUtils.get_sec_info("000003.OF,000001.OF")
    b = windUtils.convert2dict(a)
    print(b)
    con1 = utils.JdbcUtils.jdbc_connect("localhost", "root", "1026", "ia2")
    dict2 = con1.dict_to_dbdict(b, "sec_info")
    print('$dict2$')
    print(dict2)

    con1.dict_insert(dict2, 'mkt_sec_info')