# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from control.CProduct import CProduct

class AProduct(Resource):
    def __init__(self):
        self.control_product = CProduct()

    def post(self, product):
        print(PRINT_API_NAME.format(product))

        apis = {
            "create_pro": "control_product.create_pro()",
            "update_pro_info": "control_product.update_pro_info()",
            "put_on_sale": "control_product.put_on_sale()",
            "put_off_sale": "control_product.put_off_sale()"
        }

        if product in apis:
            return eval(apis[product])

        return

    def get(self, product):
        print(PRINT_API_NAME.format(product))

        apis = {
            "get_info_by_id": "self.control_product.get_info_by_id()",
            "get_all": "self.control_product.get_all()"
        }
        if product in apis:
            return eval(apis[product])

        return