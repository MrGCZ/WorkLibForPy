from data.SecId import *  # python import的是py文件，而不是目录
from utils.JdbcUtils import *
from utils.WindUtils import *


class EtlSecInfo:
    con1 = utils.JdbcUtils.jdbc_connect("localhost", "root", "1026", "ia2")
    windUtils = WindUtils()
    SecId = SecId()
    fund_id_li = SecId.str_to_list(SecId.stock_sec_id_str)[0:100]
    fund_id_li_generator = SecId.list_to_str(fund_id_li, 10)

    def etl_sec_info(self):
        for fund_id in self.fund_id_li[1:100]:
            fund_dict = self.windUtils.convert2dict(self.windUtils.get_sec_info(fund_id))
            fund_dict_db = self.con1.dict_to_dbdict(fund_dict, "sec_info")
            print(fund_id)
            print(fund_dict_db)
            self.con1.dict_insert(fund_dict_db, 'mkt_sec_info')

    # 一次查询多个sec_id，速度比较快，采用生成器的方式
    def etl_sec_info_gen(self):
        for fund_id in self.fund_id_li_generator:
            fund_dict = self.windUtils.convert2dict(self.windUtils.get_sec_info(fund_id))
            fund_dict_db = self.con1.dict_to_dbdict(fund_dict, "sec_info")
            print(fund_id)
            print(fund_dict_db)
            self.con1.dict_insert(fund_dict_db, 'mkt_sec_info')


if __name__ == "__main__":
    esi = EtlSecInfo()
    esi.etl_sec_info_gen()
