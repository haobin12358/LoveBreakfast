# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from control.CUsers import CUsers
from config.response import APIS_WRONG

class AUsers(Resource):
    def __int__(self):
        pass

    def post(self, users):
        print(PRINT_API_NAME.format(users))

        control_user = CUsers()
        apis = {
            "register":"control_user.register()",
            "login":"control_user.login()",
            "update_info":"control_user.update_info()",
            "update_pwd":"control_user.update_pwd()",
            "get_inforcode":"control_user.get_inforcode()",
            "forget_pwd": "control_user.forget_pwd()"
        }

        if users in apis:
            return eval(apis[users])

        return APIS_WRONG

    def get(self, users):
        print(PRINT_API_NAME.format(users))

        control_user = CUsers()
        apis = {
            "all_info":"control_user.all_info()"
        }

        if users in apis:
            return eval(apis[users])

        return APIS_WRONG