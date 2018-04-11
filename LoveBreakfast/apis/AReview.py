# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from control.CProduct import CProduct
from control.CReview import CReview

class AReview(Resource):
    def __init__(self):
        self.control_review = CReview()

    def post(self, product):
        print(PRINT_API_NAME.format(product))

        apis = {
            "create_review": "control_product.create_review()"
        }

        if product in apis:
            return eval(apis[product])

        return

    def get(self, product):
        print(PRINT_API_NAME.format(product))

        apis = {
            "get_user_review": "self.control_product.get_user_review()",
            "get_product_review": "self.control_product.get_product_review()"
        }
        if product in apis:
            return eval(apis[product])

        return