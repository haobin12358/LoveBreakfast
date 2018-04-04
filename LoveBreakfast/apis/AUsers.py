# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME

class AUsers(Resource):
    def post(self, users):
        print(PRINT_API_NAME.format(users))

        apis = {
            "register":"control_user.register()",
            "login":"control_user.login()",
            "add_info":"control_user.add_info()",
            "update_info":"control_user.update_info()",
            "update_pwd":"control_user.update_pwd()"
        }

        if users in apis:
            return eval(apis[users])

        return

    def get(self, users):
        print(PRINT_API_NAME.format(users))

        apis = {
            "all_info":"control_user.all_info()"
        }
        return