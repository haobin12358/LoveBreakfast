# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
#from services.SCoupons import SCoupons
import model
import pymysql
change_index = 10  # 循环中改变type的点
info_count = 22  # 需要插入的数据库条数


class MakeData():
    def __init__(self):
        #self.shop = SShop()
        # self.product = SProduct()
        self.cou = SCoupons()

    def make_id(self):
        import uuid
        user_ids = []
        i = 0
        while i < info_count:
            user_ids.append(str(uuid.uuid4()))
            i = i + 1
        return user_ids

    def add_shops(self, tshop_ids):
        for i in range(info_count):
            shop_model = model.Shops()
            shop_model.Sid = tshop_ids[i]
            shop_model.Sname = "test{0}".format(i)
            shop_model.Sreview = "5"
            shop_model.Sdetail = "包子，粥，面条"
            shop_model.Simage = "http://www.baidu.com"
            shop_model.Stel = "135880461%02d" % i
            self.shop.add_shop(shop_model)

    def add_products(self, tshop_ids):
        for i in range(info_count):
            pro_model = model.Products()
            pro_model.Pid = "100{0}".format(i)
            pro_model.Pname = "test{0}".format(i)
            pro_model.Pprice = 10
            pro_model.Pstatus = "on_sale"
            pro_model.Pimage = "http://www.baidu.com"
            pro_model.Pinfo = "taste good"
            pro_model.P_sales_volume = 100
            pro_model.Pscore = 5
            self.product.add_product(pro_model)

    def add_conpons(self, conid):
        for i in range(info_count):
            self.cou.add_coupons(**{
                "COid": i,
                "COfilter": float("1%02d.00" % i),
                "COdiscount": 0.2,
                "COamount": 10.1,
                "COstart": "2018011421%02d00" % i,
                "COend": "2018041421%02d00" % i
            })


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
        #data = MakeData()
        #tshop_ids = data.make_id()
        # data.add_shops(tshop_ids)
        # data.add_products(tshop_ids)
        #data.add_conpons(tshop_ids)
        print("over")
