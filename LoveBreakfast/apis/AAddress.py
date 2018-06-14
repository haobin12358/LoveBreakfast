# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.status import response_system_error
from config.status_code import error_wrong_apis
from config.messages import error_messages_wrong_api
from control.CAddress import CAddress


class AAddress(Resource):
    def __int__(self):
        self.apis_wrong = {}
        self.apis_wrong["status"] = response_system_error
        self.apis_wrong["status_code"] = error_wrong_apis
        self.apis_wrong["messages"] = error_messages_wrong_api

    def get(self, address):
        print("=======================api===================")
        print("接口名称是{0}，接口方法是get".format(address))
        print("=======================api===================")

        control_cadd = CAddress()
        apis = {
            "get_citys": "control_cadd.get_citys()",
            "get_addfirst": "control_cadd.get_addfirst()",
            "get_addsecond": "control_cadd.get_addsecond()",
            "get_addabo": "control_cadd.get_addabo()",
        }

        if address in apis:
            return eval(apis[address])

        return self.apis_wrong
