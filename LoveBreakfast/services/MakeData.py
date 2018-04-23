# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))  # 增加系统路径
#from services.SShop import SShop
from services.SProduct import SProduct
from services.SCoupons import SCoupons
from models import model
from common.TransformToList import add_model
import uuid

class MakeData():
    def __init__(self):
        from services.SUsers import SUsers
        self.users = SUsers()
        from services.SCoupons import SCoupons
        self.scoupons = SCoupons()

    def setUid(self):
        uid = str(uuid.uuid4())
        return uid

    def add_user(self, uid):
        try:
            add_model("Users",
                **{
                    "Uid":uid,
                    "Utel":"17706441101",
                    "Upwd":"123",
                    "Uname":"测试账号",
                    "Usex":101,
                    "Ucoin":100.1,
                    "Uinvate":"ETECH007"
                })
        except Exception as e:
            print e.message

    def setCOid(self):
        list_coid = []
        list_coid.append(str(uuid.uuid4()))
        list_coid.append(str(uuid.uuid4()))
        list_coid.append(str(uuid.uuid4()))
        return list_coid

    def add_coupons(self, coid):
        try:
            for row in coid:
                add_model("Coupons",
                          **{
                              "Couid":row,
                              "Coufilter":20,
                              "Coudiscount":1,
                              "Couamount":None,
                              "Coustart":None,
                              "Couend":None
                          })
        except Exception as e:
            print e.message

    def add_cardpackage(self, coid, uid):
        try:
            add_model("Cardpackage",
                      **{
                          "Carid":str(uuid.uuid4()),
                          "Uid":uid,
                          "Couid":coid[0],
                          "Carstatus":1,
                          "Carstart":"20180423000000",
                          "Carend":"20180429000000"
                      })
            add_model("Cardpackage",
                      **{
                          "Carid": str(uuid.uuid4()),
                          "Uid": uid,
                          "Couid": coid[1],
                          "Carstatus": 2,
                          "Carstart": "20180429000000",
                          "Carend": "20180522000000"
                      })
            add_model("Cardpackage",
                      **{
                          "Carid": str(uuid.uuid4()),
                          "Uid": uid,
                          "Couid": coid[2],
                          "Carstatus": 2,
                          "Carstart": "20180329000000",
                          "Carend": "20180419000000"
                      })
        except Exception as e:
            print e.message

    def set_pid(self):
        pid_list = []
        pid_list.append(str(uuid.uuid4()))
        pid_list.append(str(uuid.uuid4()))
        pid_list.append(str(uuid.uuid4()))
        pid_list.append(str(uuid.uuid4()))
        pid_list.append(str(uuid.uuid4()))
        return pid_list

    def add_product(self, pid):
        try:
            add_model("Products",
                      **{
                          "Pid":pid[0],
                          "Pname":"测试套餐1",
                          "Pprice":28.88,
                          "Sid":None,
                          "Cid":None,
                          "Pstatus":"on_sale",
                          "Pimage":"http://120.79.182.43:7444/imgs/hello.jpg",
                          "Pinfo":"测试数据",
                          "P_sales_volume":100,
                          "Pscore":4.2
                      })
            add_model("Products",
                      **{
                          "Pid": pid[1],
                          "Pname": "测试套餐2",
                          "Pprice": 18.88,
                          "Sid": None,
                          "Cid": None,
                          "Pstatus": "on_sale",
                          "Pimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Pinfo": "测试数据",
                          "P_sales_volume": 300,
                          "Pscore": 3.2
                      })
            add_model("Products",
                      **{
                          "Pid": pid[2],
                          "Pname": "测试套餐3",
                          "Pprice": 9.88,
                          "Sid": None,
                          "Cid": None,
                          "Pstatus": "on_sale",
                          "Pimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Pinfo": "测试数据",
                          "P_sales_volume": 120,
                          "Pscore": 3.5
                      })
            add_model("Products",
                      **{
                          "Pid": pid[3],
                          "Pname": "测试套餐4",
                          "Pprice": 15.88,
                          "Sid": None,
                          "Cid": None,
                          "Pstatus": "on_sale",
                          "Pimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Pinfo": "测试数据",
                          "P_sales_volume": 1001,
                          "Pscore": 2.1
                      })
            add_model("Products",
                      **{
                          "Pid": pid[4],
                          "Pname": "测试套餐5",
                          "Pprice": 13.88,
                          "Sid": None,
                          "Cid": None,
                          "Pstatus": "on_sale",
                          "Pimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Pinfo": "测试数据",
                          "P_sales_volume": 5,
                          "Pscore": 1.6
                      })
        except Exception as e:
            print e.message

    def add_cart(self, uid, pid):
        try:
            add_model("Cart",
                      **{
                          "Caid":str(uuid.uuid4()),
                          "Uid":uid,
                          "Pid":pid[2],
                          "Pnum":2,
                          "Castatus":1
                      })
            add_model("Cart",
                      **{
                          "Caid": str(uuid.uuid4()),
                          "Uid": uid,
                          "Pid": pid[3],
                          "Pnum": 5,
                          "Castatus": 1
                      })
            add_model("Cart",
                      **{
                          "Caid": str(uuid.uuid4()),
                          "Uid": uid,
                          "Pid": pid[0],
                          "Pnum": 1,
                          "Castatus": 2
                      })
        except Exception as e:
            print e.message

    def set_lid(self):
        lid_list = []
        lid_list.append(str(uuid.uuid4()))
        lid_list.append(str(uuid.uuid4()))
        lid_list.append(str(uuid.uuid4()))
        lid_list.append(str(uuid.uuid4()))
        lid_list.append(str(uuid.uuid4()))
        return lid_list

    def add_location(self, lid):
        try:
            add_model("Locations",
                      **{
                          "Lid":lid[0],
                          "Litem":1,
                          "Lname":"江陵路",
                          "Lno":1,
                          "Lboxno":1,
                          "Lstatus":301
                      })
            add_model("Locations",
                      **{
                          "Lid": lid[1],
                          "Litem": 2,
                          "Lname": "钱江世纪城",
                          "Lno": 1,
                          "Lboxno": 1,
                          "Lstatus": 301
                      })
            add_model("Locations",
                      **{
                          "Lid": lid[2],
                          "Litem": 1,
                          "Lname": "滨和路",
                          "Lno": 1,
                          "Lboxno": 1,
                          "Lstatus": 301
                      })
            add_model("Locations",
                      **{
                          "Lid": lid[3],
                          "Litem": 1,
                          "Lname": "西兴",
                          "Lno": 1,
                          "Lboxno": 1,
                          "Lstatus": 301
                      })
            add_model("Locations",
                      **{
                          "Lid": lid[4],
                          "Litem": 1,
                          "Lname": "滨康路",
                          "Lno": 1,
                          "Lboxno": 1,
                          "Lstatus": 301
                      })
        except Exception as e:
            print e.message

    def set_oid(self):
        oid_list = []
        oid_list.append(str(uuid.uuid4()))
        oid_list.append(str(uuid.uuid4()))
        oid_list.append(str(uuid.uuid4()))
        oid_list.append(str(uuid.uuid4()))
        oid_list.append(str(uuid.uuid4()))
        oid_list.append(str(uuid.uuid4()))
        oid_list.append(str(uuid.uuid4()))
        oid_list.append(str(uuid.uuid4()))
        return oid_list

    def add_ordermain(self, oid, uid, lid):
        try:
            add_model("Ordermain",
                      **{
                          "Oid":oid[0],
                          "Otime":"20180423210000",
                          "Otruetimemin":"20180424060000",
                          "Otruetimemax":"20180424063000",
                          "Ostatus":0,
                          "Oprice":18.88,
                          "Lid":lid[0],
                          "Uid":uid,
                          "Opic":"http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo":"测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "Oid": oid[1],
                          "Otime": "20180422210000",
                          "Otruetimemin": "20180423060000",
                          "Otruetimemax": "20180423063000",
                          "Ostatus": 7,
                          "Oprice": 18.88,
                          "Lid": lid[0],
                          "Uid": uid,
                          "Opic": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "Oid": oid[2],
                          "Otime": "20180421210000",
                          "Otruetimemin": "20180422060000",
                          "Otruetimemax": "20180422063000",
                          "Ostatus": 14,
                          "Oprice": 18.88,
                          "Lid": lid[0],
                          "Uid": uid,
                          "Opic": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "Oid": oid[3],
                          "Otime": "20180420210000",
                          "Otruetimemin": "20180421060000",
                          "Otruetimemax": "20180421063000",
                          "Ostatus": 21,
                          "Oprice": 18.88,
                          "Lid": lid[0],
                          "Uid": uid,
                          "Opic": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "Oid": oid[4],
                          "Otime": "20180419210000",
                          "Otruetimemin": "20180420060000",
                          "Otruetimemax": "20180420063000",
                          "Ostatus": 28,
                          "Oprice": 18.88,
                          "Lid": lid[0],
                          "Uid": uid,
                          "Opic": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "Oid": oid[5],
                          "Otime": "20180418210000",
                          "Otruetimemin": "20180419060000",
                          "Otruetimemax": "20180419063000",
                          "Ostatus": 35,
                          "Oprice": 18.88,
                          "Lid": lid[0],
                          "Uid": uid,
                          "Opic": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "Oid": oid[6],
                          "Otime": "20180417210000",
                          "Otruetimemin": "20180418060000",
                          "Otruetimemax": "20180418063000",
                          "Ostatus": 42,
                          "Oprice": 18.88,
                          "Lid": lid[0],
                          "Uid": uid,
                          "Opic": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "Oid": oid[7],
                          "Otime": "20180416210000",
                          "Otruetimemin": "20180417060000",
                          "Otruetimemax": "20180417063000",
                          "Ostatus": 49,
                          "Oprice": 18.88,
                          "Lid": lid[0],
                          "Uid": uid,
                          "Opic": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "Oabo": "测试备注"
                      })
        except Exception as e:
            print e.message

    def add_orderpart(self, oid, pid):
        try:
            for row in oid:
                add_model("Orderpart",
                          **{
                              "OPid":str(uuid.uuid4()),
                              "Oid":row,
                              "Pid":pid[1],
                              "Pnum":1
                          })
        except Exception as e:
            print e.message

    def add_review(self, oid, pid, uid):
        try:
            add_model("Review",
                      **{
                          "Rid":str(uuid.uuid4()),
                          "Oid":oid[7],
                          "Pid":pid[1],
                          "Uid":uid,
                          "Rscore":4,
                          "Rcontent":"测试评价",
                          "Rstatus":"off"
                      })
        except Exception as e:
            print e.message

if __name__ == "__main__":
    makedata = MakeData()
    uid = makedata.setUid()
    pid = makedata.set_pid()
    oid = makedata.set_oid()
    coid = makedata.setCOid()
    lid = makedata.set_lid()

    makedata.add_user(uid)
    makedata.add_coupons(coid)
    makedata.add_cardpackage(coid, uid)
    makedata.add_product(pid)
    makedata.add_cart(uid, pid)
    makedata.add_location(lid)
    makedata.add_ordermain(oid, uid, lid)
    makedata.add_orderpart(oid, pid)
    makedata.add_review(oid, pid, uid)