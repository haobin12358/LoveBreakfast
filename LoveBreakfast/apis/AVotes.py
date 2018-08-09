# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask_restful import Resource
from LoveBreakfast.config.Logs import PRINT_API_NAME
from LoveBreakfast.control.CVotes import CVotes
from LoveBreakfast.config.response import APIS_WRONG

class LBVotes(Resource):
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
            "get_all": "self.cvote.get_all()",
            "get_host": "self.cvote.get_host()",
            "get_vote": "self.cvote.get_vote()",

        }

        if votes in apis:
            return eval(apis[votes])

        return APIS_WRONG