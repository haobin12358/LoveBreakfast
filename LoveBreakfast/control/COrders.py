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
        global OMstatus_list
        OMstatus_list = ("已取消", "未支付", "已支付", "已接单", "已配送", "已装箱", "已完成", "已评价")

    def get_order_list(self):
        args = request.args.to_dict()
        if "token" not in args:
            return PARAMS_MISS

        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))

        Uid = args["token"]
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
                row["Order_items"] = []
                order_items = get_model_return_list(self.sorders.get_order_item_by_oid(row.OMid))
                print(self.title.format("order_items"))
                print(order_items)
                print(self.title.format("order_items"))
                for raw in order_items:
                    Pid = raw.get("PRid")
                    product = get_model_return_dict(self.sproduct.get_product_all_by_pid(Pid))
                    print(self.title.format("product"))
                    print(product)
                    print(self.title.format("product"))
                    row["Order_items"].append(product)
                data.append(row)

        response_make_main_order = import_status("messages_get_item_ok", "OK")
        from config.urlconfig import product_url_list
        response_make_main_order["sowing"] = product_url_list
        response_make_main_order["data"] = data

        return response_make_main_order

    def get_order_abo(self):
        args = request.args.to_dict()
        if "token" not in args or "Oid" not in args:
            return PARAMS_MISS

        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        Oid = args["OMid"]
        Uid = args["token"]
        order_abo = get_model_return_dict(self.sorders.get_order_abo_by_oid(Oid))
        print(self.title.format("order_abo"))
        print(order_abo)
        print(self.title.format("order_abo"))
        order_abo["OMtime"] = timeformate.get_web_time_str(order_abo.get("OMtime"))
        order_abo["Ostatus"] = self.get_status_name_by_status(order_abo.get("OMstatus"))
        order_abo["OMdate"] = timeformate.get_web_time_str(order_abo.get("OMdate"))
        order_abo["is_index"] = 701
        if self.checktime() or order_abo.OMstatus > 21 or order_abo.OMstatus == 0:
            order_abo["is_index"] = 702
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

        for row in order_items:
            product = get_model_return_dict(self.sproduct.get_product_all_by_pid(row.Pid))
            print(self.title.format("product"))
            print(product)
            print(self.title.format("product"))
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

        Uid = args["token"]
        OMtime = timeformate.get_db_time_str(data["OMtime"])
        OMdate = timeformate.get_db_time_str(data["OMdate"])
        addabo = self.sadd.get_addabo_by_addid(get_str(data, "AAid"))
        OMcode = self.make_code()
        import uuid
        OMid = str(uuid.uuid1())
        if not addabo:
            return SYSTEM_ERROR
        self.sorders.add_model("Ordermain", **{
            "OMid": OMid,
            "OMtime": OMtime,
            "OMdate": OMdate,
            "OMstatus": 7,
            "USid": Uid,
            "AAid": get_str(data, "AAid"),
            "OMcode": OMcode,
            "OMabo": get_str(data, "OMabo"),
            "OMtotal": data.get("OMtotal")

        })

        order_item = data["Order_items"]
        for op in order_item:
            prostatus = self.sproduct.get_product_status_by_prid(op.get("PRid"))
            if prostatus != 1:
                return import_status("error_no_pro", "error_no_pro", "LOVEBREAKFAST_ERROR")

            self.sorders.add_model("Orderpart", **{
                "OPid": str(uuid.uuid1()),
                "OMid": OMid,
                "PRid": op.get("PRid"),
                "PRnum": op.get("PRnum")
            })
            
        response_make_main_order = import_status("messages_add_main_order_success", "OK")
        response_make_main_order["data"] = {}
        response_make_main_order["data"]["Oid"] = OMid
        return response_make_main_order

    def update_order_info(self):
        pass

    def update_order_status(self):
        args = request.args.to_dict()
        data = request.data
        data = json.loads(data)

        if "token" not in args:
            return PARAMS_MISS
        if "Ostatus" not in data or "Oid" not in data:
            return PARAMS_MISS

        from services.SOrders import SOrders
        self.sorders = SOrders()
        # 处理token过程，这里未设计

        OMstatus = data["Ostatus"]

        if OMstatus not in OMstatus_list:
            return import_status(
                "messages_error_wrong_status_code", "LOVEBREAKFAST_ERROR", "error_wrong_status_code")

        Oid = data["Oid"]

        update_OMstatus = {}
        update_OMstatus["OMstatus"] = self.get_status_by_status_name(OMstatus)

        response_update_order_status = self.sorders.update_status_by_oid(Oid, update_OMstatus)

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

        Uid = args["token"]

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

    def deal_time_to_string(self, time):
        time_string = str(time[0,3]) + str(time[5,6]) + str(time[8,9]) + str(time[11,12]) + str(time[14,15]) + \
                      str(time[17,18])
        return time_string

    def deal_string_to_time(self, time_string):
        # time_string = int(time_string)
        time = time_string[0]\
               + time_string[1]\
               + time_string[2]\
               + time_string[3]\
               + "-" \
               + time_string[4]\
               + time_string[5]\
               + "-" \
               + time_string[6]\
               + time_string[7]\
               + " " \
               + time_string[8]\
               + time_string[9]\
               + ":" \
               + time_string[10] \
               + time_string[11]\
               + ":" \
               + time_string[12] \
               + time_string[13]
        return time

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


if __name__ == "__main__":
    sorder = COrders()
    print sorder.get_status_by_status_name("未支付")
