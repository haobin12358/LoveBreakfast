# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
from config.response import SYSTEM_ERROR, PARAMS_MISS
import datetime
from common import timeformate
from common.import_status import import_status
from common.get_model_return_list import get_model_return_list, get_model_return_dict
from common.get_str import get_str
from common.MakeToken import token_to_usid

class COrders():

    def __init__(self):
        self.title = "=========={0}=========="
        from services.SUsers import SUsers
        self.susers = SUsers()
        from services.SProduct import SProduct
        self.sproduct = SProduct()
        from services.SOrders import SOrders
        self.sorders = SOrders()
        from services.SAddress import SAddress
        self.sadd = SAddress()
        from services.SCoupons import SCoupons
        self.scoupons = SCoupons()
        from services.SMachinery import SMachinery
        self.smach = SMachinery()
        global OMstatus_list
        OMstatus_list = ("已取消", "未支付", "已支付", "已接单", "已配送", "已装箱", "已完成", "已评价")

    def get_order_list(self):
        args = request.args.to_dict()
        if "token" not in args:
            return PARAMS_MISS

        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))

        token = args.get("token")
        Uid = token_to_usid(token)
        # 暂时不处理过滤
        order_list = get_model_return_list(self.sorders.get_all_order_by_uid(Uid))
        print(self.title.format("order_list"))
        print(order_list)
        print(self.title.format("order_list"))

        data = []
        if order_list:
            for row in order_list:
                status = row.get("OMstatus")
                row["OMtime"] = timeformate.get_web_time_str(str(row.get("OMtime")))
                if status > 21 or status == 0 or self.checktime():
                    row["is_index"] = 702
                else:
                    row["is_index"] = 701
                row["OMstatus"] = self.get_status_name_by_status(status)
                row["Orderitems"] = []
                order_items = get_model_return_list(self.sorders.get_order_item_by_oid(row.get("OMid")))
                print(self.title.format("order_items"))
                print(order_items)
                print(self.title.format("order_items"))
                for raw in order_items:
                    Pid = raw.get("PRid")
                    product = get_model_return_dict(self.sproduct.get_product_all_by_pid(Pid))
                    product["PRid"] = Pid
                    print(self.title.format("product"))
                    print(product)
                    print(self.title.format("product"))
                    row["Orderitems"].append(product)
                data.append(row)

        response_make_main_order = import_status("messages_get_item_ok", "OK")
        from config.urlconfig import product_url_list
        response_make_main_order["sowing"] = product_url_list
        response_make_main_order["data"] = data

        return response_make_main_order

    def get_order_abo(self):
        args = request.args.to_dict()
        if "token" not in args or "OMid" not in args:
            return PARAMS_MISS

        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        Oid = args["OMid"]
        token = args.get("token")
        Uid = token_to_usid(token)
        order_abo = get_model_return_dict(self.sorders.get_order_abo_by_oid(Oid))
        print(self.title.format("order_abo"))
        print(order_abo)
        print(self.title.format("order_abo"))
        order_abo["OMtime"] = timeformate.get_web_time_str(order_abo.get("OMtime"))
        order_abo["is_index"] = 701
        if self.checktime() or order_abo.get("OMstatus") > 21 or order_abo.get("OMstatus") == 0:
            order_abo["is_index"] = 702
        order_abo["OMstatus"] = self.get_status_name_by_status(order_abo.get("OMstatus"))
        order_abo["OMdate"] = timeformate.get_web_time_str(order_abo.get("OMdate"))

        users = get_model_return_dict(self.susers.get_uname_utel_by_uid(Uid))
        print(self.title.format("users"))
        print(users)
        print(self.title.format("users"))
        order_abo.update(users)
        order_items = get_model_return_list(self.sorders.get_order_item_by_oid(Oid))
        print(self.title.format("order_items"))
        print(order_items)
        print(self.title.format("order_items"))

        order_abo["Orderitems"] = order_items
        addabo = get_model_return_dict(self.sadd.get_addabo_by_addid(order_abo.get("AAid")))
        print(self.title.format("addabo"))
        print(addabo)
        print(self.title.format("addabo"))
        order_abo.update(addabo)
        for row in order_items:
            product = get_model_return_dict(self.sproduct.get_product_all_by_pid(row.get("PRid")))
            print(self.title.format("product"))
            print(product)
            print(self.title.format("product"))
            product["PRid"] = row.get("PRid")
            row.update(product)

        response_make_main_order = import_status("messages_get_item_ok", "OK")
        response_make_main_order["data"] = order_abo
        return response_make_main_order

    def make_main_order(self):
        args = request.args.to_dict()
        data = request.data
        data = json.loads(data)
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))

        if "token" not in args:
            return PARAMS_MISS

        params_list = ["Order_items", "OMtime", "OMdate", "OMtotal", "AAid"]
        for params in params_list:
            if params not in data:
                return PARAMS_MISS

        token = args.get("token")
        Uid = token_to_usid(token)
        OMtime = timeformate.get_db_time_str(data["OMtime"])
        OMdate = timeformate.get_db_time_str(data["OMdate"])
        order_item = data["Order_items"]
        OMcode = self.make_code()
        import uuid
        aaid = get_str(data, "AAid")
        OMid = str(uuid.uuid1())
        try:
            for op in order_item:
                prostatus = self.sproduct.get_product_status_by_prid(op.get("PRid"))
                print(self.title.format("prostatus"))
                print(prostatus.PRstatus)
                print(self.title.format("prostatus"))
                if prostatus.PRstatus != 1:
                    return import_status("error_no_pro", "LOVEBREAKFAST_ERROR", "error_no_pro")
                mach = self.smach.get_maid_by_aaid_prid(get_str(data, "AAid"), op.get("PRid"))
                print(self.title.format("mach"))
                print(mach)
                print(self.title.format("mach"))

                if not mach:
                    return SYSTEM_ERROR

                self.sorders.add_model("Orderpart", **{
                    "OPid": str(uuid.uuid1()),
                    "OMid": OMid,
                    "PRid": op.get("PRid"),
                    "PRnum": op.get("PRnum")
                })

            print(self.title.format("success add orderpart"))

            self.sorders.add_model("Ordermain", **{
                "OMid": OMid,
                "OMtime": OMtime,
                "OMdate": OMdate,
                "OMstatus": 7,
                "USid": Uid,
                "AAid": aaid,
                "OMcode": OMcode,
                "OMabo": get_str(data, "OMabo"),
                "OMtotal": data.get("OMtotal")

            })

            self.scoupons.update_carbackage(get_str(data, "CAid"))
            response_make_main_order = import_status("messages_add_main_order_success", "OK")
            response_make_main_order["data"] = {}
            response_make_main_order["data"]["OMid"] = OMid
            return response_make_main_order
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))
            return SYSTEM_ERROR

    def update_order_info(self):
        pass

    def update_order_status(self):
        args = request.args.to_dict()
        data = request.data
        data = json.loads(data)

        if "token" not in args:
            return PARAMS_MISS
        if "OMstatus" not in data or "OMid" not in data:
            return PARAMS_MISS
        # 处理token过程，这里未设计

        OMstatus = data["OMstatus"]

        if OMstatus not in OMstatus_list:
            return import_status(
                "messages_error_wrong_status_code", "LOVEBREAKFAST_ERROR", "error_wrong_status_code")

        OMid = data["OMid"]

        update_OMstatus = {}
        update_OMstatus["OMstatus"] = self.get_status_by_status_name(OMstatus)

        response_update_order_status = self.sorders.update_status_by_oid(OMid, update_OMstatus)

        if not response_update_order_status:
            return SYSTEM_ERROR

        return import_status("messages_update_order_status_ok", "OK")

    def get_order_user(self):
        args = request.args.to_dict()
        if "token" not in args:
            return PARAMS_MISS

        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))

        token = args.get("token")
        Uid = token_to_usid(token)

        users_info = self.susers.get_all_users_info(Uid)

        if not users_info:
            return SYSTEM_ERROR

        response_user_info = {}
        Utel = users_info.UStelphone
        response_user_info["Utel"] = Utel
        if users_info.USname not in ["", None]:
            Uname = users_info.USname
            response_user_info["Uname"] = Uname
        else:
            response_user_info["Uname"] = None
        if users_info.USsex not in ["", None]:
            Usex = users_info.USsex
            response_user_info["Usex"] = Usex
        else:
            response_user_info["Usex"] = None

        response_of_get_all = import_status("messages_get_item_ok", "OK")
        response_of_get_all["data"] = response_user_info
        return response_of_get_all

    def get_status_name_by_status(self, status):
        return OMstatus_list[status/7]

    def get_status_by_status_name(self, status_name):
        i = 0
        while i < 7:
            if status_name == OMstatus_list[i]:
                return i*7
            i = i + 1

        return -99

    def checktime(self):
        """
        check now is between 6:00 and 22:00
        :return:
        """
        timenow = datetime.datetime.now()

        if 6 < timenow.hour < 22:
            return False
        return True

    def make_code(self):
        import random
        while True:
            randomcode = random.randint(100000, 999999)
            order = self.sorders.get_order_main_by_code(randomcode)
            if not order:
                return randomcode

    def get_order_price(self):
        args = request.args.to_dict()
        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))

        if "token" not in args:
            return PARAMS_MISS

        data = json.loads(request.data)
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))
        products_list = data.get("productlist")
        # OMcointype = "￥"
        order_list = []
        OMprice = 0
        try:
            for product in products_list:
                prnumber = product.get("PRnumber")
                product = get_model_return_dict(self.sproduct.get_pro_info_by_pid(product.get("PRid")))
                # if product.get("PBunit") != OMcointype:
                #     TODO 增加换算过程
                    # pass
                OMprice += (product.get("PRprice") * prnumber)
                order_list.append(product)

            if "COid" in data and get_str(data, "COid"):
                coupon = get_model_return_dict(self.scoupons.get_coupons_by_couid(get_str(data, "COid")))
                print(self.title.format(coupon))
                print(coupon)
                print(self.title.format(coupon))
                OMprice = self.compute_om_price_by_coupons(coupon, OMprice)
                if not isinstance(OMprice, float):
                    return OMprice

            print(self.title.format("OMprice"))
            print(OMprice)
            print(self.title.format("OMprice"))

            data = import_status("SUCCESS_MESSAGE_GET_INFO", "OK")
            data["data"] = {"OMprice": OMprice, "productlist": order_list}
            return data
        except Exception as e:
            print(self.title.format("get order error"))
            print(e.message)
            print(self.title.format("get order error"))

    def compute_om_price_by_coupons(self, coupon, omprice):
        from decimal import Decimal
        time_now = timeformate.get_db_time_str()
        omprice = Decimal(str(omprice))
        print(self.title.format("timenow"))
        print(time_now)
        print(self.title.format("timenow"))
        print(self.title.format("coutime"))
        print("endtime:", coupon.get("COend", ""), "\n starttime:", coupon.get("COstart", ""))
        print(self.title.format("coutime"))

        if coupon.get("COend") and time_now > coupon.get("COend"):
            return import_status("ERROR_MESSAGE_COUPONS_TIMEEND", "SHARPGOODS_ERROR", "ERROR_TIMR")

        if coupon.get("COstart") and time_now < coupon.get("COstart"):
            return import_status("ERROR_MESSAGE_COUPONS_TIMESTART", "SHARPGOODS_ERROR", "ERROR_TIMR")

        if omprice > coupon.get("COfilter", 0):
            if coupon.get("COamount"):
                omprice = omprice - Decimal(str(coupon.get("COamount", 0)))
            elif isinstance(coupon.get("COdiscount"), float):
                omprice = omprice * Decimal(str(coupon.get("COdiscount")))
            else:
                # 优惠券不打折扣也不满减，要他干嘛
                pass

        print(self.title.format("限定两位小数前的omproce"))
        print(omprice)
        print(self.title.format("限定两位小数前的omproce"))
        omprice = omprice.quantize(Decimal("0.00"))
        return float(omprice) if omprice >= 0 else 0.00


if __name__ == "__main__":
    sorder = COrders()
    print sorder.get_status_by_status_name("未支付")
"""
{
    "status": 200,
    "message": "获取区域信息成功",
    "data": [
        {
            "ACid": "f9490b5d-1745-47e9-b399-36614a8e10e4",
            "ACname": "杭州市",
            "AFtype: ["地铁","生活区"]
        }
    ]
}
"""