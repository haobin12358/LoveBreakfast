# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
from services.SProduct import SProduct
from common.get_str import get_str
from config.response import PARAMS_MISS, SYSTEM_ERROR
from common.import_status import import_status
from services.SCategory import SCategory
from services.SMachinery import SMachinery


class CProduct():
    def __init__(self):
        try:
            self.title = "========{0}========="
            self.sproduct = SProduct()
            self.service_category = SCategory()
            self.smach = SMachinery()
        except Exception as e:
            print(self.title.format("error"))
            print(e.message)
            print(self.title.format("error"))

    def get_all(self):
        args = request.args.to_dict()
        if "AAid" not in args:
            return PARAMS_MISS
        try:
            pro_list_of_product = self.sproduct.get_all()
            print(self.title.format("pro_list_of_product"))
            print(pro_list_of_product)
            print(self.title.format("pro_list_of_product"))

            pro_list_of_addabo = self.smach.get_pro_by_aaid(get_str(args, "AAid"))
            print(self.title.format("pro_list_of_addabo"))
            print(pro_list_of_addabo)
            print(self.title.format("pro_list_of_addabo"))

            prolist = [pro for pro in pro_list_of_product if pro.PRid in pro_list_of_addabo]
            print(self.title.format("prolist"))
            print(prolist)
            print(self.title.format("prolist"))
            if prolist:
                pro_list_of_control = []
                for i in range(len(prolist)):
                    dic_of_pro = {}
                    dic_of_pro["Pid"] = prolist[i].PRid
                    dic_of_pro["Pname"] = prolist[i].PRname
                    dic_of_pro["Pprice"] = prolist[i].PRprice
                    dic_of_pro["Pimage"] = prolist[i].PRimage
                    dic_of_pro["PsalesVolume"] = prolist[i].PRsalesvolume
                    dic_of_pro["Pscore"] = prolist[i].PRscore
                    dic_of_pro["Pnum"] = 0  # 前端控制用
                    pro_list_of_control.append(dic_of_pro)

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
        if len(args) != 1 or "Pid" not in args.keys():
            return import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")

        pid_to_str = get_str(args, "Pid")
        # 判断是否存在此pid
        print type(pid_to_str)
        all_product_id = self.sproduct.get_all_pid()
        if all_product_id is not None:
            print type(all_product_id[0])
            if pid_to_str not in all_product_id:
                return import_status("NO_THIS_PRODUCT", "response_error", "NO_THIS_PRODUCT")

            # 返回商品详情
            proabo_of_controller = {}
            proabo_of_service = self.sproduct.get_pro_info_by_pid(pid_to_str)
            proabo_of_controller["Pname"] = proabo_of_service.PRname
            proabo_of_controller["Pprice"] = proabo_of_service.PRprice
            proabo_of_controller["Pimage"] = proabo_of_service.PRimage
            proabo_of_controller["Pinfo"] = proabo_of_service.PRinfo
            proabo_of_controller["Pnum"] = 0
            from config.messages import get_product_info_success
            return {
                "status": 200,
                "message": get_product_info_success,
                "data": proabo_of_controller,
            }
        else:
           return SYSTEM_ERROR