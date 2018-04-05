# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok

class COrders():

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

        from services.SOrders import SOrders
        self.sorders = SOrders()

    def get_order_list(self):
        pass

    def get_order_abo(self):
        pass

    def make_main_order(self):
        args = request.args.to_dict()
        data = request.data

        if "token" not in args:
            return self.param_miss


        pass

    def add_order_item(self):
        pass

    def update_order_info(self):
        pass

    def update_order_status(self):
        pass