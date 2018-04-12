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
from services.SShop import SShop

class CShop():
    def __init__(self):
        self.service_product = SProduct()
        self.service_shop = SShop()

    # 获取所有商店的信息
    def get_all_shops(self):
        # 返回商品详情
        list = []
        shopsdetail_of_service = self.service_shop.get_all_shops()
        for i in range(shopsdetail_of_service.__len__()/10):
            shopdetail_of_controller = {}
            dic2 = {}
            shopdetail_of_controller["Sname"] = shopsdetail_of_service[i].Sname
            dic2["Simage"] = shopsdetail_of_service[i].Simage
            dic2["Sreview"] = shopsdetail_of_service[i].Sreview
            dic2["Sdetail"] = shopsdetail_of_service[i].Sdetail.encode("utf-8")
            shopdetail_of_controller["data"] = dic2
            list.append(shopdetail_of_controller)
        return {
            "status": 200,
            "message": "get homepage_shops success !",
            "data": list,
        }

    # 根据商品id获取商店详情
    def get_shop_detail(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 1 or "Sid" not in args.keys():
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }

        sid_to_str = get_str(args, "Sid")
        # 判断是否存在此pid
        print type(sid_to_str)
        all_shop_id = self.service_shop.get_all_sid()
        print type(all_shop_id)
        print all_shop_id
        if str(args["Sid"]) not in all_shop_id:
            message, status, statuscode = import_status("NO_THIS_Shop", "response_error", "NO_THIS_Shop")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }

        shopdetail = {}
        shopdetail_from_service = self.service_shop.get_shop_detail(sid_to_str)
        shopdetail["Sname"] = shopdetail_from_service.Sname
        shopdetail["Simage"] = shopdetail_from_service.Simage
        shopdetail["Stel"] = shopdetail_from_service.Stel
        shopdetail["Sdetail"] = shopdetail_from_service.Sdetail
        return {
            "status": 200,
            "message": "get shop_detail success !",
            "data": shopdetail
        }

    # 根据店铺id获取所有的分类与商品信息
    def get_category_and_product(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        # 判断url参数是否异常
        if len(args) != 1 or "Sid" not in args.keys():
            message, status, statuscode = import_status("URL_PARAM_WRONG", "response_error", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }

        sid_to_str = get_str(args, "Sid")
        # 判断是否存在此sid
        print type(sid_to_str)
        all_shop_id = self.service_shop.get_all_sid()
        print type(all_shop_id)
        print all_shop_id
        if str(args["Sid"]) not in all_shop_id:
            message, status, statuscode = import_status("NO_THIS_Shop", "response_error", "NO_THIS_Shop")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }

        # 获取所有的分类信息
        dic_for_cate_and_pro = []
        cate_list = self.service_shop.get_all_cid_cname(str(args["Sid"]))
        for i in range(cate_list.__len__()):
            dict1 = {}
            dict1["name"] = cate_list[i].Pcatgoryname
            Pcategoryid = cate_list[i].Pcategoryid
            pro_dic = None
            pro_dic = self.service_product.get_pro_id_by_cid(Pcategoryid)  # 根据分类id获取商品信息
            pro_dic_of_control = None
            pro_dic_of_control["Pname"] = pro_dic.Pname
            pro_dic_of_control["Pprice"] = pro_dic.Pprice
            pro_dic_of_control["Pimage"] = pro_dic.Pimage
            dict1["data"] = pro_dic_of_control
            dic_for_cate_and_pro.append(dict1)
        return {
            "status": 200,
            "message": "get get_category_and_product success !",
            "data": dic_for_cate_and_pro
        }




