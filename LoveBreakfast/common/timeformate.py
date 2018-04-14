# *- coding:utf8 *-
from datetime import datetime
"""
统一日期交互格式 
存进数据是 20180414182524
传给前端是 2017-08-06 12:35:26
"""
fomat_for_db = '%Y%m%d%H%M%S'
fomat_for_web = '%Y-%m-%d %H:%M:%S'


def get_db_time_str(time_info=None):
    if time_info:
        return time_info.strftime(fomat_for_db)
    return datetime.now().strftime(fomat_for_db)


def get_web_time_str(time_str):
    return datetime.strptime(time_str, fomat_for_db).strftime(fomat_for_web)
