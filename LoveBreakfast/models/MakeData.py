# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
#from services.SShop import SShop
from services.SProduct import SProduct
import model

change_index = 10  # 循环中改变type的点
info_count = 22  # 需要插入的数据库条数


class MakeData():
    def __init__(self):
        #self.shop = SShop()
        self.product = SProduct()

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

if __name__ == "__main__":
    print("start")
    data = MakeData()
    tshop_ids = data.make_id()
    # data.add_shops(tshop_ids)
    data.add_products(tshop_ids)
    print("over")
