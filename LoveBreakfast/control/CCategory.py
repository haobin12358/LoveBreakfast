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

class CCategory():
    def __init__(self):
        self.service_product = SProduct()
        self.service_category =SCategory()

    # 获取所有的分类名称与id
    def get_all_category(self):
        category_list = self.service_cotegory.get_all_category()
        return {
            "status": 200,
            "message": "get all_category success !",
            "data": category_list
        }




    # 根据店铺id获取所有的分类名称与id
    def get_category_by_sid(self):
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

        list_for_cate_and_pro = self.service_category.get_all_cid_cname()
        return {
            "status": 200,
            "message": "get cate_and_pro success !",
            "data": list_for_cate_and_pro
        }