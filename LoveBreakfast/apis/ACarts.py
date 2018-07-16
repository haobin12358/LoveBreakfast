# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from LoveBreakfast.config.Logs import PRINT_API_NAME
from LoveBreakfast.control.CCarts import CCarts
from LoveBreakfast.config.response import APIS_WRONG


class LBCarts(Resource):
    def __init__(self):
        self.ccart = CCarts()
        self.title = "=========={0}=========="

    def post(self, cart):
        print()
        print(PRINT_API_NAME.format(cart))

        apis = {
            "delete_product": "self.ccart.del_product()",
            "update": "self.ccart.add_or_update_cart()",
            "get_select_product": "self.ccart.get_carts_by_uid_caid()"
        }

        if cart in apis:
            return eval(apis[cart])

        return APIS_WRONG

    def get(self, cart):
        print(PRINT_API_NAME.format(cart))

        apis = {
            "get_all": "self.ccart.get_carts_by_uid_caid()"
        }

        if cart in apis:
            return eval(apis[cart])

        return APIS_WRONG
