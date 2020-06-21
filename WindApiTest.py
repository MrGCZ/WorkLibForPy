from WindPy import w
import numpy as np
from matplotlib import pyplot as plt





w.start() # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected() # 判断WindPy是否已经登录成功

a = w.wsd("600030.SH","CLOSE","20190101","20200101")
#
# closePriceList = a.Data[0]
# print(closePriceList)
# plt.plot(closePriceList)
# plt.show()

# wssdata=w.wss("600000.SH,600007.SH,600016.SH", "ev,total_shares","tradeDate=20151222;industryType=1")
# print(wssdata)
#
# a=w.edb("M5567876", "2019-04-01", "2020-05-23","Fill=Previous")
# print(a)
#
# w.edb("M5567876", "2019-04-01", "2020-05-23","Fill=Previous")
#

b = w.edb("M0009805", "2019-06-21", "2020-06-20","Fill=Previous")
print(b)


# dict1={}
# # wind api
# b = w.wss("000001.OF,000005.OF,000009.OF",
#           "trade_code,windcode,sec_name,sec_englishname,exchange_cn,ipo_date,isin_code,fund_fullname,name_official")
# print(b)
#
# # convert to dict
# for i in range(len(b.Fields)):
#         dict1[b.Fields[i]] = b.Data[i]
#
# print(dict1)

# insert into INSERT INTO `ia2`.`mkt_sec_info`(`sec_id`, `name_cn`, `symbol`, `mkt_id`) values()

# a=w.wset("etfconstituent","date=2020-06-19;windcode=159901.OF")
