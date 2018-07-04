# *- coding:utf8 *-
import sys
import os

sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from control.CAddress import CAddress
from config.Singerconfig import sbase
from config.response import APIS_WRONG


class AAddress(Resource):
    def __init__(self):
        pass

    def get(self, address):
        print("=======================api===================")
        print("接口名称是{0}，接口方法是get".format(address))
        print("=======================api===================")
        print("SBASE", id(sbase))
        sbase.check_connection()
        control_cadd = CAddress()
        apis = {
            "get_citys": "control_cadd.get_citys()",
            "get_addfirst": "control_cadd.get_addfirst()",
            "get_addsecond": "control_cadd.get_addsecond()",

        }

        if address in apis:
            return eval(apis[address])

        return APIS_WRONG

    def post(self, address):
        print("=======================api===================")
        print("接口名称是{0}，接口方法是get".format(address))
        print("=======================api===================")
        control_cadd = CAddress()
        apis = {
            "get_addabo": "control_cadd.get_addabo()",
        }

        if address in apis:
            return eval(apis.get(address))
        return APIS_WRONG
