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

class COrders():

    def __init__(self):
        self.title = "=========={0}=========="
        from services.SUsers import SUsers
        self.susers = SUsers()
        from services.SProduct import SProduct
        self.sproduct = SProduct()
        from services.SOrders import SOrders
        self.sorders = SOrders()
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
                row["OMtime"] = timeformate.get_web_time_str(str(row.get("OMtime")))
                if row.get("OMstatus") > 21 or row.get("OMstatus") == 0 or self.checktime():
                    row["is_index"] = 702
                else:
                    row["is_index"] = 701
                row["OMstatus"] = self.get_status_name_by_status(row.get("OMstatus"))
                row["Order_items"] = []
                order_items = get_model_return_list(self.sorders.get_order_item_by_oid(row.OMid))
                print(self.title.format("order_items"))
                print(order_items)
                print(self.title.format("order_items"))
                for raw in order_items:
                    order_item = {}
                    order_item["Pnum"] = raw.OPamount
                    Pid = raw.Pid
                    product = self.sproduct.get_product_all_by_pid(Pid)
                    print(self.title.format("product"))
                    print(product)
                    print(self.title.format("product"))
                    order_item["Pname"] = product.PRname
                    order_item["Psalenum"] = product.PRsalesvolume
                    order_item["Plevel"] = product.PRscore
                    order_item["Pprice"] = product.PRprice
                    order_item["Pimage"] = product.PRimage
                    row["Order_items"].append(order_item)
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
        Oid = args["Oid"]
        Uid = args["token"]
        order_abo = self.sorders.get_order_abo_by_oid(Oid)
        print(self.title.format("order_abo"))
        print(order_abo)
        print(self.title.format("order_abo"))
        data = {}
        data["Oid"] = Oid
        data["Otime"] = timeformate.get_web_time_str(order_abo.OMtime)
        data["Ostatus"] = self.get_status_name_by_status(order_abo.OMstatus)
        data["Otruetimemin"] = timeformate.get_web_time_str(order_abo.OMmealTimeMin)
        data["Otruetimemax"] = timeformate.get_web_time_str(order_abo.OMmealTimeMax)
        data["Oprice"] = order_abo.OMtotal
        data["Opic"] = order_abo.OMimage
        LOid = order_abo.LOid
        labo = self.sorders.get_loname_loexitnumber_loboxcode_by_loid(LOid)
        data["Lname"] = labo.LOname
        data["Lno"] = labo.LOexitNumber
        data["Lboxno"] = labo.LOboxCode

        if self.checktime() or order_abo.OMstatus > 21 or order_abo.OMstatus == 0:
            data["is_index"] = 702
        else:
            data["is_index"] = 701
        from services.SUsers import SUsers
        susers = SUsers()
        users = susers.get_uname_utel_by_uid(Uid)
        data["Utel"] = users.UStelphone
        data["Uname"] = users.USname
        data["Oabo"] = order_abo.OMabo
        data["Order_items"] = []
        order_items = self.sorders.get_order_item_by_oid(Oid)
        for row in order_items:
            order_item = {}
            order_item["Pnum"] = row.OPamount
            order_item["Pid"] = row.Pid
            from services.SProduct import SProduct
            sproduct = SProduct()
            product = sproduct.get_product_all_by_pid(row.Pid)
            order_item["Pname"] = product.PRname
            order_item["Psalenum"] = product.PRsalesvolume
            order_item["Plevel"] = product.PRscore
            order_item["Pprice"] = product.PRprice
            order_item["Pimage"] = product.PRimage
            data["Order_items"].append(order_item)

        response_make_main_order = import_status("messages_get_item_ok", "OK")
        response_make_main_order["data"] = data
        return response_make_main_order

    def make_main_order(self):
        args = request.args.to_dict()
        data = request.data
        data = json.loads(data)

        if "token" not in args:
            return PARAMS_MISS

        if "Otime" not in data or "Omintime" not in data or "Omaxtime" not in data:
            return PARAMS_MISS

        if "Order_items" not in data:
            return PARAMS_MISS

        print(self.title.format("args"))
        print(args)
        print(self.title.format("args"))
        print(self.title.format("data"))
        print(data)
        print(self.title.format("data"))
        Uid = args["token"]
        OMtime = timeformate.get_db_time_str(data["Otime"])
        OMmealTimeMin = timeformate.get_db_time_str(data["Omintime"])
        OMmealTimeMax = timeformate.get_db_time_str(data["Omaxtime"])
        OMstatus = 7

        if "Lname" not in data or "Lno" not in data:
            from config.status import response_error
            from config.status_code import error_no_location
            from config.messages import messages_no_location
            no_location = {}
            no_location["status"] = response_error
            no_location["status_code"] = error_no_location
            no_location["messages"] = messages_no_location
            return no_location

        LOname = data["Lname"]
        LOexitNumber = data["Lno"]
        LOboxCode = 1  # 后面从其他地方获取 && 智能推荐

        LOid = self.sorders.get_loid_by_loname_loexitNumber_loboxCode(LOname, LOexitNumber, LOboxCode)
        if not LOid:
            return SYSTEM_ERROR
        OMabo = None
        if "Oabo" in data:
            OMabo = data["Oabo"]

        add_main_order = self.sorders.add_main_order(OMtime, OMmealTimeMin, OMmealTimeMax, OMstatus, None, Uid, LOid, OMabo)
        if not add_main_order:
            return SYSTEM_ERROR

        order_item = data["Order_items"]
        add_order_items_by_uid = self.add_order_items(order_item, add_main_order)
        response_make_main_order = import_status("messages_add_main_order_success", "OK")
        response_make_main_order["data"] = {}
        response_make_main_order["data"]["Oid"] = add_main_order
        return response_make_main_order

    def add_order_items(self, order_item_list, oid):
        order_price = 0
        for row in order_item_list:
            Pid = row["Pid"]
            OPamount = row["Pnum"]
            add_order_item = self.sorders.add_order_item(oid, Pid, OPamount)
            if not add_order_item:
                return SYSTEM_ERROR
            from services.SProduct import SProduct
            sproduct = SProduct()
            order_item_price = sproduct.get_pprice_by_pid(Pid)
            if not order_item_price:
                return SYSTEM_ERROR
            order_price = order_price + order_item_price

        from services.SOrders import SOrders
        self.sorders = SOrders()
        update_main_order = {}
        update_main_order["OMtotal"] = order_price
        response_update_main_order = self.sorders.update_price_by_oid(oid, update_main_order)

        if not response_update_main_order:
            return SYSTEM_ERROR

        return True

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
if __name__ == "__main__":
    sorder = COrders()
    print sorder.get_status_by_status_name("未支付")
