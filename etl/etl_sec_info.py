from data.SecId import *  # python import的是py文件，而不是目录
from utils.JdbcUtils import *
from utils.WindUtils import *


class EtlSecInfo:
    con1 = JdbcConnect("localhost", "root", "1026", "ia2")
    windUtils = WindUtils()
    SecId = SecId()
    # 获取sec_id迭代器 多种方式
    fund_id_li = SecId.str_to_list(SecId.stock_sec_id_str)[0:100]
    fund_id_li_generator = SecId.list_to_str(fund_id_li, 10)
    # 从数据库中获取
    fund_id_li_gen_db = CommonUtils.list_split_by_step(WindUtils.get_sec_id_list("stock_a"), 1000)

    def etl_sec_info(self):
        for fund_id in self.fund_id_li[1:100]:
            fund_dict = self.windUtils.convert2dict(self.windUtils.get_sec_info(fund_id))
            fund_dict_db = self.con1.dict_to_dbdict(fund_dict, "sec_info")
            print(fund_id)
            print(fund_dict_db)
            self.con1.dict_insert(fund_dict_db, 'mkt_sec_info')

    # 一次查询多个sec_id，速度比较快，采用生成器的方式
    def etl_sec_info_gen(self, sec_id_generator):
        '''
        :param sec_id_generator:sec_id迭代器对象
        :return:
        '''
        for sec_id in sec_id_generator:
            sec_id_dict = self.windUtils.convert2dict(self.windUtils.get_sec_info(sec_id))
            sec_dict_db = self.con1.dict_to_dbdict(sec_id_dict, "sec_info")
            # print(sec_id)
            # print(sec_dict_db)
            # self.con1.dict_insert(sec_dict_db, 'mkt_sec_info')
            self.con1.dict_insert_bulk(sec_dict_db, 'mkt_sec_info')

    def wind_marcoeco_data(self, begin_date, end_date, *my_code_list):
        '''
        wind宏观经济数据
        :return:
        '''
        wind_list = self.con1.my_code2wind_code("EDB", *my_code_list)
        result_data = WindUtils.get_edb_data(wind_list, begin_date, end_date)
        print(result_data)
        for i in range(len(result_data.Codes)):
            in_dict = self.con1.wind_code2my_code("EDB", result_data.Codes[i])
            data_num = len(result_data.Data[i])
            for k in in_dict:
                in_dict[k] = [in_dict[k]] * data_num
            in_dict['val'] = result_data.Data[i]
            in_dict['dt'] = result_data.Times
            print(in_dict)
            self.con1.dict_insert_bulk(in_dict,'wind_macroeco')



if __name__ == "__main__":
    esi = EtlSecInfo()
    # esi.etl_sec_info_gen(EtlSecInfo.fund_id_li_gen_db)
    esi.wind_marcoeco_data('2000-01-01', '2020-07-01', 'GDP_SEASON', 'GDP_FIRST_INDUS_SEASON', 'GDP_SECOND_INDUS_SEASON',
                           'GDP_THIRD_INDUS_SEASON')