query_sql = "select convert2_key from etl_convert_dictkey_mapping t where t.convert_type='%s' " \
            "and t.converted_key='%s'" %('123', '222')
print(query_sql)