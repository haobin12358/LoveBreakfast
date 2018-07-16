# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
from LoveBreakfast.services.SProduct import SProduct
from LoveBreakfast.common.get_str import get_str
from LoveBreakfast.config.response import PARAMS_MISS, SYSTEM_ERROR
from LoveBreakfast.common.import_status import import_status
from LoveBreakfast.services.SCategory import SCategory
from LoveBreakfast.services.SMachinery import SMachinery
from LoveBreakfast.services.SAddress import SAddress
from LoveBreakfast.common.get_model_return_list import get_model_return_list, get_model_return_dict


class CProduct():
    def __init__(self):
        try:
            self.title = "========{0}========="
            self.sproduct = SProduct()
            self.service_category = SCategory()
            self.smach = SMachinery()
            self.sadd = SAddress()
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))

    def get_all(self):
        args = request.args.to_dict()
        if "VNtelphone" in args:
            pass
        try:
            pro_list_of_product = get_model_return_list(self.sproduct.get_all())
            print(self.title.format("pro_list_of_product"))
            print(pro_list_of_product)
            print(self.title.format("pro_list_of_product"))
            if "PRhost" in args and args.get("PRhost") == "host":
                prolist = pro_list_of_product[:]
            elif "ASid" in args and args.get("ASid"):
                aaid_list = get_model_return_list(self.sadd.get_addabo_by_asid(get_str(args, "ASid")))
                print(self.title.format("aaid_list"))
                print(aaid_list)
                print(self.title.format("aaid_list"))
                pro_list_of_addabo = []
                for aaid in aaid_list:
                    pro_list_of_addabo.extend([i.PRid for i in self.smach.get_pro_by_aaid(aaid.get("AAid"))])

                pro_list_of_addabo = {}.fromkeys(pro_list_of_addabo).keys()
                print(self.title.format("pro_list_of_addabo"))
                print(pro_list_of_addabo)
                print(self.title.format("pro_list_of_addabo"))

                prolist = [pro for pro in pro_list_of_product if pro.get("PRid") in pro_list_of_addabo]
            elif "ASid" not in args:
                return PARAMS_MISS
            else:
                return SYSTEM_ERROR

            print(self.title.format("prolist"))
            print(prolist)
            print(self.title.format("prolist"))
            pro_list_of_control = []
            if prolist:
                pro_list_of_control = prolist

            data = import_status("get_product_list_success", "OK")
            data["data"] = pro_list_of_control
            return data
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))
            return SYSTEM_ERROR

    # 根据商品id获取商品详情
    def get_info_by_id(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 1 or "PRid" not in args.keys():
            return import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")

        pid_to_str = get_str(args, "PRid")

        print(self.title.format("pid_to_str"))
        print(pid_to_str)
        print(self.title.format("pid_to_str"))
        # 返回商品详情
        try:
            proabo_of_service = get_model_return_dict(self.sproduct.get_pro_info_by_pid(pid_to_str))
            if not proabo_of_service:
                # 判断是否存在此pid
                return import_status("NO_THIS_PRODUCT", "response_error", "NO_THIS_PRODUCT")

            print("proabo_of_service")
            print(proabo_of_service)
            print("proabo_of_service")

            proabo_of_service["Pnum"] = 0
            data = import_status("get_product_info_success", "OK")
            data["data"] = proabo_of_service
            return data
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))
            return SYSTEM_ERROR
