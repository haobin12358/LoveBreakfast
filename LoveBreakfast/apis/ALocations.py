# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from control.Clocations import Clocations
from config.response import APIS_WRONG

class ALocations(Resource):
    def __int__(self):
        self.apis_wrong = []

    def get(self, locations):
        print(PRINT_API_NAME.format(locations))

        control_location = Clocations()
        apis = {
            "get_all_location":"control_location.get_all_location()",
            "get_lno": "control_location.get_lno()",
            "get_lline": "control_location.get_lline()",
            "get_city_location": "control_location.get_city_location()"
        }

        if locations in apis:
            return eval(apis[locations])

        return APIS_WRONG