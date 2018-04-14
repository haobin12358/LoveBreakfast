# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from config.status import response_system_error
from config.status_code import error_wrong_apis
from config.messages import error_messages_wrong_api
from control.CCarts import CCarts


class ACarts(Resource):
    def __int__(self):
        self.apis_wrong = {}
        self.apis_wrong["status"] = response_system_error
        self.apis_wrong["status_code"] = error_wrong_apis
        self.apis_wrong["messages"] = error_messages_wrong_api

    def post(self, cart):
        print(PRINT_API_NAME.format(cart))

        control_cart = CCarts()
        apis = {
            "delete_product": "control_cart.del_cart()",
            "update": "control_cart.add_or_update_cart()"
        }

        if cart in apis:
            return eval(apis[cart])

        return self.apis_wrong

    def get(self, cart):
        print(PRINT_API_NAME.format(cart))

        control_cart = CCarts()
        apis = {
            "get_all": "control_cart.get_carts_by_uid()"
        }

        if cart in apis:
            return eval(apis[cart])

        return self.apis_wrong
