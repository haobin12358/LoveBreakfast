# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from control.CAddress import CAddress
from services.SBase import SBase
from config.response import APIS_WRONG


class AAddress(Resource):
    def __init__(self):
        self.sbase = SBase()

    def get(self, address):
        print("=======================api===================")
        print("接口名称是{0}，接口方法是get".format(address))
        print("=======================api===================")
        print("SBASE", id(self.sbase))
        self.sbase.check_connection()
        control_cadd = CAddress()
        apis = {
            "get_citys": "control_cadd.get_citys()",
            "get_addfirst": "control_cadd.get_addfirst()",
            "get_addsecond": "control_cadd.get_addsecond()",
            "get_addabo": "control_cadd.get_addabo()",
        }

        if address in apis:
            return eval(apis[address])

        return APIS_WRONG
