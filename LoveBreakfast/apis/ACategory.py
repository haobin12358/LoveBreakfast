# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from LoveBreakfast.config.Logs import PRINT_API_NAME
from LoveBreakfast.services.SCategory import SCategory

class LBCategory(Resource):
    def __init__(self):
        self.control_category = SCategory()

    def post(self, category):
        print(PRINT_API_NAME.format(category))

        apis = {

        }

        if category in apis:
            return eval(apis[category])

        return

    def get(self, category):
        print(PRINT_API_NAME.format(category))

        apis = {
            "get_all_category": "self.control_category.get_all_category()",
            "get_category_by_sid": "self.control_category.get_category_by_sid()",
        }
        return eval(apis[category])