# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from LoveBreakfast.control.CAddress import CAddress
from LoveBreakfast.config.response import APIS_WRONG

class LBAddress(Resource):
    def __init__(self):
        self.cadd = CAddress()
        self.title = "=========={0}=========="

    def get(self, address):
        print(self.title.format("api"))
        print("接口名称是{0}，接口方法是get".format(address))
        print(self.title.format("api"))

        apis = {
            "get_citys": "self.cadd.get_citys()",
            "get_addfirst": "self.cadd.get_addfirst()",
            "get_addsecond": "self.cadd.get_addsecond()"
        }

        if address in apis:
            return eval(apis[address])

        return APIS_WRONG

    def post(self, address):
        print(self.title.format("api"))
        print("接口名称是{0}，接口方法是post".format(address))
        print(self.title.format("api"))

        apis = {
            "get_addabo": "self.cadd.get_addabo()"
        }

        if address in apis:
            return eval(apis.get(address))
        return APIS_WRONG
