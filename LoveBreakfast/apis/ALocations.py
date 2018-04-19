# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from config.status import response_system_error
from config.status_code import error_wrong_apis
from config.messages import error_messages_wrong_api
from control.Clocations import Clocations

class ALocations(Resource):
    def __int__(self):
        self.apis_wrong = []

    def get(self, locations):
        print(PRINT_API_NAME.format(locations))

        control_location = Clocations()
        apis = {
            "get_all_location":"control_location.get_all_location()",
            "get_lno": "control_location.get_lno()",
            "get_lline": "control_location.get_lline()"
        }

        if locations in apis:
            return eval(apis[locations])

        apis_wrong = []
        apis_wrong["status"] = response_system_error
        apis_wrong["status_code"] = error_wrong_apis
        apis_wrong["messages"] = error_messages_wrong_api
        return apis_wrong