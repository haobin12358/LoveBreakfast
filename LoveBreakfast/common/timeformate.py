# *- coding:utf8 *-
import datetime
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
            return datetime.datetime.strptime(time_info, fomat_for_web_second).strftime(fomat_for_db)
        else:
            return datetime.datetime.strptime(time_info, fomat_forweb_no_second).strftime(fomat_for_db)
    return datetime.datetime.now().strftime(fomat_for_db)


def get_web_time_str(time_str):
    return datetime.datetime.strptime(time_str, fomat_for_db).strftime(fomat_for_web_second)

if __name__ == "__main__":
    # print get_db_time_str("2018-04-24 09:00")
    # print get_db_time_str("2018-04-24 8:00:7")
    # print re.match(re_fomat_for_web, "2018-02-12 9:0:2")
    min_time = "2020-03-01 12:35:26"
    datetime_min = datetime.datetime.strptime(min_time, fomat_for_web_second)
    day_min_time = datetime_min.day
    year_min_time = datetime_min.year
    month_min_time = datetime_min.month
    cancel_time = datetime.datetime(year=year_min_time, month=month_min_time,
                                    day=day_min_time, hour=22, minute=0, second=0) - \
                  datetime.timedelta(days=1)
    print cancel_time.strftime(fomat_for_web_second)
    print datetime.datetime.now() > cancel_time
