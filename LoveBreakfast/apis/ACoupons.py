# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from config.status import response_system_error
from config.status_code import error_wrong_apis
from config.messages import error_messages_wrong_api
from control.CCoupons import CCoupons

class ACoupons(Resource):

    def __init__(self):
        self.apis_wrong = {}
        self.apis_wrong["status"] = response_system_error
        self.apis_wrong["status_code"] = error_wrong_apis
        self.apis_wrong["messages"] = error_messages_wrong_api

    def post(self, card):
        print(PRINT_API_NAME.format(card))

        control_coupon = CCoupons()
        apis = {
            "update_coupons": "control_coupon.add_cardpackage()",
        }

        if card in apis:
            return eval(apis[card])

        return self.apis_wrong

    def get(self, card):
        print(PRINT_API_NAME.format(card))

        control_coupon = CCoupons()
        apis = {
            "get_cardpkg": "control_coupon.get_cart_pkg()"

        }

        if card in apis:
            return eval(apis[card])

        return self.apis_wrong
