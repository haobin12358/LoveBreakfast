# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from LoveBreakfast.config.Logs import PRINT_API_NAME
from LoveBreakfast.control.CCarts import CCarts
from LoveBreakfast.config.response import APIS_WRONG

class ACarts(Resource):
    def __int__(self):
        pass

    def post(self, cart):
        print(PRINT_API_NAME.format(cart))

        control_cart = CCarts()
        apis = {
            "delete_product": "control_cart.del_product()",
            "update": "control_cart.add_or_update_cart()",
            "get_select_product": "control_cart.get_carts_by_uid_caid()"
        }

        if cart in apis:
            return eval(apis[cart])

        return APIS_WRONG

    def get(self, cart):
        print(PRINT_API_NAME.format(cart))

        control_cart = CCarts()
        apis = {
            "get_all": "control_cart.get_carts_by_uid_caid()"
        }

        if cart in apis:
            return eval(apis[cart])

        return APIS_WRONG
