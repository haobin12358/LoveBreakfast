# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from control.COrders import COrders
from config.response import APIS_WRONG

class AOrders(Resource):
    def __int__(self):
        pass

    def get(self, orders):
        print(PRINT_API_NAME.format(orders))

        control_order = COrders()
        apis = {
            "get_order_list": "control_order.get_order_list()",
            "get_order_abo": "control_order.get_order_abo()",
            "get_order_user": "control_order.get_order_user()"
        }

        if orders not in apis:
            return APIS_WRONG

        return eval(apis[orders])

    def post(self, orders):
        print(PRINT_API_NAME.format(orders))

        control_order = COrders()
        apis = {
            "make_main_order": "control_order.make_main_order()",
            "add_order_items": "control_order.add_order_items()",
            "update_order_info": 'control_order.update_order_info()',
            "update_order_status": "control_order.update_order_status()",
            "order_price": "control_order.get_order_price()"
        }

        if orders not in apis:
            return APIS_WRONG

        return eval(apis[orders])
