# *- coding:utf8 *-
from datetime import datetime
import re
"""
统一日期交互格式 
存进数据是 20180414182524
传给前端是 2017-08-06 12:35:26
"""
fomat_for_db = '%Y%m%d%H%M%S'
fomat_for_web_second = '%Y-%m-%d %H:%M:%S'
re_fomat_for_web = r"^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$"
fomat_forweb_no_second = '%Y-%m-%d %H:%M'


def get_db_time_str(time_info=None):
    if time_info:
        if re.match(re_fomat_for_web, time_info):
            return datetime.strptime(time_info, fomat_for_web_second).strftime(fomat_for_db)
        else:
            return datetime.strptime(time_info, fomat_forweb_no_second).strftime(fomat_for_db)
    return datetime.now().strftime(fomat_for_db)


def get_web_time_str(time_str):
    return datetime.strptime(time_str, fomat_for_db).strftime(fomat_for_web_second)

if __name__ == "__main__":
    print get_db_time_str("2018-04-24 09:00")
    print get_db_time_str("2018-04-24 8:00:7")
    # print re.match(re_fomat_for_web, "2018-02-12 9:0:2")
