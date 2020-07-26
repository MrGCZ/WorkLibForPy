import matplotlib.pyplot as plt
from utils.JdbcUtils import *

sql = "select dt,val from wind_macroeco where my_code = 'GDP_SEASON'"
jdbc_connect = JdbcConnect("localhost", "root", "1026", "ia2")
a = jdbc_connect.select(sql)
dt_li = [i[0] for i in a]
val_li = [float(i[1]) for i in a]
print(dt_li)
print(val_li)
plt.plot(dt_li, val_li)
plt.savefig('aaa.png')  # 保存图片要在show之前
plt.show()
