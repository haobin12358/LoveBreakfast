# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from services.SCategory import SCategory

class ACategory(Resource):
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