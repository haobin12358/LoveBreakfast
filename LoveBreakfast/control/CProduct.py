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

class CProduct():
    def __init__(self):
        self.sproduct = SProduct()

    def get_info(self):
        args = request.args.to_dict()  # 捕获前端的URL参数，以字典形式呈现
        if len(args) != 1 or "Pid" not in args.keys():
            message, status, statuscode = import_status("URL_PARAM_WRONG", "INNER", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
                }

        all_product_id = self.sproduct.get_all_pid()
        if args["Pid"] not in all_product_id:
            message, status, statuscode = import_status("URL_PARAM_WRONG", "INNER", "URL_PARAM_WRONG")
            return {
                "message": message,
                "status": status,
                "statuscode": statuscode,
            }
