# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from config.Logs import PRINT_API_NAME
from control.CVotes import CVotes
from config.response import APIS_WRONG

class AVotes(Resource):
    def __init__(self):
        self.cvote = CVotes()

    def post(self, votes):
        print(PRINT_API_NAME.format(votes))

        apis = {
            "make_vote":"self.cvote.make_vote()"
        }

        if votes in apis:
            return eval(apis[votes])

        return APIS_WRONG

    def get(self, votes):
        print(PRINT_API_NAME.format(votes))

        apis = {
            "get_all":"self.cvote.get_all()"
        }

        if votes in apis:
            return eval(apis[votes])

        return APIS_WRONG