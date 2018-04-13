# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from config.status import response_system_error
from config.status_code import error_wrong_apis
from config.messages import error_messages_wrong_api
from control.CUsers import CUsers

class AUsers(Resource):
    def __int__(self):
        self.apis_wrong = {}
        self.apis_wrong["status"] = response_system_error
        self.apis_wrong["status_code"] = error_wrong_apis
        self.apis_wrong["messages"] = error_messages_wrong_api

    def post(self, users):
        print(PRINT_API_NAME.format(users))

        control_user = CUsers()
        apis = {
            "register":"control_user.register()",
            "login":"control_user.login()",
            "update_info":"control_user.update_info()",
            "update_pwd":"control_user.update_pwd()"
        }

        if users in apis:
            return eval(apis[users])

        return self.apis_wrong

    def get(self, users):
        print(PRINT_API_NAME.format(users))

        control_user = CUsers()
        apis = {
            "all_info":"control_user.all_info()"
        }

        if users in apis:
            return eval(apis[users])

        return self.apis_wrong