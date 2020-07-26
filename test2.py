# encoding=utf-8
import datetime
from utils.JdbcUtils import *

# sql_str = "insert into mkt_sec_info(`symbol`,`sec_id`,`name_cn`) values(%s,%s,%s)"
# parali = [('000001', '000001.SZ', '平安银行', 'PAB', datetime.datetime(1991, 4, 3, 0, 0), 'CNE000000040', 'CNY', '普通股', 'SZSE', 'L', '平安银行股份有限公司'), ('000002', '000002.SZ', '万科A', 'VANKE-A', datetime.datetime(1991, 1, 29, 0, 0), 'CNE0000000T2', 'CNY', '普通股', 'SZSE', 'L', '万科企业股份有限公司'), ('000004', '000004.SZ', '国农科技', 'CAU-TECH', datetime.datetime(1991, 1, 14, 0, 0), 'CNE0000000Y2', 'CNY', '普通股', 'SZSE', 'L', '深圳中国农大科技股份有限公司'), ('000005', '000005.SZ', '世纪星源', 'FOUNTAIN', datetime.datetime(1990, 12, 10, 0, 0), 'CNE0000001L7', 'CNY', '普通股', 'SZSE', 'L', '深圳世纪星源股份有限公司'), ('000006', '000006.SZ', '深振业A', 'ZHENYE', datetime.datetime(1992, 4, 27, 0, 0), 'CNE000000164', 'CNY', '普通股', 'SZSE', 'L', '深圳市振业(集团)股份有限公司'), ('000007', '000007.SZ', '全新好', 'QUANXINHAO', datetime.datetime(1992, 4, 13, 0, 0), 'CNE0000000P0', 'CNY', '普通股', 'SZSE', 'L', '深圳市全新好股份有限公司')]
#
# parali2 = [('000001', '000001.SZ', '平安银行')]
#
# connect1 = jdbc_connect("localhost", "root", "1026", "ia2")
# connect1.sql_many_by_step(sql_str, parali2)

li = ['a'] * 10

print(li)
