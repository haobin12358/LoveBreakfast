# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok
from common.get_model_return_list import get_model_return_list


class CCarts():
    def __int__(self):
        from config.status import response_error
        from config.status_code import error_param_miss
        from config.messages import error_messages_param_miss
        self.param_miss = {}
        self.param_miss["status"] = response_error
        self.param_miss["status_code"] = error_param_miss
        self.param_miss["messages"] = error_messages_param_miss

        from config.status import response_system_error
        from config.messages import error_system_error
        self.system_error = {}
        self.system_error["status"] = response_system_error
        self.system_error["messages"] = error_system_error

        from services.SCarts import SCarts
        self.scart = SCarts()
        from services.SProduct import SProduct
        self.spro = SProduct()

    def get_carts_by_uid(self):
        args = request.args.to_dict()
        if "token" not in args:
            return self.param_miss

        #todo uid 验证未实现
        uid = args.get("token")
        res_get_all = {}

        try:
            cart_info_list = []
            cart_list = get_model_return_list(self.scart.get_carts_by_Uid(uid))
            for cart in cart_list:
                self.spro.
            res_get_all["data"] =
        except Exception as e:




