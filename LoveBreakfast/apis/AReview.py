# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from control.CReview import CReview
from config.response import APIS_WRONG

class AReview(Resource):
    def __init__(self):
        self.control_review = CReview()

    def post(self, review):
        print(PRINT_API_NAME.format(review))

        apis = {
            "create_review": "self.control_review.create_review()",
            "delete_user_review": "self.control_review.delete_user_review()"
        }

        if review in apis:
            return eval(apis[review])

        return APIS_WRONG

    def get(self, review):
        print(PRINT_API_NAME.format(review))
        apis = {
            "get_review": "self.control_review.get_review()",
            "get_user_review": "self.control_review.get_user_review()",
            "get_product_review": "self.control_review.get_product_review()"
        }
        if review in apis:
            return eval(apis[review])

        return APIS_WRONG