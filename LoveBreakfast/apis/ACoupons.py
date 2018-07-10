# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from LoveBreakfast.config.Logs import PRINT_API_NAME
from LoveBreakfast.control.CCoupons import CCoupons
from LoveBreakfast.config.response import APIS_WRONG

class LBCoupons(Resource):

    def __init__(self):
        pass

    def post(self, card):
        print(PRINT_API_NAME.format(card))

        control_coupon = CCoupons()
        apis = {
            "update_coupons": "control_coupon.add_cardpackage()",
        }

        if card in apis:
            return eval(apis[card])

        return APIS_WRONG

    def get(self, card):
        print(PRINT_API_NAME.format(card))

        control_coupon = CCoupons()
        apis = {
            "get_cardpkg": "control_coupon.get_cart_pkg()"

        }

        if card in apis:
            return eval(apis[card])

        return APIS_WRONG
