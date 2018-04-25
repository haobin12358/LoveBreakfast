# *- coding:utf8 *-
# *- coding:utf8 *-
# 兼容linux系统
import sys
import os
sys.path.append(os.path.dirname(os.getcwd())) # 增加系统路径
#引用python类
from flask import request
import json
#引用项目类
from services.SProduct import SProduct
from common.get_str import get_str
from common.import_status import import_status
from services.SCategory import SCategory

class CProduct():
    def __init__(self):
        self.service_product = SProduct()
        self.service_category =SCategory()

    #  获取全部商品列表
    def get_all(self):
        pro_list_of_service = self.service_product.get_all()
        if pro_list_of_service != None:
            pro_list_of_control = []
            for i in range(len(pro_list_of_service)):
                dic_of_pro = {}
                dic_of_pro["Pid"] = pro_list_of_service[i].PRid
                dic_of_pro["Pname"] = pro_list_of_service[i].PRname
                dic_of_pro["Pprice"] = pro_list_of_service[i].PRprice
                dic_of_pro["Pimage"] = pro_list_of_service[i].PRimage
                dic_of_pro["PsalesVolume"] = pro_list_of_service[i].PRsalesvolume
                dic_of_pro["Pscore"] = pro_list_of_service[i].PRscore
                dic_of_pro["Pnum"] = 0  # 前端控制用
                pro_list_of_control.append(dic_of_pro)

            print(pro_list_of_control)
            from config.messages import get_product_list_success
            return {
                "message": get_product_list_success,
                "status": 200,
                "data": pro_list_of_control
            }
        else:
            from config.status import response_error
            from config.status_code import SYSTEM_ERROR
            from config.messages import error_system_error
            return {
                "message": error_system_error,
                "status": response_error,
                "status_code": SYSTEM_ERROR

            }
    #  根据商品id获取商品详情
    def get_info_by_id(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 1 or "Pid" not in args.keys():
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
                }

        pid_to_str = get_str(args, "Pid")
        # 判断是否存在此pid
        print type(pid_to_str)
        all_product_id = self.service_product.get_all_pid()
        if all_product_id != None:
            print type(all_product_id[0])
            if pid_to_str not in all_product_id:
                message, status, statuscode = import_status("NO_THIS_PRODUCT", "response_error", "NO_THIS_PRODUCT")
                return {
                    "message": message,
                    "status": status,
                    "statuscode": statuscode,
                }

            # 返回商品详情
            proabo_of_controller = {}
            proabo_of_service = self.service_product.get_pro_info_by_pid(pid_to_str)
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
            from config.status import response_error
            from config.status_code import SYSTEM_ERROR
            from config.messages import error_system_error
            return {
                "message": error_system_error,
                "status": response_error,
                "status_code": SYSTEM_ERROR
            }

    # 根据分类id获取商品信息
    # def get_all_by_category(self, cid):
    #     args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
    #     # 判断url参数是否异常
    #     if len(args) != 1 or "Cid" not in args.keys():
    #         message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
    #         return {
    #             "message": message,
    #             "status": status,
    #             "statuscode": statuscode,
    #         }
    #
    #     cid_to_str = get_str(args, "Cid")
    #     # 判断是否存在此cid
    #     all_category_id = self.service_cotegory.get_all_cid()
    #     if cid_to_str not in all_category_id:
    #         message, status, statuscode = import_status("NO_THIS_CATEGORY", "response_error", "NO_THIS_CATEGORY")
    #         return {
    #             "message": message,
    #             "status": status,
    #             "statuscode": statuscode,
    #         }
    #
    #     # 根据cid获取所有商品的信息
    #     cid_list = self.service_product.get_pro_id_by_cid(cid_to_str)
    #     pro_info_list = []
    #     for each_cid in cid_list:
    #         proabo_of_controller = {}
    #         proabo_of_service = self.service_product.get_pro_info_by_uid(each_cid)
    #         proabo_of_controller["Pname"] = proabo_of_service.Pname
    #         proabo_of_controller["Pprice"] = proabo_of_service.Pprice
    #         proabo_of_controller["Pimage"] = proabo_of_service.Pimage
    #         proabo_of_controller["Sid"] = proabo_of_service.Sid
    #         proabo_of_controller["Pabo"] = proabo_of_service.Pabo
    #         proabo_of_controller["Pstatus"] = proabo_of_service.Pstatus
    #         pro_info_list.append(proabo_of_controller)
    #     return {
    #         "status": 200,
    #         "message": "get pro_list success !",
    #         "productinfo": pro_info_list,
    #     }
    #
