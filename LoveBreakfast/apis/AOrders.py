# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from config.status import response_system_error
from config.status_code import error_wrong_apis
from config.messages import error_messages_wrong_api
from control.COrders import COrders

class AOrders(Resource):
    def __int__(self):
        self.apis_wrong = {}
        self.apis_wrong["status"] = response_system_error
        self.apis_wrong["status_code"] = error_wrong_apis
        self.apis_wrong["messages"] = error_messages_wrong_api

    def get(self, orders):
        print(PRINT_API_NAME.format(orders))

        control_order = COrders()
        apis = {
            "get_order_list":"control_order.get_order_list()",
            "get_order_abo":"control_order.get_order_abo()",
            "get_order_user": "control_order.get_order_user()"
        }

        if orders not in apis:
            return self.apis_wrong

        return eval(apis[orders])

    def post(self, orders):
        print(PRINT_API_NAME.format(orders))

        control_order = COrders()
        apis = {
            "make_main_order":"control_order.make_main_order()",
            "add_order_items":"control_order.add_order_items()",
            "update_order_info":'control_order.update_order_info()',
            "update_order_status":"control_order.update_order_status()"
        }

        if orders not in apis:
            return self.apis_wrong

        return eval(apis[orders])