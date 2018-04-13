# *- coding:utf8 *-
import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
from flask import request
import json
import uuid
from config.status import response_ok


class Clocations():
    def __init__(self):
        from config.status import response_error
        from config.status_code import error_param_miss
        from config.messages import error_messages_param_miss
        self.param_miss = {}
        self.param_miss["status"] = response_error
        self.param_miss["status_code"] = error_param_miss
        self.param_miss["messages"] = error_messages_param_miss

        from config.status import response_system_error
        from config.messages import error_system_error
        self.system_error = {}
        self.system_error["status"] = response_system_error
        self.system_error["messages"] = error_system_error

    def get_all_location(self):
        from services.Slocations import Slocations
        slocations = Slocations()
        all_location = slocations.get_all()
        print all_location
        data = []
        for row in all_location:
            data_item = {}
            data_item["Lid"] = row.Lid
            data_item["Lname"] = row.Lname
            data_item["Lline"] = row.Litem
            data.append(data_item)
        response = {}
        response["status"] = response_ok
        response["message"] = "成功获取数据"
        response["data"] = data
        return response

    def get_lno(self):
        args = request.args.to_dict()
        if "Lid" not in args:
            return self.param_miss
        Lid = args["Lid"]
        from services.Slocations import Slocations
        slocations = Slocations()
        all_lno = slocations.get_all_lno_by_lid(Lid)
        data = []
        for row in all_lno:
            data_item = {}
            data_item["Lno"] = row.Lno
            data.append(data_item)
        response = {}
        response["status"] = response_ok
        response["message"] = "获取数据成功"
        response["data"] = data

        return response