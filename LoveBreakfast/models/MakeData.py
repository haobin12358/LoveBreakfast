# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
args = sys.argv
path = os.getcwd()
if len(args) > 1:
    path = args[1]  # /opt/LoveBreakfast
print(path)
sys.path.append(os.path.dirname(path))  # 增加系统路径
import model
import pymysql
change_index = 10  # 循环中改变type的点
info_count = 22  # 需要插入的数据库条数


def add_model(model_name, **kwargs):
    print(model_name)
    if not getattr(model, model_name):
        print("model name = {0} error ".format(model_name))
        return
    model_bean = eval(" models.{0}()".format(model_name))
    for key in model_bean.__table__.columns.keys():
        if key in kwargs:
            setattr(model_bean, key, kwargs.get(key))
    from services.DBSession import get_session
    session, status = get_session()
    if status:
        session.add(model_bean)
        session.commit()
        session.close()
        return
    raise Exception("session connect error")


class databse_deal():
    def __init__(self):
        self.conn = pymysql.connect(
            host=model.cfg.host, user=model.cfg.username,
            passwd=model.cfg.password, charset=model.cfg.charset)
        self.cursor = self.conn.cursor()

    def create_database(self):
        sql = "create database if not exists {0} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;".format(
            model.cfg.database)
        print sql
        try:
            self.cursor.execute(sql)
        except Exception, e:
            print(e)
        finally:
            self.conn_close()

    def drop_database(self):
        sql = "drop database if exists {0} ;".format(
            model.cfg.database)
        print sql
        try:
            self.cursor.execute(sql)
        except Exception, e:
            print(e)

        finally:
            self.conn_close()

    def conn_close(self):
        self.conn.close()


def create():
    databse_deal().create_database()
    model.Base.metadata.create_all(model.mysql_engine)


def drop():
    databse_deal().drop_database()


if __name__ == "__main__":
    print("start")
    '''
       运行该文件就可以在对应的数据库里生成本文件声明的所有table
       如果需要清除数据库，输入drop
       如果需要创建数据库 输入任意不包含drop的字符
       '''
    action = raw_input("create database?")
    if "drop" in action:
        drop()

    else:
        create()
    print("over")
