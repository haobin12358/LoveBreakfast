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
                    "USid":uid,
                    "UStelphone":"17706441101",
                    "USpassword":"123",
                    "USname":"测试账号",
                    "USsex":101,
                    "UScoin":100.1,
                    "USinvatecode":"ETECH007"
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
                              "COid":row,
                              "COfilter":20,
                              "COdiscount":1,
                              "COamount":None,
                              "COstart":None,
                              "COend":None
                          })
        except Exception as e:
            print e.message

    def add_cardpackage(self, coid, uid):
        try:
            add_model("Cardpackage",
                      **{
                          "CAid":str(uuid.uuid4()),
                          "USid":uid,
                          "COid":coid[0],
                          "CAstatus":1,
                          "CAstart":"20180423000000",
                          "CAend":"20180429000000"
                      })
            add_model("Cardpackage",
                      **{
                          "CAid": str(uuid.uuid4()),
                          "USid": uid,
                          "COid": coid[1],
                          "CAstatus": 2,
                          "CAstart": "20180429000000",
                          "CAend": "20180522000000"
                      })
            add_model("Cardpackage",
                      **{
                          "CAid": str(uuid.uuid4()),
                          "USid": uid,
                          "COid": coid[2],
                          "CAstatus": 2,
                          "CAstart": "20180329000000",
                          "CAend": "20180419000000"
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
                          "PRid":pid[0],
                          "PRname":"测试套餐1",
                          "PRprice":28.88,
                          "PRstatus":1,
                          "PRimage":"http://120.79.182.43:7444/imgs/hello.jpg",
                          "PRinfo":"测试数据",
                          "PRsalesvolume":100,
                          "PRscore":4.2
                      })
            add_model("Products",
                      **{
                          "PRid": pid[1],
                          "PRname": "测试套餐2",
                          "PRprice": 18.88,
                          "PRstatus": 1,
                          "PRimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "PRinfo": "测试数据",
                          "PRsalesvolume": 300,
                          "PRscore": 3.2
                      })
            add_model("Products",
                      **{
                          "PRid": pid[2],
                          "PRname": "测试套餐3",
                          "PRprice": 9.88,
                          "PRstatus": 1,
                          "PRimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "PRinfo": "测试数据",
                          "PRsalesvolume": 120,
                          "PRscore": 3.5
                      })
            add_model("Products",
                      **{
                          "PRid": pid[3],
                          "PRname": "测试套餐4",
                          "PRprice": 15.88,
                          "PRstatus": 1,
                          "PRimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "PRinfo": "测试数据",
                          "PRsalesvolume": 1001,
                          "PRscore": 2.1
                      })
            add_model("Products",
                      **{
                          "PRid": pid[4],
                          "PRname": "测试套餐5",
                          "PRprice": 13.88,
                          "PRstatus": 1,
                          "PRimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "PRinfo": "测试数据",
                          "PRsalesvolume": 5,
                          "PRscore": 1.6
                      })
        except Exception as e:
            print e.message

    def add_cart(self, uid, pid):
        try:
            add_model("Cart",
                      **{
                          "CAid":str(uuid.uuid4()),
                          "USid":uid,
                          "PRid":pid[2],
                          "CAnumber":2,
                          "CAstatus":1
                      })
            add_model("Cart",
                      **{
                          "CAid": str(uuid.uuid4()),
                          "USid": uid,
                          "PRid": pid[3],
                          "CAnumber": 5,
                          "CAstatus": 1
                      })
            add_model("Cart",
                      **{
                          "CAid": str(uuid.uuid4()),
                          "USid": uid,
                          "PRid": pid[0],
                          "CAnumber": 1,
                          "CAstatus": 2
                      })
        except Exception as e:
            print e.message

    def set_LOid(self):
        LOid_list = []
        LOid_list.append(str(uuid.uuid4()))
        LOid_list.append(str(uuid.uuid4()))
        LOid_list.append(str(uuid.uuid4()))
        LOid_list.append(str(uuid.uuid4()))
        LOid_list.append(str(uuid.uuid4()))
        return LOid_list

    def add_location(self, LOid):
        try:
            add_model("Locations",
                      **{
                          "LOid":LOid[0],
                          "LOnumber":1,
                          "LOname":"江陵路",
                          "LOexitNumber":1,
                          "LOboxCode":1,
                          "LOstatus":301
                      })
            add_model("Locations",
                      **{
                          "LOid": LOid[1],
                          "LOnumber": 2,
                          "LOname": "钱江世纪城",
                          "LOexitNumber": 1,
                          "LOboxCode": 1,
                          "LOstatus": 301
                      })
            add_model("Locations",
                      **{
                          "LOid": LOid[2],
                          "LOnumber": 1,
                          "LOname": "滨和路",
                          "LOexitNumber": 1,
                          "LOboxCode": 1,
                          "LOstatus": 301
                      })
            add_model("Locations",
                      **{
                          "LOid": LOid[3],
                          "LOnumber": 1,
                          "LOname": "西兴",
                          "LOexitNumber": 1,
                          "LOboxCode": 1,
                          "LOstatus": 301
                      })
            add_model("Locations",
                      **{
                          "LOid": LOid[4],
                          "LOnumber": 1,
                          "LOname": "滨康路",
                          "LOexitNumber": 1,
                          "LOboxCode": 1,
                          "LOstatus": 301
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

    def add_ordermain(self, oid, uid, LOid):
        try:
            add_model("Ordermain",
                      **{
                          "OMid":oid[0],
                          "OMtime":"20180423210000",
                          "OMmealTimeMin":"20180424060000",
                          "OMmealTimeMax":"20180424063000",
                          "OMstatus":0,
                          "OMtotal":18.88,
                          "LOid":LOid[0],
                          "Uid":uid,
                          "OMimage":"http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo":"测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "OMid": oid[1],
                          "OMtime": "20180422210000",
                          "OMmealTimeMin": "20180423060000",
                          "OMmealTimeMax": "20180423063000",
                          "OMstatus": 7,
                          "OMtotal": 18.88,
                          "LOid": LOid[0],
                          "Uid": uid,
                          "OMimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "OMid": oid[2],
                          "OMtime": "20180421210000",
                          "OMmealTimeMin": "20180422060000",
                          "OMmealTimeMax": "20180422063000",
                          "OMstatus": 14,
                          "OMtotal": 18.88,
                          "LOid": LOid[0],
                          "Uid": uid,
                          "OMimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "OMid": oid[3],
                          "OMtime": "20180420210000",
                          "OMmealTimeMin": "20180421060000",
                          "OMmealTimeMax": "20180421063000",
                          "OMstatus": 21,
                          "OMtotal": 18.88,
                          "LOid": LOid[0],
                          "Uid": uid,
                          "OMimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "OMid": oid[4],
                          "OMtime": "20180419210000",
                          "OMmealTimeMin": "20180420060000",
                          "OMmealTimeMax": "20180420063000",
                          "OMstatus": 28,
                          "OMtotal": 18.88,
                          "LOid": LOid[0],
                          "Uid": uid,
                          "OMimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "OMid": oid[5],
                          "OMtime": "20180418210000",
                          "OMmealTimeMin": "20180419060000",
                          "OMmealTimeMax": "20180419063000",
                          "OMstatus": 35,
                          "OMtotal": 18.88,
                          "LOid": LOid[0],
                          "Uid": uid,
                          "OMimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "OMid": oid[6],
                          "OMtime": "20180417210000",
                          "OMmealTimeMin": "20180418060000",
                          "OMmealTimeMax": "20180418063000",
                          "OMstatus": 42,
                          "OMtotal": 18.88,
                          "LOid": LOid[0],
                          "Uid": uid,
                          "OMimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo": "测试备注"
                      })
            add_model("Ordermain",
                      **{
                          "OMid": oid[7],
                          "OMtime": "20180416210000",
                          "OMmealTimeMin": "20180417060000",
                          "OMmealTimeMax": "20180417063000",
                          "OMstatus": 49,
                          "OMtotal": 18.88,
                          "LOid": LOid[0],
                          "Uid": uid,
                          "OMimage": "http://120.79.182.43:7444/imgs/hello.jpg",
                          "OMabo": "测试备注"
                      })
        except Exception as e:
            print e.message

    def add_orderpart(self, oid, pid):
        try:
            for row in oid:
                add_model("Orderpart",
                          **{
                              "OPid":str(uuid.uuid4()),
                              "OMid":row,
                              "Pid":pid[1],
                              "Pnum":1
                          })
        except Exception as e:
            print e.message

    def add_review(self, oid, pid, uid):
        try:
            add_model("Review",
                      **{
                          "REid":str(uuid.uuid4()),
                          "OMid":oid[7],
                          "PRid":pid[1],
                          "USid":uid,
                          "REscore":4,
                          "REcontent":"测试评价",
                          "REstatus":1
                      })
        except Exception as e:
            print e.message

if __name__ == "__main__":
    makedata = MakeData()
    uid = makedata.setUid()
    pid = makedata.set_pid()
    oid = makedata.set_oid()
    coid = makedata.setCOid()
    LOid = makedata.set_LOid()

    makedata.add_user(uid)
    makedata.add_coupons(coid)
    makedata.add_cardpackage(coid, uid)
    makedata.add_product(pid)
    makedata.add_cart(uid, pid)
    makedata.add_location(LOid)
    makedata.add_ordermain(oid, uid, LOid)
    makedata.add_orderpart(oid, pid)
    makedata.add_review(oid, pid, uid)