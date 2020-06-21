from data.SecId import *  # python import的是py文件，而不是目录
from utils.JdbcUtils import *
from utils.WindUtils import *

con1 = utils.JdbcUtils.jdbc_connect("localhost", "root", "1026", "ia2")
windUtils = WindUtils()
SecId = SecId()
fund_id_li = SecId.str_to_list(SecId.fund_sec_id_str)

for fund_id in fund_id_li[0:50]:
    fund_dict = windUtils.convert2dict(windUtils.get_fund_info(fund_id))
    fund_dict_db = con1.dict_to_dbdict(fund_dict, "sec_info")
    print(fund_id)
    print(fund_dict_db)
    con1.dict_insert(fund_dict_db, 'mkt_sec_info')